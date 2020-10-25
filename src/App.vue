<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-toolbar-title>MTG: Virtual Table</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        icon
        @click="addPlayer"
      >
        <v-icon>mdi-account-plus</v-icon>
      </v-btn>

      <v-spacer></v-spacer>

      <div class="card-search">
        <CardSearch/>
      </div>

    </v-app-bar>

    <v-main>
      <Table :players="players"/>
    </v-main>
  </v-app>
</template>

<script>
import Table from './components/Table';
import CardSearch from './components/CardSearch'

export default {
  name: 'App',

  components: {
    Table,
    CardSearch,
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

</style>