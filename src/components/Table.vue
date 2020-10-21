<template>
    <drop-list
        :items="players"
        class="players"
        @insert="onInsert"
        @reorder="onReorder"
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
            {id: 2, name: "Eric"},
            {id: 1, name: "Mark"},
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
}

</style>