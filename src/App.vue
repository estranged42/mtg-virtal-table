<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-toolbar-title>MTG: Virtual Table</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-account-plus</v-icon>
      </v-btn>

      <v-spacer></v-spacer>

      <div class="card-search">
        <CardSearch/>
      </div>

    </v-app-bar>

    <v-main>
      <Table/>
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

  }),
};
</script>

<style lang="scss" scoped>

.card-search {
  width: 400px;
}

</style>