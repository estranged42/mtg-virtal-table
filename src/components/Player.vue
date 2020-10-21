<template>
    <v-card
        class="mx-auto player-card"
        max-width="800"
        min-width="400"
    >
        <v-toolbar
            color="indigo"
            dark
        >
            <v-toolbar-title>{{ player.name }}</v-toolbar-title>
        </v-toolbar>
        <v-container fluid>
            <v-row dense>
            </v-row>
        </v-container>
    </v-card>
    
</template>

<script>
export default {
    props: ['player'],
}
</script>

<style lang="scss" scoped>

.player-card {
    margin: 15px;
}

</style>