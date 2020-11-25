<template>
    <v-container class="players" flex>
        <v-row>
            <v-col v-for="p in $root.$data.state.players" :key="p.id" class="players-list">
                <Player :player="p" :setactiveplayerfn="doSetActivePlayer" :setmonarchfn="doSetMonarch"/>
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

    }),
    methods: {
        doSetActivePlayer(player) {
            for (let i = 0; i < this.$root.$data.state.players.length; i++) {
                const p = this.$root.$data.state.players[i];
                p.is_active_player = false
            }
            player.is_active_player = true
            this.$root.$data.sendGameData()
        },
        doSetMonarch(player) {
            if (player.is_monarch) {
                player.is_monarch = false
            } else {
                for (let i = 0; i < this.$root.$data.state.players.length; i++) {
                    const p = this.$root.$data.state.players[i];
                    p.is_monarch = false
                }
                player.is_monarch = true
            }
            this.$root.$data.sendGameData()
        },
    }
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