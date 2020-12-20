<template>
    <span>
        <v-dialog
            v-model="dialog"
            width="500"
            >
            <v-card>
                <v-card-title class="headline grey lighten-2">
                Delete {{ player.name }}?
                </v-card-title>

                <v-card-text>
                   Are yo usure you want to delete this player?
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    @click="dialog = false"
                >
                    CANCEL
                </v-btn>
                <v-btn
                    color="red"
                    text
                    @click="doDeletePlayer"
                >
                    DELETE
                </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-card
            class="player-card"
        >
            <v-hover>
            <template v-slot:default="{ hover }">
            <v-toolbar
                color="indigo"
                class="player-toolbar"
                dark
            >


                <v-tooltip 
                    bottom
                    open-delay="300"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <div
                            v-bind="attrs"
                            v-on="on"
                        >
                            <v-toolbar-title
                                v-bind="attrs"
                                v-on="on"
                                v-if="!editingPlayerName"
                                @click.self="doEditPlayerName"
                            >
                                {{ player.name }}
                            </v-toolbar-title>
                            <v-toolbar-title 
                                v-if="editingPlayerName"
                                class="toolbar-title-edit"
                            >
                                <v-text-field
                                    class="edit-field"
                                    v-model="player.name"
                                    label="Press enter to save"
                                    placeholder="Player Name"
                                    outlined
                                    dense
                                    hide-details="true"
                                    @keydown.enter="endEditPlayerName"
                                    @blur="endEditPlayerName"
                                    ref="playerNameEditField"
                                ></v-text-field>
                            </v-toolbar-title>
                        </div>
                    </template>
                    Click to edit player name
                </v-tooltip>

                <Stepper :count="player.health" icon="mdi-heart" iconoffset="2"/>

                    <!--
                        Active Player Button / Icon
                    -->
                    <v-tooltip 
                        v-show="hover || player.is_active_player"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-show="hover || player.is_active_player"
                                v-bind="attrs"
                                v-on="on"
                                icon
                                small
                                @click.stop="setactiveplayerfn(player)"
                            >
                                <v-icon v-if="player.is_active_player">mdi-account-check</v-icon>
                                <v-icon v-if="!player.is_active_player">mdi-account-outline</v-icon>
                            </v-btn>
                        </template>
                        <span v-if="player.is_active_player">It's this person's turn</span>
                        <span v-if="!player.is_active_player">Set as this player's turn</span>
                    </v-tooltip>

                    <!--
                        Monarch Button / Icon
                    -->
                    <v-tooltip 
                        v-show="hover || player.is_monarch"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-show="hover || player.is_monarch"
                                v-bind="attrs"
                                v-on="on"
                                icon
                                small
                                @click.stop="setmonarchfn(player)"
                            >
                                <v-icon v-if="player.is_monarch">mdi-crown</v-icon>
                                <v-icon v-if="!player.is_monarch">mdi-crown-outline</v-icon>
                            </v-btn>
                        </template>
                        <span v-if="player.is_monarch">This player is the Monarch</span>
                        <span v-if="!player.is_monarch">Claim the Monarchy</span>
                    </v-tooltip>

                <v-spacer></v-spacer>

                    <!--
                        Untap All Button
                    -->
                    <v-tooltip 
                        v-if="hover"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-bind="attrs"
                                v-on="on"
                                icon
                                small
                                @click.stop="doUntapAll"
                            >
                                <v-icon>mdi-undo-variant</v-icon>
                            </v-btn>
                        </template>
                        Untap All
                    </v-tooltip>

                    <!--
                        Toggle Graveyard Button
                    -->
                    <v-tooltip 
                        v-if="hover"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-bind="attrs"
                                v-on="on"
                                :disabled="player.graveyard.length == 0"
                                icon
                                small
                                @click.stop="showGraveyard = !showGraveyard"
                            >
                                <v-icon>mdi-grave-stone</v-icon>
                            </v-btn>
                        </template>
                        Show Graveyard / Exiled
                    </v-tooltip>

                    <!--
                        Sort Cards Alphabetically
                    -->
                    <v-tooltip 
                        v-if="hover"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-bind="attrs"
                                v-on="on"
                                icon
                                small
                                @click.stop="doSortCards('name')"
                            >
                                <v-icon>mdi-sort-alphabetical-descending-variant</v-icon>
                            </v-btn>
                        </template>
                        Sort Cards Alphabetically
                    </v-tooltip>

                    <!--
                        Sort Cards By Type
                    -->
                    <v-tooltip 
                        v-if="hover"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-bind="attrs"
                                v-on="on"
                                icon
                                small
                                @click.stop="doSortCards('type')"
                            >
                                <v-icon>mdi-sort-bool-ascending</v-icon>
                            </v-btn>
                        </template>
                        Sort Cards By Type
                    </v-tooltip>

                    <!--
                        Delete Player Button
                    -->
                    <v-tooltip 
                        v-if="hover"
                        bottom
                        open-delay="300"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                v-bind="attrs"
                                v-on="on"
                                icon
                                small
                                @click.stop="dialog = true"
                            >
                                <v-icon>mdi-delete</v-icon>
                            </v-btn>
                        </template>
                        Delete Player
                    </v-tooltip>

                </v-toolbar>
                </template>
            </v-hover>

            <drop-list
                :items="player.cards"
                class="cards"
                @insert="onInsert"
                @reorder="onReorder"
                :column="true"
                mode="cut"
            >
                <template v-slot:item="{item}">
                    <drag class="item" :key="item.table_card_id" :data="item" @cut="remove(item)" :disabled="$vuetify.breakpoint.mobile">
                        <Card 
                            v-if="item.drag_type=='card'" 
                            v-bind:carddata="item" 
                            :closefn="remove" 
                            :duplicatefn="onDuplicate"
                            :deletefn="cardFromPlayer"
                        />
                        <Counter v-if="item.drag_type=='counter'" :counterdata="item" :closefn="remove"/>
                    </drag>
                </template>
                <template v-slot:feedback="{data}">
                    <div class="item feedback" :key="data.table_card_id">
                        <Card v-if="data.drag_type=='card'" v-bind:carddata="data"/>
                        <Counter v-if="data.drag_type=='counter'" :counterdata="data"/>
                    </div>
                </template>
                <template v-slot:reordering-feedback="{}">
                    <div class="reordering-feedback" key="feedback"/>
                </template>
            </drop-list>

            <!-- 
                Graveyard Overlay
            -->

            <v-overlay
                :absolute="false"
                :opacity="0.8"
                :value="showGraveyard"
                class="player-graveyard-container"
                >

                <v-card
                    class="player-graveyard"
                >
                    <v-toolbar
                        color="indigo"
                        class="player-toolbar"
                        dark
                    >
                        <v-toolbar-title>
                            {{ player.name }}'s Graveyard
                        </v-toolbar-title>

                        <v-spacer></v-spacer>
                        <v-btn
                            icon
                            small
                            @click.stop="showGraveyard = false"
                        >
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </v-toolbar>

                    <div class="graveyard_card_list">
                        <Card 
                            v-for="card in player.graveyard"
                            :key="card.table_card_id"
                            v-bind:carddata="card" 
                            :closefn="remove" 
                            :duplicatefn="onDuplicate"
                            :returntoplayfn="onReturnToPlay"
                            :deletefn="cardFromGraveyard"
                        />
                    </div>
                </v-card>
                
            </v-overlay>
        </v-card>
        
    </span>
</template>

<script>
import { Drag, DropList } from "vue-easy-dnd";
import Card from './Card';
import Counter from './Counter';
import Stepper from './Stepper';

export default {
    props: [
        'player',
        'setactiveplayerfn',
        'setmonarchfn'
    ],
    components: {
        Card,
        Counter,
        Stepper,
        Drag,
        DropList
    },
    data: () => ({
        editingPlayerName: false,
        dialog: false,
        showGraveyard: false,
    }),
    methods: {
        onInsert(event) {
            let card = this.duplicateCard(event.data)
            // If this is a counter, pick a new random background color
            if (card.drag_type == 'counter') {
                card.background_image = this.$root.$data.getCounterBackgroundImage()
            }
            this.cardToPlayer(card, event.index)
            this.$root.$data.sendGameData()
        },
        onDuplicate(card) {
            let cardCopy = this.duplicateCard(card)
            this.cardToPlayer(cardCopy)
            this.$root.$data.sendGameData()
        },
        onReorder(event) {
            event.apply(this.player.cards)
            this.$root.$data.sendGameData()
        },
        remove(card) {
            // put a duplicate of the card into the graveyard
            let cardCopy = this.duplicateCard(card)
            cardCopy.inGraveyard = true
            this.cardToGraveyard(cardCopy)
            // delete the card from the player
            this.cardFromPlayer(card)
            this.$root.$data.sendGameData()
        },
        onReturnToPlay(card) {
            let cardCopy = this.duplicateCard(card)
            this.cardFromGraveyard(card)
            this.cardToPlayer(cardCopy)
            this.showGraveyard = false
            this.$root.$data.sendGameData()
        },
        duplicateCard(card) {
            let cardCopy = JSON.parse(JSON.stringify(card));
            cardCopy.table_card_id = this.$root.$data.getCardId()
            return cardCopy
        },
        cardFromPlayer(card) {
            let index = this.player.cards.indexOf(card);
            this.player.cards.splice(index, 1);
        },
        cardToPlayer(card, position) {
            card.inGraveyard = false
            if (position == undefined) {
                position = this.player.cards.length
            }
            this.player.cards.splice(position, 0, card);
        },
        cardFromGraveyard(card) {
            let index = this.player.graveyard.indexOf(card);
            this.player.graveyard.splice(index, 1);
        },
        cardToGraveyard(card) {
            card.inGraveyard = true
            card.table_card_is_tapped = false
            this.player.graveyard.splice(this.player.graveyard.length, 0, card)
        },
        doEditPlayerName() {
            this.editingPlayerName = true
            this.$nextTick(() => {
                let el = this.$refs.playerNameEditField
                el.focus()
            });
        },
        endEditPlayerName() {
            this.editingPlayerName = false
            this.$root.$data.sendGameData()
        },
        doDeletePlayer() {
            this.dialog = false
            this.$root.$data.deletePlayer(this.player)
            this.$root.$data.sendGameData()
        },
        doUntapAll() {
            for (let i = 0; i < this.player.cards.length; i++) {
                const card = this.player.cards[i];
                card.table_card_is_tapped = false;
            }
            this.$root.$data.sendGameData()
        },
        doSortCards(sortBy) {
            if (sortBy == "name") {
                this.player.cards = this.player.cards.sort(this.cardCompareByName)
            }
            if (sortBy == "type") {
                let sortedCards = this.player.cards.sort(this.cardCompareByName)
                this.player.cards = sortedCards.sort(this.cardCompareByType)
            }
            this.$root.$data.sendGameData()
        },
        cardCompareByName(card1, card2) {
            let c1 = card1.name.toLowerCase()
            let c2 = card2.name.toLowerCase()
            if (c1 < c2) {
                return -1
            }
            if (c1 > c2) {
                return 1
            }
            return 0
        },
        cardCompareByType(card1, card2) {
            let cardOrder = [
                "legendary land",
                "land",
                "basic snow land",
                "basic land",
                "legendary planeswalker",
                "legendary creature",
                "artifact creature",
                "creature",
                "token creature",
                "snow creature",
                "legendary artifact",
                "legendary enchantment artifact",
                "artifact",
                "token artifact",
                "enchantment",
                "instant",
                "sorcery",
                "table_card_counter",
            ]
            let c1 = card1.type_line.toLowerCase()
            let c2 = card2.type_line.toLowerCase()
            // Just get the first part of the type line, ie "Basic Snow Land — Plains"
            if (c1.includes("—")) {
                c1 = c1.split("—")[0].trim()
            }
            if (c2.includes("—")) {
                c2 = c2.split("—")[0].trim()
            }
            if (c1.includes("//")) {
                c1 = c1.split("//")[0].trim()
            }
            if (c2.includes("//")) {
                c2 = c2.split("//")[0].trim()
            }
            let idx1 = cardOrder.indexOf(c1)
            let idx2 = cardOrder.indexOf(c2)
            if (idx1 < idx2) {
                return -1
            }
            if (idx1 > idx2) {
                return 1
            }
            return 0
        }
    }
}
</script>

<style lang="scss">

.cards {
    padding: 5px;
    min-height: 75px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));

    .item {
        display: inline-block;
    }
}

.player-card {
    .edit-field,
    .toolbar-title-edit {
        overflow: visible;
    }

    .player-toolbar {
        .stepper-box {
            background-color: transparent;
            margin: 0px 10px;
        }
    }

    .cards {
        .stepper-box {
            background-color: #333;
            color: white;
        }
    }
}

.health {
    .v-input__control {
        flex-grow: unset;
        width: unset;
    }

    .v-input__slot {
        font-size: 1.3em;
    }
}

.player-graveyard-container {
    display: flex;
}

.player-graveyard-container .v-overlay__content {
    flex-basis: 40%;
}

.player-graveyard-container .graveyard_card_list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    max-height: 700px;
    overflow-y: scroll;
}

</style>