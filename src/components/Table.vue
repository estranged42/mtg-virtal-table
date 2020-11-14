<template>
    <v-container class="players" flex>
        <v-row>
            <v-col v-for="p in $root.$data.state.players" :key="p.id" class="players-list">
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

    })
}
</script>

<style scoped lang="scss">

div.players {
    max-width: unset;
}
.players-list {
    min-width: 380px;
    flex-grow: 0.5;
}
</style>