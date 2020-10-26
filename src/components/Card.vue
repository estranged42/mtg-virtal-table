<template>

    <v-tooltip 
        right
        content-class="card_wrapper"
        open-delay="600"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-chip
                light
                v-bind="attrs"
                v-on="on"
                class="card_chip"
                :close="closable"
                @click:close="doClose"
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
    props: {
        carddata: undefined,
        closefn: undefined   
    },
    components: {
        ManaCost,
    },
    data: () => ({
        closable: false
    }),
    created() {
        if (this.closefn != undefined) {
            this.closable = true
        }
    },
    methods: {
        doClose() {
            if (this.closefn != undefined) {
                this.closefn(this.carddata)
            }
        }
    }
}
</script>

<style>

.v-autocomplete__content .v-list-item {
    padding: 0 5px;
}

.card_chip {
    margin: 2px;
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
    line-height: 0;
    margin: 0px 5px;
}

.v-tooltip__content.card_wrapper {
    background: none;
}

</style>
