<template>
  <v-app class="mtgvirtualtable">

    <v-app-bar
      color="deep-purple"
      v-if="$vuetify.breakpoint.mobile"
      class="mobile-app-bar"
      src="images/wood-background2-sm.jpg"
      dark
      app
      fixed
      elevate-on-scroll
    >
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
      <v-toolbar-title>MTG: Virtual Table</v-toolbar-title>
      <v-spacer/>
      <v-btn
        icon
        v-bind="attrs"
        v-on="on"
        @click="infopanel=!infopanel"
      >
        <v-icon>mdi-information</v-icon>
      </v-btn>

    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      dark
      src="images/wood-background2-sm.jpg"
      width=275
      class="mtgappdrawer"
    >
        <v-list-item>
          <div class="d-flex flex-no-wrap app-name-header">
            <v-list-item-content>
              <v-list-item-title class="title">
                MTG: Virtual Table
              </v-list-item-title>
              <v-list-item-subtitle>
                By <a href="https://github.com/estranged42/mtg-virtual-table">Mark Fischer - @estranged</a>
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              @click="infopanel=!infopanel"
            >
              <v-icon>mdi-information</v-icon>
            </v-btn>

          </div>
        </v-list-item>


        <v-list
          nav
        >
          <v-divider></v-divider>

          <v-list-item
            link
            @click="settings=!settings"
          >
            <v-list-item-icon>
              <v-icon left>mdi-cog</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>Settings</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            link
            @click="addPlayer"
          >
            <v-list-item-icon>
              <v-icon left>mdi-account-plus</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>Add Player</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item
          >
            <v-list-item-content>
                <drag :data="counterData" @dragstart="onDragStart" @cut="onCut">
                    <Counter :counterdata="counterData"/>
                </drag>
            </v-list-item-content>
          </v-list-item>

        </v-list>

        <div class="card-search-container">
            <CardSearch @beginCardSearchDrag="doCloseDrawer"/>
        </div>

        <template v-slot:append>
            
        </template>

    </v-navigation-drawer>

    <v-main class="main-table">
      <v-img
        class="backgroundimage"
        :lazy-src="background.lazysrc"
        :src="background.filename"
        height="100%"
      >
        <Table />
        <v-sheet 
          class="image-credit pa-1"
        >
          Image Credit: <a :href="background.url">{{background.credit}}</a>
        </v-sheet>
      </v-img>
    </v-main>

    <v-dialog
      v-model="settings"
      width="500"
    >
      <v-card>

        <div v-if="$root.$data.connected">
          <v-card-title>
            Connected to Game Table:
          </v-card-title>

          <v-card-subtitle>
            <pre>{{ $root.$data.state.gameid }}</pre>
          </v-card-subtitle>
        </div>

        <v-expansion-panels focusable class="settings-panels">
          <v-expansion-panel>
            <v-expansion-panel-header>Start a new game table</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-btn
                color="primary"
                @click="doHostGame"
              >
                Start New Game Table
              </v-btn>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header>Join existing game table</v-expansion-panel-header>
            <v-expansion-panel-content>

              <v-text-field
                  v-model="$root.$data.state.gameid"
                  label="Enter game ID to join"
                  outlined
                  dense
                  hide-details
              ></v-text-field>

              <v-btn
                color="primary"
                @click="doJoinGame"
              >
                Join Game Table
              </v-btn>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>

      </v-card>
    </v-dialog>


    <v-dialog
      v-model="infopanel"
      min-width="300"
      max-width="800"
      max-height="800"
    >
      <v-card
        class="overflow-hidden"
      >

        <v-app-bar
            absolute
            elevate-on-scroll
            color="indigo"
            scroll-target="#infopanelscrollbody"
            dark
          >
            <v-toolbar-title>
              MTG: Virtual Table - Info
            </v-toolbar-title>
            <v-spacer/>
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              @click="infopanel=!infopanel"
            >
              <v-icon>mdi-close-circle</v-icon>
            </v-btn>
        </v-app-bar>

        <v-sheet
          id="infopanelscrollbody"
          class="overflow-y-auto"
          max-height="800"
        >
          <v-card-text>
          <p>
            MTG: Virtual Table lets you share a game table with other people so you can all participate in a virtual 
            Magic The Gathering game. One person hosts a game in Settings. Share the resulting table code with your 
            friends, and they'll be connected to the same table. No accounts or sign-ups required.
          </p>

          <h3>Basics</h3>
          <p>
            Start by setting up the number of players you're going to have. You can add players with the "Add Player"
            button in the left sidebar. You can rename players by clicking on the name. If you mouse over the player
            bar you can see the other toolbar buttons. Delete a player by clicking on the trashcan icon.
          </p>

          <p>
            Search for cards by entering text in the "Search for Cards" field in the left sidebar. Once the cards are
            returned, drag the card you want over to one of the players. You can re-order cards by dragging them around
            within a player, or drag them from one player to another. In the player toolbar there are two sorting buttons
            to sort alphabetically, or by card type.
          </p>

          <p>
            If you hover over a card, a detail view with a full image of the card will appear. While hovering over a 
            card, a close icon will appear in the upper right of the card. Clicking on this will discard the card from
            the player. You can also click on a card to 'tap' and 'untap' it.
          </p>
          <p>
            There's also a context menu for each card that can be accessed by right-clicking on the card.
            In the context menu you will find the following:
          <ul>
            <li>Duplicate Card - Makes a copy of this card and adds it to the player.</li>
            <li>Show Counter - Shows a configurable counter on the right side of the card.</li>
            <li>Discard - Discard this card from the player. Same as clicking the close icon.</li>
            <li>Create 'X' Token - If the card support creating tokens of various sorts, they will appear here. Not all 
                cards that create tokens are supported in this way by the underlying Scryfall API. Newer cards seem to
                be well supported, while older ones are not.</li>
            <li>View on Gatherer - Open a new tab to the gatherer.wizards.com entry for that card.</li>
          </ul>
          </p>

          <h3>Changelog</h3>
          <ul>
            <li>2020-11-24: Added 'Create Token' item to the Card context menu. Note that only newer cards seem to provide
                the data required to make this work, so not all cards that create tokens will display this item. Try the 
                'Hive Stirring' card for an example that works.</li>
            <li>2020-11-23: Added card sorting buttons to the Player toolbar.</li>
            <li>2020-11-22: Added tap/untap rotation to cards by clicking on them.</li>
            <li>2020-11-22: Added a toggleable counter to all cards.</li>
            <li>2020-11-15: Fixed bug with dual-faced cards. Not fully supported yet, will only display the front face.</li>
            <li>2020-11-14: Replaced the {W} placeholder text in card descriptions with icons.</li>
            <li>2020-11-04: Added multi-player support.</li>
            <li>2020-10-29: Better support for mobile browsers.</li>
            <li>2020-10-27: Added background images to the table.</li>
            <li>2020-10-27: Added player health stepper.</li>
            <li>2020-10-27: Dragging cards to players.</li>
            <li>2020-10-27: Card seraching basics.</li>
          </ul>
          </v-card-text>
        </v-sheet>

      </v-card>
    </v-dialog>

  </v-app>
</template>

<script>
import Table from './components/Table';
import CardSearch from './components/CardSearch'
import Counter from './components/Counter';
import { Drag } from "vue-easy-dnd";
import { decode } from "blurhash";

export default {
  name: 'App',

  components: {
    Table,
    CardSearch,
    Counter,
    Drag,
  },

  data: () => ({
    settings: false,
    infopanel: false,
    connection: null,
    connected: false,
    drawer: true,
    collapseOnScroll: false,
    background: { credit: "", url: "", filename: "", blurhash: "" },
    backgroundImages: [
      {
          credit: "Enrique Meseguer", 
          url: "https://pixabay.com/photos/fantasy-landscape-fantasy-landscape-4069829/",
          blurhash: "LNC%:KNbMwog_3IV%Nof_4M|oLV@",
          filename: require("@/assets/fantasy-4069829_1920.jpg")
      },
      {
          credit: "Raphael Lacoste", 
          url: "https://www.goodfon.com/wallpaper/raphael-lacoste-sentinels-fantasy-landscape-art-ruiny.html",
          blurhash: "LUCsgakCITM__NR+RPRjxvRjofj[",
          filename: require("@/assets/fantasy-ruins.jpg")
      },
      {
          credit: "Blizzard Entertainment", 
          url: "https://blizzard.gamespress.com/be/World-of-Warcraft",
          blurhash: "LMI{sLM~0j}-5RX8w[s;I@NGbckV",
          filename: require("@/assets/ragnaros.jpg")
      },
      {
          credit: "Blizzard Entertainment", 
          url: "https://blizzard.gamespress.com/be/World-of-Warcraft",
          blurhash: "LsI{~CSzNcsT}=oeWXjZNtxFayR+",
          filename: require("@/assets/Arrak_Landscape_Color.jpg")
      },
      {
          credit: "Johannes Plenio", 
          url: "https://unsplash.com/photos/1vzLW-ihJaM",
          blurhash: "LkEnhUR*0gt6ENj@$%ayIVoextWB",
          filename: "https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&ixid=eyJhcHBfaWQiOjE3Nzk4Mn0"
      },
      {
          credit: "Tomas Sobek", 
          url: "https://unsplash.com/photos/EKNe678ktEY",
          blurhash: "LrGSAkt7t8Rj?wofofWBtSa}WBj[",
          filename: "https://images.unsplash.com/photo-1472982728022-601a8d99e9af?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&ixid=eyJhcHBfaWQiOjE3Nzk4Mn0"
      },

    ],
    counterData: {
      drag_type: "counter", 
      name: "New Counter", 
      count: {val: 1}, 
      table_card_id: 0
    },
  }),
  mounted() {
    let r = Math.floor( Math.random() * this.backgroundImages.length )
    this.background = this.backgroundImages[r]
    this.counterData.table_card_id = this.$root.$data.getCardId()

    const width = 300
    const height = 150
    const pixels = decode(this.background.blurhash, width, height);

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const imageData = ctx.createImageData(width, height);
    imageData.data.set(pixels);
    ctx.putImageData(imageData, 0, 0);
    this.background.lazysrc = canvas.toDataURL('image/png')

  },
  methods: {
    addPlayer() {
      if (this.connected) this.sendWebSocketMessage("new player")
      this.$root.$data.addPlayer()
    },
    onDragStart(event) {
      let counterSource = event.source.data
      counterSource.table_card_id = this.$root.$data.getCardId()
      this.doCloseDrawer()
      // console.log(event)
    },
    doCloseDrawer() {
      if (this.$vuetify.breakpoint.mobile && this.drawer == true) {
        this.drawer = false
      }
    },
    onCut() {},
    doHostGame() {
      this.$root.$data.checkWebSocketConnection()
      this.$root.$data.sendWebSocketMessage('host')
      this.settings = false
    },
    doJoinGame() {
      this.$root.$data.checkWebSocketConnection()
      this.$root.$data.sendWebSocketMessage('join', this.$root.$data.state.gameid)
      this.settings = false
    }

  }
};
</script>

<style lang="scss">

.app-name-header {
  align-items: center;
}

header.mobile-app-bar {
  flex: unset;
}

div.mtgvirtualtable {
  a {
    color: white;
  }

  .image-credit {
    position: fixed;
    bottom: 0px;
    right: 0px;
    background-color: rgba(55,55,55,0.5);
    color: white;
  }

}

.backgroundimage > .v-image__image {
  filter: brightness(150%) contrast(40%) blur(2px);
}

.card-search {
  width: 400px;
}

.main-table {
  background-color: #9eabae;
}

.mtgappdrawer {
  .v-navigation-drawer__content {
    overflow-y: hidden;
  }
}

.settings-panels .v-expansion-panel-content {
  padding-top: 15px;
}

#infopanelscrollbody .v-card__text {
  margin-top: 70px;
}

</style>