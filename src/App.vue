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
                <drag :key="counterData.table_card_id" :data="counterData" @dragstart="onDragStart" @cut="onCut">
                    <Counter counterdata="counterData"/>
                </drag>
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
        :lazy-src="background.lazysrc"
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
    players: [
        {id: 1, name: "Player One"},
        {id: 2, name: "Player Two"},
    ],
    nextPlayerId: 3,
    background: { credit: "", url: "", filename: "" },
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
      }

    ],
    counterData: {
      drag_type: "counter", 
      name: "New Counter", 
      count: 1, 
      table_card_id: 0
    },
  }),
  mounted() {
    let r = Math.floor( Math.random() * this.backgroundImages.length )
    this.background = this.backgroundImages[r]
    this.counterData.table_card_id = this.getCardId()

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
      let p = {id: this.nextPlayerId, name: "New Player"}
      this.players = this.players.concat(p)
      this.nextPlayerId = this.nextPlayerId + 1
    },
    onDragStart(event) {
      let counterSource = event.source.data
      counterSource.table_card_id = this.getCardId()
      console.log(event)
    },
    onCut() {}
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