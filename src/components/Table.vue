<template>
    <v-container class="players" >
        <v-row>
            <v-col v-for="p in players" :key="p.id" cols=4>
                <Player :player="p"/>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
// import { Drag, DropList } from "vue-easy-dnd";
import Player from './Player';

export default {
    components: {
        Player,
        //Drag,
        //DropList
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

</style>