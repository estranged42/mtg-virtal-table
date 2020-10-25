<template>
    <v-card
        class="player-card"
    >
        <v-toolbar
            color="indigo"
            dark
        >
            <v-toolbar-title>{{ player.name }}</v-toolbar-title>
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
                    <Card v-bind:carddata="item"/>
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
        cards: []
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


</style>