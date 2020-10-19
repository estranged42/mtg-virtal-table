<template>
    <div>
        <Player v-for="p in players" :key="p.id"/>
    </div>
</template>


<script>
import Player from './Player';

export default {
    components: {
        Player,
    },
    data: () => ({
        players: [
            {id: 1},
            {id: 2}
        ]
    })
}
</script>
