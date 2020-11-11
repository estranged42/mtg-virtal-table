import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

let _gamedata = undefined

var gamedata = {
  debug: true,
  connection: null,
  connected: false,
  state: {
    gameid: "0000",
    nextPlayerId: 3,
    nextCardId: 100,
    players: [
        {id: 1, name: "Player One", health: {val: 20}, cards: []},
        {id: 2, name: "Player Two", health: {val: 20}, cards: []},
    ],
  },
  setGameID(newValue) {
    if (this.debug) console.log('setGameID triggered with', newValue)
    this.state.gameid = newValue
  },
  getCardId() {
    let id = this.state.nextCardId
    this.state.nextCardId = id + 1
    console.log(`card id: ${id}`)
    return id
  },
  addPlayer() {
    let p = {id: this.state.nextPlayerId, name: "New Player", health: {val: 20}, cards: []}
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
        if (_gamedata.debug) console.log("new game id: " + event_data.gameid)
        _gamedata.state.gameid = event_data.gameid
        // Be sure to send over the game data after receiving host confirmation
        _gamedata.sendGameData()

      } else if (action == "join") {
        _gamedata.state = event_data.gamedata
        if (_gamedata.debug) console.log("joined game: " + _gamedata.state.gameid)

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
  }
}

new Vue({
  vuetify,
  data: gamedata,
  render: h => h(App)
}).$mount('#app')
