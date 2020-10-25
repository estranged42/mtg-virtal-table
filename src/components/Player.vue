<template>
    <v-card
        class="player-card"
    >
        <v-toolbar
            color="indigo"
            dark
            @click="doEditPlayerName"
        >
            <v-toolbar-title 
                v-if="!editingPlayerName"
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
        </v-toolbar>
        <drop-list
            :items="cards"
            class="cards"
            @insert="onInsert"
            @reorder="onReorder"
            :column="true"
            mode="cut"
        >
            <template v-slot:item="{item}">
                <drag class="item" :key="item.table_card_id" :data="item" @cut="remove(item)">
                    <Card v-bind:carddata="item" :closefn="remove"/>
                </drag>
            </template>
            <template v-slot:feedback="{data}">
                <div class="item feedback" :key="data.table_card_id">
                    <Card v-bind:carddata="data"/>
                </div>
            </template>
            <template v-slot:reordering-feedback="{}">
                <div class="reordering-feedback" key="feedback"/>
            </template>
        </drop-list>
    </v-card>
    
</template>

<script>
import { Drag, DropList } from "vue-easy-dnd";
import Card from './Card';

export default {
    props: ['player'],
    components: {
        Card,
        Drag,
        DropList
    },
    data: () => ({
        cards: [],
        editingPlayerName: false,
    }),
    methods: {
        onInsert(event) {
            this.cards.splice(event.index, 0, event.data);
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
        }
    }
}
</script>

<style lang="scss" scoped>

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
}

</style>