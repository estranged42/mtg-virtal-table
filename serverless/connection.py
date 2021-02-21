import logging
import os
import json
import traceback
import sys
import boto3
import time
from hashids import Hashids
from datetime import date, datetime, timedelta, timezone
import decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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


if os.getenv("GAMETABLE"):
    game_table_name = os.getenv("GAMETABLE")
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    game_table = dynamodb.Table(game_table_name)
else:
    logger.error("Environment Var GAMETABLE Not Set")

if os.getenv("APIGATEWAY_ENDPOINT"):
    apigateway_endpoint = os.getenv("APIGATEWAY_ENDPOINT")
    apig = boto3.client('apigatewaymanagementapi', endpoint_url=apigateway_endpoint, region_name='us-west-2')
else:
    logger.error("Environment Var APIGATEWAY_ENDPOINT Not Set")

if os.getenv("SSM_LAST_GAME_ID"):
    last_game_id_param = os.getenv("SSM_LAST_GAME_ID")
    ssm = boto3.client('ssm', region_name='us-west-2')
else:
    logger.error("Environment Var SSM_LAST_GAME_ID Not Set")


def get_parameter(p_name, decrypt=False):
    try:
        response = ssm.get_parameter(Name=p_name, WithDecryption=decrypt)
        v = response['Parameter']['Value']
        return v
    except Exception as ex:
        msg = str(ex)
        if "ParameterNotFound" in msg:
            log_info(msg)
            return None
        else:
            raise ex


def put_parameter(p_name, value):
    if type(value) != str:
        value = str(value)
    try:
        response = ssm.put_parameter(
            Name=p_name,
            Value=value, 
            Type='String',
            Overwrite=True
        )
        version = response['Version']
        return version
    except Exception as ex:
        msg = str(ex)
        if "ParameterNotFound" in msg:
            log_info(msg)
            return None
        else:
            raise ex


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


def generate_gameid():
    last_game_number_param_value = get_parameter(last_game_id_param)
    if last_game_number_param_value is None:
        log_error(f"last_game_id_param error: {last_game_number_param_value}")
        return None
    last_game_number = int(last_game_number_param_value)
    next_game_number = last_game_number + 1
    put_parameter(last_game_id_param, next_game_number)
    hashids = Hashids(salt=game_table_name, min_length=4, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    gameid = hashids.encode(next_game_number)
    log_info(f"last: {last_game_number}, next: {next_game_number}, gameid: {gameid}")
    return gameid


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


def put_game(game):
    expiration_time = time.time() + 3600
    game['expiration'] = decimal.Decimal(expiration_time)
    put_result = game_table.put_item(
        Item=game
    )

def add_player_to_game(gameid, connection_id):
    expiration_time = time.time() + 3600
    game = get_game(gameid)
    if game is None:
        game = {
            "gameid": gameid,
            "players": [connection_id],
            "gamedata": {},
            "expiration": decimal.Decimal(expiration_time)
        }
    else:
        players = game.get('players', [])
        if connection_id not in players:
            players.append(connection_id)
        game['players'] = players
    
    put_result = put_game(game)

    game = get_game(gameid)
    return game


def remove_player_from_game(gameid, connection_id):
    expiration_time = time.time() + 3600
    game = get_game(gameid)
    if game is not None:
        players = game.get('players', [])
        if connection_id in players:
            players.remove(connection_id)
            log_info(f"Removed {connection_id} from game {gameid}")
        game['players'] = players
    
    put_result = put_game(game)

    game = get_game(gameid)
    return game


def update_other_players(game, connection_id, domain_name):
    players = game.get('players', [])
    gameid = game['gameid']
    for p in players:
        if p != connection_id:
            try:
                resp = {
                    "action": "updatestate",
                    "gameid": gameid,
                    "gamedata": game['gamedata']
                }
                send_socket_message(resp, p, domain_name)
            except Exception as ex:
                msg = str(ex)
                if "GoneException" in msg:
                    log_info(f"Player {connection_id} is gone from game {gameid}")
                    remove_player_from_game(gameid, p)
                else:
                    raise ex


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
            gameid = generate_gameid()
            log_info(f"save host to new game: {gameid}")
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
            gameid = body.get('message', None)
            if gameid is None:
                return _format_response(f'Missing gameid for join', 400)

            game = get_game(gameid)
            if game is None:
                resp = {
                    "error": f'Could not join table {gameid}. Table does not exist, or has expired.',
                    "connected": False
                }
                send_socket_message(resp, connection_id, domain_name)
                return _format_response(f'Invalid gameid {gameid}', 400)

            game = add_player_to_game(gameid, connection_id)
            numplayers = len(game['players'])

            resp = {
                "action": "join",
                "gameid": gameid,
                "numplayers": numplayers,
                "gamedata": game['gamedata']
            }

        if action == "sendstate":
            new_game_data = body.get('message', None)
            if new_game_data is None:
                return _format_response(f'No new gamedata to set', 400)

            log_info(new_game_data)


            gameid = new_game_data.get('gameid', None)
            if gameid is None:
                return _format_response(f'Missing gameid for sendstate', 400)

            game = get_game(gameid)
            if game is None:
                resp = {
                    "error": f'Could not join table {gameid}. Table does not exist, or has expired.'
                }
                send_socket_message(resp, connection_id, domain_name)
                return _format_response(f'Invalid gameid {gameid}', 400)
            
            game['gamedata'] = new_game_data
            numplayers = len(game['players'])
            put_game(game)

            resp = {
                "action": "sendstate",
                "gameid": gameid,
                "numplayers": numplayers
            }

            update_other_players(game, connection_id, domain_name)

        send_socket_message(resp, connection_id, domain_name)
        return _format_response(resp, 200)
