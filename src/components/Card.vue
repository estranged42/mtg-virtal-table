<template>
    <v-card
        width="300"
        outlined
        class="card_slug"
    >
        <v-container>
            <v-row
                no-gutters
                align="center"
                align-content="center"
            >
                <v-col>
                    <v-card-title
                        class="card_title"
                        v-text="carddata.name"
                    ></v-card-title>
                </v-col>
                <v-spacer/>
                <v-col class="manacost_container">
                    <ManaCost/>
                    <ManaCost/>
                </v-col>
            </v-row>
        </v-container>
        
    </v-card>
    
</template>

<script>
import ManaCost from './ManaCost';

export default {
    props: ['carddata'],
    components: {
        ManaCost,
    }
}
</script>

<style>

.v-autocomplete__content .v-list-item {
    padding: 0 5px;
}

.card_slug .card_title {
    font-size: 1rem;
    padding: 0;
}

.card_slug .container {
    padding: 0;
}

.card_slug .row {
    padding: 2px 8px;
}

.card_slug .col {
    padding: 0;
    width: inherit;
}

.card_slug .manacost_container {
    flex-grow: unset;
    flex-basis: unset;
    line-height: 1;
}

</style>
