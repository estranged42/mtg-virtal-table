<template>
    <drop-list
        :items="players"
        class="players"
        @insert="onInsert"
        @reorder="onReorder"
        :column=true
    >
        <template v-slot:item="{item}">
            <drag class="item" :key="item.id">
                <Player :player="item"/>
            </drag>
        </template>
    </drop-list>
</template>


<script>
import { Drag, DropList } from "vue-easy-dnd";
import Player from './Player';

export default {
    components: {
        Player,
        Drag,
        DropList
    },
    data: () => ({
        players: [
            {id: 1, name: "Mark"},
            {id: 4, name: "Angela"},
            {id: 5, name: "Kirin"},
            {id: 6, name: "Darla"},
        ]
    }),
    methods: {
        onInsert(event) {
            this.players.splice(event.index, 0, event.data);
        },
        onReorder(event) {
            event.apply(this.players)
        }
    }
}
</script>

<style scoped lang="scss">

.players {
    margin: 5px;

    .item {
        display: inline-block;
        margin: 15px;
    }
}

</style>