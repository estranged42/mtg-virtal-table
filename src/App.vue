<template>
  <v-app>

    <v-navigation-drawer
      app
      dark
      src="images/wood-background2.jpg"
      width=300
    >
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              MTG: Virtual Table
            </v-list-item-title>
            <v-list-item-subtitle>
              By Mark Fischer - @estranged
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
          nav
        >
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
              <Counter />
            </v-list-item-content>
          </v-list-item>


        </v-list>

        <template v-slot:append>
            <div class="pa-2">
              <CardSearch/>
            </div>
        </template>

    </v-navigation-drawer>

    <v-main class="main-table">
      <v-img
        class="backgroundimage"
        :src="background.filename"
        height="100%"
      >
        <Table :players="players"/>
        <v-sheet 
          class="image-credit pa-1"
          color="rgba(255,255,255,0.5)"
        >
          Image Credit: <a :href="background.url">{{background.credit}}</a>
        </v-sheet>
      </v-img>
    </v-main>
  </v-app>
</template>

<script>
import Table from './components/Table';
import CardSearch from './components/CardSearch'
import Counter from './components/Counter';

export default {
  name: 'App',

  components: {
    Table,
    CardSearch,
    Counter,
  },

  data: () => ({
    players: [
        {id: 1, name: "Player One"},
        {id: 2, name: "Player Two"},
    ],
    nextPlayerId: 3,
    background: undefined,
    backgroundImages: [
      {
          credit: "Enrique Meseguer", 
          url: "https://pixabay.com/photos/fantasy-landscape-fantasy-landscape-4069829/", 
          filename: require("@/assets/fantasy-4069829_1920.jpg")
      },
      {
          credit: "Raphael Lacoste", 
          url: "https://www.goodfon.com/wallpaper/raphael-lacoste-sentinels-fantasy-landscape-art-ruiny.html", 
          filename: require("@/assets/fantasy-ruins.jpg")
      },
      {
          credit: "Blizzard Entertainment", 
          url: "https://blizzard.gamespress.com/be/World-of-Warcraft", 
          filename: require("@/assets/ragnaros.jpg")
      },
      {
          credit: "Blizzard Entertainment", 
          url: "https://blizzard.gamespress.com/be/World-of-Warcraft", 
          filename: require("@/assets/Arrak_Landscape_Color.jpg")
      }
    ]
  }),
  mounted() {
    let r = Math.floor( Math.random() * this.backgroundImages.length )
    this.background = this.backgroundImages[r]
  },
  methods: {
    addPlayer() {
      let p = {id: this.nextPlayerId, name: "New Player"}
      this.players = this.players.concat(p)
      this.nextPlayerId = this.nextPlayerId + 1
    },
  }
};
</script>

<style lang="scss">

.backgroundimage {
  .v-image__image {
    filter: brightness(200%) contrast(30%) blur(2px);
  }

  .image-credit {
    position: fixed;
    bottom: 0px;
    right: 0px;
  }
}

.card-search {
  width: 400px;
}

.main-table {
  background-color: #9eabae;
}

</style>