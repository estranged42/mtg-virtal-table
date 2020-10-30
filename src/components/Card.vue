<template>

    <v-tooltip 
        right
        content-class="card_wrapper"
        open-delay="600"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-hover>
                <template v-slot:default="{ hover }">
                    <v-card
                        class="card_card"
                        v-bind="attrs"
                        v-on="on"
                    >
                        <div class="d-flex flex-no-wrap">
                            <v-img 
                                :src="carddata.image_uris.art_crop"
                                max-width=50
                                max-height=50
                                min-height="50"
                                min-width="50"
                            ></v-img>

                            <div>
                                <v-card-title>
                                    {{ carddata.name }} 
                                    <ManaCost :cost="carddata.mana_cost"/>
                                </v-card-title>

                                <v-card-text>
                                    {{ carddata.type_line }} 
                                </v-card-text>
                            </div>

                            <v-btn
                                v-show="closefn && hover"
                                icon
                                x-small
                                color="grey"
                                class="close-btn"
                                @click="doClose"
                            >
                                <v-icon>mdi-close-circle</v-icon>
                            </v-btn>
                        </div>
                    </v-card>

                </template>
            </v-hover>            
        </template>

        <v-card
            class="card_details"
            rounded="lg"
            min-width="250"
        >
            <div class="d-flex flex-no-wrap justify-space-between">
                <div class="descriptive-text" v-if="!$vuetify.breakpoint.mobile">
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

.card_card {
    position: relative;
    margin: 2px;
}

.card_card .v-chip__content {
    width: 100%;
    position: relative;
}

.card_card .v-card__title {
    font-size: 1rem;
    line-height: 1rem;
    padding: 0;
}

.card_card .v-card__text {
    display: grid;
    grid-template-columns: auto auto;
    align-items: center;
    white-space: nowrap;
}

.card_card .v-card__subtitle, 
.card_card .v-card__text, 
.card_card .v-card__title {
    padding: 4px;
}

.card_card .mana_costs_container {
    margin: 0px 5px;
}

.card_card .close-btn {
    position: absolute;
    background-color: white;
    margin: 1px 6px;
    top: 0px;
    right: 0px;
}

.v-tooltip__content.card_wrapper {
    background: none;
}

.card_details .descriptive-text {
    width: 250px;

}

</style>
