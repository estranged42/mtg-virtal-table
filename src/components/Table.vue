<template>
    <v-container class="players">
        <v-row>
            <v-col v-for="p in players" :key="p.id" cols=4>
                <Player :player="p" :deleteHandler="deletePlayer" />
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
    props: ['players'],
    data: () => ({

    }),
    methods: {
        onInsert(event) {
            this.players.splice(event.index, 0, event.data);
        },
        onReorder(event) {
            event.apply(this.players)
        },
        deletePlayer(player) {
            console.log(`Deleting player ${player.name}`)
            let index = this.players.indexOf(player);
            this.players.splice(index, 1);
        }
    }
}
</script>

<style scoped lang="scss">

</style>