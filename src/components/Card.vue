<template>

    <v-tooltip 
        right
        content-class="card_wrapper"
        open-delay="1200"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-hover>
                <template v-slot:default="{ hover }">
                    <div>
                    <v-card
                        v-bind:class="[{ 'is_tapped': carddata.table_card_is_tapped }, 'card_card']"
                        v-bind="attrs"
                        v-on="on"
                        dark
                        @click="doToggleTap"
                        @contextmenu="showContextMenu"
                    >
                        <div class="d-flex flex-no-wrap">
                            <v-img 
                                :src="carddata.image_uris.art_crop"
                                width=100%
                                max-width=350
                                max-height=72
                                min-height=72
                            >
                                <div>
                                    <ManaCost :cost="carddata.mana_cost"/>
                                    <Stepper 
                                        v-if="carddata.table_card_show_counter" 
                                        :count="carddata.table_card_counter" 
                                        icon="mdi-hexagon"
                                    />

                                    <v-card-title>
                                        {{ carddata.name }} 
                                    </v-card-title>

                                    <v-card-text>
                                        {{ carddata.type_line }} 
                                    </v-card-text>
                                </div>

                                <v-btn
                                    v-show="closefn && hover && !$vuetify.breakpoint.mobile"
                                    icon
                                    x-small
                                    color="grey"
                                    class="close-btn"
                                    @click.stop="showContextMenu"
                                >
                                    <v-icon>mdi-menu</v-icon>
                                </v-btn>

                                <v-btn
                                    v-show="closefn && $vuetify.breakpoint.mobile"
                                    icon
                                    x-small
                                    color="grey"
                                    class="close-btn"
                                    @click.stop="showContextMenu"
                                >
                                    <v-icon>mdi-menu</v-icon>
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
                        dark
                        v-if="closable"
                        
                    >
                        <!-- 
                            Context Menu Popup
                        -->
                        <v-list nav dense class="card-context-menu">

                            <v-list-item-group
                                color="primary"
                            >
                                <!-- Discard Card -->
                                <v-list-item 
                                    v-if="!carddata.inGraveyard"
                                    @click="doClose"
                                >
                                    <v-list-item-title>Discard</v-list-item-title>
                                </v-list-item>

                                <!-- Duplicate Card -->
                                <v-list-item 
                                    v-if="duplicatefn != undefined && !carddata.inGraveyard" 
                                    @click="doDuplicate"
                                >
                                    <v-list-item-title>Duplicate Card</v-list-item-title>
                                </v-list-item>

                                <!-- Toggle Counter -->
                                <v-list-item 
                                    v-if="duplicatefn != undefined && !carddata.inGraveyard" 
                                    @click="doToggleCounter"
                                >
                                    <v-list-item-title 
                                        v-if="carddata.table_card_show_counter==false"
                                    >
                                        Show Counter
                                    </v-list-item-title>
                                    <v-list-item-title 
                                        v-if="carddata.table_card_show_counter==true"
                                    >
                                        Hide Counter
                                    </v-list-item-title>
                                </v-list-item>

                                <!-- Create Tokens -->
                                <div v-if="!carddata.inGraveyard && carddata.tokens">
                                <v-list-item 
                                    v-for="token in carddata.tokens" 
                                    :key="token.id" 
                                    @click="doCreateToken(token)"
                                >
                                    <v-list-item-title>Create '{{ token.name }}' Token</v-list-item-title>
                                </v-list-item>
                                </div>

                                <!-- Return Card to Play -->
                                <v-list-item 
                                    v-if="carddata.inGraveyard"
                                    @click="doReturnToPlay"
                                >
                                    <v-list-item-title>Return to Play</v-list-item-title>
                                </v-list-item>

                                <!-- View on Gatherer -->
                                <a :href="carddata.related_uris.gatherer" target="_new">
                                <v-list-item>
                                    <v-list-item-title>View at Gatherer</v-list-item-title>
                                </v-list-item>
                                </a>
                                
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

                    <v-card-text v-html="oracle_text_enhanced" class="oracle-text"></v-card-text>
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
const axios = require('axios').default;
import Stepper from './Stepper';
import ManaCost from './ManaCost';

export default {
    props: {
        carddata: undefined,
        closefn: undefined,
        duplicatefn: undefined,
        returntoplayfn: undefined,
    },
    components: {
        ManaCost,
        Stepper,
    },
    data: () => ({
        closable: false,
        showMenu: false,
        menux: 0,
        menuy: 0,
        oracle_text_enhanced: "",
    }),
    created() {
        if (this.closefn != undefined) {
            this.closable = true
        }

        const regex = /({[0-9WBRGUTXC/]+})/g;
        let matches = this.carddata.oracle_text.match(regex)
        this.oracle_text_enhanced = this.carddata.oracle_text
        this.oracle_text_enhanced = this.oracle_text_enhanced.replace("\n", "<br>")
        if (matches) {
            for (let index = 0; index < matches.length; index++) {
                let m = matches[index];
                let m2 = m.replace("/", "")
                m2 = m2.replace("{", "")
                m2 = m2.replace("}", "")
                let t = `<div class='mana_cost mana_icon_${m2}'></div>`
                this.oracle_text_enhanced = this.oracle_text_enhanced.replace(m, t)
            }
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
        doToggleCounter() {
            this.carddata.table_card_show_counter = !this.carddata.table_card_show_counter
            this.$root.$data.sendGameData()
        },
        doToggleTap() {
            if (!this.carddata.inGraveyard) {
                this.carddata.table_card_is_tapped = !this.carddata.table_card_is_tapped
                this.$root.$data.sendGameData()
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
        doCreateToken(token) {
            let call_url = token.url
            axios
                .get(call_url)
                .then(response => {
                    let data = response.data
                    if (data.object == 'card') {
                        let new_card = this.$root.$data.generateCardFromJSON(data)
                        if (this.duplicatefn != undefined) {
                            this.duplicatefn(new_card)
                        }
                    }
                    this.loading = false
                })
                .catch(err => {
                    this.loading = false
                    if (err.response) {
                    console.log("response error")
                    console.log(err.response)
                    if (err.response.status == 404) {
                        this.setError("The requested token was not found. It likely expired.")
                    } else if (err.response.status == 403) {
                        this.setError("The requested token has expired.")
                    } else {
                        console.log(err)
                        this.setError("Something went wrong.")
                    }
                    } else if (err.request) {
                    console.log("request error")
                    console.log(err.request)
                    } else {
                    console.log(err)
                    }
                })
        },
        doReturnToPlay() {
            if (this.returntoplayfn != undefined) {
                this.returntoplayfn(this.carddata)
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

.card_card.is_tapped {
    transform: rotate(8deg);
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

.card_card .stepper-box {
    position: absolute;
    right: 0px;
    bottom: 0px;
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

.card_details .v-card__title {
    word-break: break-word;
}

.card_details .descriptive-text {
    width: 250px;
}

.oracle-text .mana_cost {
    position: relative;
    top: 3px;
}

.card-context-menu a {
    text-decoration: none;
}

</style>
