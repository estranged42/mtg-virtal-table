<template>

    <v-tooltip 
        bottom
        content-class="card_wrapper"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-chip
                light
                v-bind="attrs"
                v-on="on"
                class="card_chip"
                draggable
            >
                {{ carddata.name }}
                <ManaCost :cost="carddata.mana_cost"/>
            </v-chip>
            
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

                <v-img 
                    :src="carddata.image_uris.png"
                    :lazy-src="carddata.image_uris.small"
                    max-width=250
                ></v-img>
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

.card_chip {
    width: 300px;

}

.card_chip .v-chip__content {
    width: 100%;
    position: relative;
}

.card_chip .card_title {
    font-size: 1rem;
    padding: 0;
}

.card_chip .mana_costs_container {
    position: absolute;
    right: 0px;
    line-height: 1;
}

.v-tooltip__content.card_wrapper {
    background: none;
}

</style>
