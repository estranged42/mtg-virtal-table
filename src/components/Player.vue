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
                                @click.stop="doUntapAll"
                            >
                                <v-icon>mdi-undo-variant</v-icon>
                            </v-btn>
                        </template>
                        Untap All
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
                        <Card v-if="item.drag_type=='card'" v-bind:carddata="item" :closefn="remove" :duplicatefn="onDuplicate"/>
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
        </v-card>
        
    </span>
</template>

<script>
import { Drag, DropList } from "vue-easy-dnd";
import Card from './Card';
import Counter from './Counter';
import Stepper from './Stepper';

export default {
    props: ['player'],
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
    }),
    methods: {
        onInsert(event) {
            let dataCopy = JSON.parse(JSON.stringify(event.data));
            this.player.cards.splice(event.index, 0, dataCopy);
            this.$root.$data.sendGameData()
        },
        onDuplicate(card) {
            let dataCopy = JSON.parse(JSON.stringify(card));
            dataCopy.table_card_id = this.$root.$data.getCardId()
            this.player.cards.splice(event.index, 0, dataCopy);
            this.$root.$data.sendGameData()
        },
        onReorder(event) {
            event.apply(this.player.cards)
            this.$root.$data.sendGameData()
        },
        remove(value) {
            let index = this.player.cards.indexOf(value);
            this.player.cards.splice(index, 1);
            this.$root.$data.sendGameData()
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

</style>