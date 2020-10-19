<template>

    <v-tooltip 
        bottom
        content-class="card_wrapper"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-card
                width="300"
                outlined
                class="card_slug"
                v-bind="attrs"
                v-on="on"
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
                            <ManaCost :cost="carddata.mana_cost"/>
                        </v-col>
                    </v-row>
                </v-container>
                
            </v-card>
        </template>
        <v-card
            class="card_details"
            width=500
            rounded="lg"
        >
            <div class="d-flex flex-no-wrap justify-space-between">
                <div>
                    <v-card-title
                    v-text="carddata.name"
                    ></v-card-title>

                    <v-card-text>
                        {{ carddata.oracle_text }}
                    </v-card-text>
                </div>

                <v-img :src="carddata.image_uris.png" width=250></v-img>
            </div>

            
        </v-card>
    </v-tooltip>
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

.card_slug {
    position: relative;
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
    flex-basis: unset;
    width: inherit;
}

.card_slug .manacost_container {
    flex-grow: unset;
    flex-basis: unset;
    line-height: 1;
}

.v-tooltip__content.card_wrapper {
    background: none;
}

.card_details {
    position: absolute;
    z-index: 100;
}

</style>
