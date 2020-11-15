<template>

    <v-tooltip 
        right
        content-class="card_wrapper"
        open-delay="600"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-hover>
                <template v-slot:default="{ hover }">
                    <div>
                    <v-card
                        class="card_card"
                        v-bind="attrs"
                        v-on="on"
                        dark
                        @contextmenu="showContextMenu"
                    >
                        <div class="d-flex flex-no-wrap">
                            <v-img 
                                :src="carddata.image_uris.art_crop"
                                width=100%
                                max-width=350
                                max-height=65
                                min-height="65"
                            >
                                <div>
                                    <ManaCost :cost="carddata.mana_cost"/>

                                    <v-card-title>
                                        {{ carddata.name }} 
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
                            </v-img>
                        </div>
                    </v-card>

                    <v-menu
                        v-model="showMenu"
                        :position-x="menux"
                        :position-y="menuy"
                        absolute
                        offset-y
                        v-if="closable"
                        >
                        <v-list nav dense>
                            <v-list-item-group
                                color="primary"
                            >
                                <v-list-item @click="doClose">
                                    <v-list-item-title>Delete Card</v-list-item-title>
                                </v-list-item>

                                <v-list-item v-if="duplicatefn != undefined" @click="doDuplicate">
                                    <v-list-item-title>Duplicate Card</v-list-item-title>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                    </v-menu>
                    
                    </div>
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
                    width=250
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
        closefn: undefined,
        duplicatefn: undefined
    },
    components: {
        ManaCost,
    },
    data: () => ({
        closable: false,
        showMenu: false,
        menux: 0,
        menuy: 0,
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
        },
        doDuplicate() {
            if (this.duplicatefn != undefined) {
                this.duplicatefn(this.carddata)
            }
        },
        showContextMenu(event) {
            event.preventDefault()
            this.showMenu = false
            this.menux = event.clientX
            this.menuy = event.clientY
            this.$nextTick(() => {
                this.showMenu = true
            })
        },
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
    text-shadow: 0 0 0.4em black;
}

.card_card .v-image__image {
  filter: brightness(80%) contrast(80%);
}


.card_card .v-chip__content {
    width: 100%;
    position: relative;
}

.card_card .v-card__title {
    font-size: 1rem;
    line-height: 1rem;
    padding: 0;
    word-break: break-word;
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
    margin: 5px 5px;
    float: right;
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
