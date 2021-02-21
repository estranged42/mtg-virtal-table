import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

let _gamedata = undefined

var gamedata = {
  debug: process.env.NODE_ENV == "development",
  showalertbar: false,
  alertmessage: "",
  gambetableurl: "",
  connection: null,
  connected: false,
  state: {
    gameid: "0000",
    nextPlayerId: 3,
    nextCardId: 100,
    players: [
        {id: 1, name: "Player One", health: {val: 20}, cards: [], graveyard: [], is_active_player: true, is_monarch: false},
        {id: 2, name: "Player Two", health: {val: 20}, cards: [], graveyard: [], is_active_player: false, is_monarch: false},
    ],
  },
  alert(message) {
    this.alertmessage = message,
    this.showalertbar = true
  },
  setGameID(newValue) {
    if (this.debug) console.log('setGameID triggered with', newValue)
    this.state.gameid = newValue
  },
  disconnectFromGameID() {
    // Update this browser's URL
    if (_gamedata.debug) console.log("Not Connected. Clear URL.")
    history.pushState({gamdid: null}, `MTG: VirtualTable`, "/")
    this.state.gameid = "0000"
    this.connected = false
    this.connection = null
  },
  getCardId() {
    let id = this.state.nextCardId
    this.state.nextCardId = id + 1
    if (this.debug) console.log(`card id: ${id}`)
    return id
  },
  addPlayer() {
    let p = {
      id: this.state.nextPlayerId, 
      name: "New Player", 
      health: {val: 20}, 
      cards: [],
      graveyard: [],
      is_active_player: false,
      is_monarch: false
    }
    this.state.players = this.state.players.concat(p)
    this.state.nextPlayerId = this.state.nextPlayerId + 1
    if (this.debug) console.log(`Adding player ${p.id}: ${p.name}`)
    this.sendGameData()
  },
  deletePlayer(player) {
    if (this.debug) console.log(`Deleting player ${player.id}: ${player.name}`)
    let index = this.state.players.indexOf(player);
    this.state.players.splice(index, 1);
    this.sendGameData()
  },
  checkWebSocketConnection() {
    if (this.connection == null) {
      if (this.debug) console.log("Starting connection to WebSocket Server")
      this.connection = new WebSocket("wss://5mz965txnl.execute-api.us-west-2.amazonaws.com/dev")

      // store a reference to this gamedata object globally
      _gamedata = this
      this.connection.onmessage = this.handleIncomingMessage

      this.connection.onopen = (function(scope) {
        if (scope.debug) console.log("Successfully connected to the echo websocket server...")
        scope.connected = true
      })(this)
    }
  },
  handleIncomingMessage(event) {
    if (event.data != undefined) {
      let event_data = JSON.parse(event.data)
      let action = event_data.action
      if (event_data.error) {
        if (event_data.connected == false) {
          _gamedata.disconnectFromGameID()
        }
        if (_gamedata.debug) console.log(event_data.error)
        _gamedata.alert(event_data.error)
      }
      if (action == "host") {
        if (_gamedata.debug) console.log("new game id: " + event_data.gameid)
        _gamedata.state.gameid = event_data.gameid
        // Be sure to send over the game data after receiving host confirmation
        _gamedata.sendGameData()
        // Update this browser's URL
        history.pushState({gamdid: _gamedata.state.gameid}, `MTG: ${_gamedata.state.gameid}`, _gamedata.state.gameid)
        // Copy a game URL to the clipboard
        let document_url = new URL(document.location.href)
        _gamedata.gambetableurl = `${document_url.origin}/${_gamedata.state.gameid}`
        navigator.clipboard.writeText(_gamedata.gambetableurl).then(function() {
          /* clipboard successfully set */
          if (_gamedata.debug) console.log(_gamedata.gambetableurl)
          _gamedata.alert(`Coppied Game Table URL to clipboard: ${_gamedata.gambetableurl}`)
        }, function() {
          /* clipboard write failed */
          if (_gamedata.debug) console.log("text not coppied!")
        });
      } else if (action == "join") {
        _gamedata.state = event_data.gamedata
        if (_gamedata.debug) console.log("joined game: " + _gamedata.state.gameid)
        _gamedata.alert(`Joine Game Table: ${_gamedata.state.gameid}`)
        // Update this browser's URL
        history.pushState({gamdid: _gamedata.state.gameid}, `MTG: ${_gamedata.state.gameid}`, _gamedata.state.gameid)
      } else if (action == "sendstate") {
        if (_gamedata.debug) console.log("confirm new state sent")

      } else if (action == "updatestate") {
        if (_gamedata.debug) console.log("new state received")
        _gamedata.state = event_data.gamedata
      }

    } else {
      if (_gamedata.debug) console.log(event)
    }
  },
  sendWebSocketMessage(action, message=null) {
    if (this.connection) {
      let msg = {
          "action": action,
          "message": message
        }
        if (this.debug) console.log(`Sending Message: ${msg.action}`)

        if (this.connection.readyState == 1) {
          this.connection.send(JSON.stringify(msg))
        } else {
          this.connection.addEventListener('open', function deferred_msg() {
            this.send(JSON.stringify(msg))
            this.removeEventListener('open', deferred_msg, false)
          })
        }
      }
  },
  sendGameData() {
    this.sendWebSocketMessage("sendstate", this.state)
  },
  generateCardFromJSON(card_json) {
    // console.log(card_json)
    // Figure out how to handle dual-face cards
    let card_face = card_json
    if (card_json.card_faces != undefined) {
        card_face = card_json.card_faces[0]
    }
    let new_card = {
        "table_card_id": this.getCardId(),
        "table_card_counter": {val: 0},
        "table_card_show_counter": false,
        "table_card_is_tapped": false,
        "drag_type": "card",
        "name": card_json.name,
        "oracle_text": card_face.oracle_text,
        "flavor_text": card_face.flavor_text,
        "mana_cost": card_face.mana_cost,
        "type_line": card_json.type_line,
        "color_identity": card_json.color_identity,
        "power": card_json.power,
        "toughness": card_json.toughness,
        "image_uris": {
            "art_crop": card_face.image_uris.art_crop,
            "png": card_face.image_uris.png,
            "small": card_face.image_uris.small
        },
        "related_uris": {
            "gatherer": card_json.related_uris.gatherer
        }
    }
    let tokens = []
    if (card_json.all_parts && card_json.set_type && card_json.set_type != 'token') {
      for (let i = 0; i < card_json.all_parts.length; i++) {
        const element = card_json.all_parts[i];
        if (element.component && element.component == 'token') {
          tokens.push({
              "name": element.name,
              "url": element.uri,
              "id": element.id
          })
        }
      }
    }
    new_card.tokens = tokens
    return new_card
  },
  getCounterBackgroundImage() {
    let backgroundImages = [
      "images/token-yellow.jpg",
      "images/token-red.jpg",
      "images/token-blue.jpg",
      "images/token-green.jpg",
    ]
    let r = Math.floor(Math.random() * backgroundImages.length)
    return backgroundImages[r]
  }
}

new Vue({
  vuetify,
  data: gamedata,
  render: h => h(App)
}).$mount('#app')
