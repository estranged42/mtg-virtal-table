<template>
    <v-card
        width="300"
        outlined=true
        class="card_slug"
    >
        <v-card-title
            class="card_title"
            v-text="carddata.name"
        ></v-card-title>

    </v-card>
    
</template>

<script>

export default {
    props: ['carddata']
}
</script>

<style>

.v-autocomplete__content .v-list-item {
    padding: 5px;
}

.card_title {
    font-size: 1rem;
    padding: 2px 8px;
}

</style>
