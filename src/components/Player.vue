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

                <v-toolbar-title 
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

                <Stepper :count="health" icon="mdi-heart" iconoffset="2"/>

                <v-spacer></v-spacer>

                <v-btn
                    v-if="hover"
                    icon
                    @click.stop="dialog = true"
                >
                    <v-icon>mdi-delete</v-icon>
                </v-btn>

                </v-toolbar>
                </template>
            </v-hover>

            <drop-list
                :items="cards"
                class="cards"
                @insert="onInsert"
                @reorder="onReorder"
                :column="true"
                mode="cut"
            >
                <template v-slot:item="{item}">
                    <drag class="item" :key="getCardId()" :data="item" @cut="remove(item)">
                        <Card v-if="item.drag_type=='card'" v-bind:carddata="item" :closefn="remove"/>
                        <Counter v-if="item.drag_type=='counter'" :counterdata="item" :closefn="remove"/>
                    </drag>
                </template>
                <template v-slot:feedback="{data}">
                    <div class="item feedback" :key="getCardId()">
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
    props: ['player', 'deleteHandler'],
    components: {
        Card,
        Counter,
        Stepper,
        Drag,
        DropList
    },
    data: () => ({
        cards: [],
        editingPlayerName: false,
        dialog: false,
        health: {val: 20},
    }),
    methods: {
        onInsert(event) {
            let dataCopy = JSON.parse(JSON.stringify(event.data));
            this.cards.splice(event.index, 0, dataCopy);
        },
        onReorder(event) {
            event.apply(this.cards)
        },
        remove(value) {
            let index = this.cards.indexOf(value);
            this.cards.splice(index, 1);
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
        },
        doDeletePlayer() {
            this.dialog = false
            this.deleteHandler(this.player)
        }
    }
}
</script>

<style lang="scss">

.cards {
    padding: 5px;
    border: 1px solid black;
    min-height: 75px;

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