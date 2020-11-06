import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

let next_card_id = 1
Vue.prototype.getCardId = function() {
  let id = next_card_id
  next_card_id = id + 1
  return id
}

let _gamedata = undefined

var gamedata = {
  debug: true,
  connection: null,
  connected: false,
  state: {
    gameid: "0000",
    nextPlayerId: 3,
    players: [
        {id: 1, name: "Player One", health: {val: 20}, cards: []},
        {id: 2, name: "Player Two", health: {val: 20}, cards: []},
    ],
  },
  setGameID(newValue) {
    if (this.debug) console.log('setGameID triggered with', newValue)
    this.state.gameid = newValue
  },
  addPlayer() {
    let p = {id: this.state.nextPlayerId, name: "New Player"}
    this.state.players = this.state.players.concat(p)
    this.state.nextPlayerId = this.state.nextPlayerId + 1
    if (this.debug) console.log(`Adding player ${p.id}: ${p.name}`)
  },
  deletePlayer(player) {
    if (this.debug) console.log(`Deleting player ${player.id}: ${player.name}`)
    let index = this.state.players.indexOf(player);
    this.state.players.splice(index, 1);
  },
  checkWebSocketConnection() {
    if (this.connection == null) {
      if (this.debug) console.log("Starting connection to WebSocket Server")
      this.connection = new WebSocket("wss://5mz965txnl.execute-api.us-west-2.amazonaws.com/dev")

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
      if (action == "host") {
        _gamedata.state.gameid = event_data.gameid
        if (_gamedata.debug) console.log("new game id: " + _gamedata.state.gameid)
      }
    } else {
      if (_gamedata.debug) console.log(event)
    }
  },
  sendWebSocketMessage(action, message=null) {
   let msg = {
      "action": action,
      "message": message
    }

    if (this.connection.readyState == 1) {
      if (this.debug) console.log("Sending Message: " + JSON.stringify(msg))
      this.connection.send(JSON.stringify(msg))
    } else {
      this.connection.addEventListener('open', function deferred_msg() {
        if (this.debug) console.log("Sending Message: " + JSON.stringify(msg))
        this.send(JSON.stringify(msg))
        this.removeEventListener('open', deferred_msg, false)
      })
    }

  },
  sendGameData() {
    this.sendWebSocketMessage("sendstate", this.state)
  }
}

new Vue({
  vuetify,
  data: gamedata,
  render: h => h(App)
}).$mount('#app')
