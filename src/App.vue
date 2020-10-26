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
        :src="require('@/assets/ragnaros-faded.jpg')"
        :lazy-src="require('@/assets/ragnaros-blur.jpg')"
        height="100%"
      >
        <Table :players="players"/>
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
  }),
  methods: {
    addPlayer() {
      let p = {id: this.nextPlayerId, name: "New Player"}
      this.players = this.players.concat(p)
      this.nextPlayerId = this.nextPlayerId + 1
    },
  }
};
</script>

<style lang="scss" scoped>

.card-search {
  width: 400px;
}

.main-table {
  background-color: #9eabae;
}

</style>