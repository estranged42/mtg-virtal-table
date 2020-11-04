import logging
import os
import json
import traceback
import sys
import boto3
import time
import pytz
import uuid
import base64
from datetime import date, datetime, timedelta, timezone
import decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if os.getenv("GAMETABLE"):
    game_table_name = os.getenv("GAMETABLE")
else:
    logger.error("Environment Var GAMETABLE Not Set")

if os.getenv("APIGATEWAY_ENDPOINT"):
    apigateway_endpoint = os.getenv("APIGATEWAY_ENDPOINT")
else:
    logger.error("Environment Var APIGATEWAY_ENDPOINT Not Set")

apig = boto3.client('apigatewaymanagementapi', endpoint_url=apigateway_endpoint)

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table(game_table_name)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)

    elif isinstance(obj, bytes):
        try:
            s = obj.decode()
            return s
        except Exception:
            return str(obj)

    raise TypeError("Type %s not serializable" % type(obj))


def jsondumps(obj):
    return json.dumps(obj, default=json_serial)


def log_error(err_msg, event=None, context=None, tb=''):
    err_json = {
        'msg': err_msg,
        'event': event,
        'traceback': tb
    }
    json_str = jsondumps(err_json)
    logger.error(json_str)


def log_info(message):
    json_str = jsondumps(message)
    logger.info(json_str)


def _format_response(message, code=200, **additional_fields):
    response = {
        'message': message
    }

    if code != 200:
        logger.error(message)

    response.update(additional_fields)

    json_text = jsondumps(response)

    proxy_response = {
        'statusCode': code,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key"
        },
        'body': json_text
    }
    return proxy_response


def get_game(gameid):
    try:
        game_record = game_table.get_item(Key={"gameid": gameid})
        game = game_record.get("Item", None)
        log_info("Got Game:")
        log_info(game)
        return game

    except:
        err_msg = f'Error occurred while looking for game: {gameid}'
        log_error(err_msg, None, None, traceback.format_exc())
        return None


def add_player_to_game(gameid, connection_id):
    expiration_time = time.time() + 3600
    game = get_game(gameid)
    if game is None:
        players = [connection_id]
        gamedata = {}
    else:
        players = game.get('players', [])
        if connection_id not in players:
            players.append(connection_id)
        gamedata = game.get('gamedata', {})
    
    put_result = game_table.put_item(
        Item={
            "gameid": gameid,
            "players": players,
            "gamedata": gamedata,
            "expiration": decimal.Decimal(expiration_time)
        }
    )

    game = get_game(gameid)
    return game


def send_socket_message(message, connection_id, domain_name):
    log_info(message)
    resp = apig.post_to_connection(
        Data=jsondumps(message),
        ConnectionId=connection_id
    )


def handler(event, context):
    logger.info(jsondumps(event))
    action = event.get('event', None)
    request_context = event.get('requestContext', None)
    if not request_context:
        return _format_response(f'Missing requestContext', 400)

    route_key = request_context.get('routeKey', None)
    if not route_key:
        return _format_response(f'Missing routeKey', 400)

    connection_id = request_context.get('connectionId', None)
    if not connection_id:
        return _format_response(f'Missing connectionId', 400)

    domain_name = request_context.get('domainName', None)
    if not domain_name:
        return _format_response(f'Missing domainName', 400)

    body = event.get('body', None)
    if body:
        body = json.loads(body)

    if route_key == "$connect":
        return _format_response(f'Connected', 200)

    if route_key == "$disconnect":
        return _format_response(f'Bye', 200)

    if route_key == "$default":
        resp = {}
        
        if not body:
            return _format_response(f'Missing body', 400)

        action = body.get('action', None)

        if not action:
            return _format_response(f'Missing body', 400)

        if action == "host":
            gameid = uuid.uuid1()
            gameid = base64.b85encode(gameid.bytes)
            gameid = gameid.decode('utf-8')
            log_info("save host to new game:")
            game = add_player_to_game(gameid, connection_id)
            log_info("returned game:")
            log_info(game)
            numplayers = len(game['players'])

            resp = {
                "action": "host",
                "gameid": gameid,
                "numplayers": numplayers
            }

        if action == "join":
            gameid = body.get('gameid', None)
            if gameid is None:
                return _format_response(f'Missing gameid for join', 400)

            game = get_game(gameid)
            if game is None:
                return _format_response(f'Invalid gameid', 400)

            game = add_player_to_game(gameid, connection_id)
            numplayers = len(game['players'])

            resp = {
                "action": "join",
                "gameid": gameid,
                "numplayers": numplayers
            }

        send_socket_message(resp, connection_id, domain_name)
        return _format_response(resp, 200)
