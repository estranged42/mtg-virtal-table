<template>
    <v-card
        class="player-card"
        max-width="600"
        min-width="300"
        min-height="300"
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
            :column=true
        >
            <template v-slot:item="{item}">
                <drag class="item" :key="item.id">
                    <Card v-bind:carddata="item"/>
                </drag>
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
        cards: [
            {
                "object": "card",
                "id": "77f1f6ac-983f-4f3e-8906-47f774e8367b",
                "oracle_id": "c9ed8b01-959a-47d6-891e-0abbdccf6e4f",
                "name": "Armageddon",
                "image_uris": {
                    "small": "https://c1.scryfall.com/file/scryfall-cards/small/front/7/7/77f1f6ac-983f-4f3e-8906-47f774e8367b.jpg?1582021719",
                    "normal": "https://c1.scryfall.com/file/scryfall-cards/normal/front/7/7/77f1f6ac-983f-4f3e-8906-47f774e8367b.jpg?1582021719",
                    "large": "https://c1.scryfall.com/file/scryfall-cards/large/front/7/7/77f1f6ac-983f-4f3e-8906-47f774e8367b.jpg?1582021719",
                    "png": "https://c1.scryfall.com/file/scryfall-cards/png/front/7/7/77f1f6ac-983f-4f3e-8906-47f774e8367b.png?1582021719",
                    "art_crop": "https://c1.scryfall.com/file/scryfall-cards/art_crop/front/7/7/77f1f6ac-983f-4f3e-8906-47f774e8367b.jpg?1582021719",
                    "border_crop": "https://c1.scryfall.com/file/scryfall-cards/border_crop/front/7/7/77f1f6ac-983f-4f3e-8906-47f774e8367b.jpg?1582021719"
                },
                "mana_cost": "{3}{W}",
                "oracle_text": "Destroy all lands."
            },
            {
                "object": "card",
                "id": "ab55bb84-03c2-4989-8db4-0d5578ea0431",
                "oracle_id": "70d90ef4-0cda-405f-abf1-734fa909efa6",
                "name": "Armageddon Clock",
                "image_uris": {
                    "small": "https://c1.scryfall.com/file/scryfall-cards/small/front/a/b/ab55bb84-03c2-4989-8db4-0d5578ea0431.jpg?1562935409",
                    "normal": "https://c1.scryfall.com/file/scryfall-cards/normal/front/a/b/ab55bb84-03c2-4989-8db4-0d5578ea0431.jpg?1562935409",
                    "large": "https://c1.scryfall.com/file/scryfall-cards/large/front/a/b/ab55bb84-03c2-4989-8db4-0d5578ea0431.jpg?1562935409",
                    "png": "https://c1.scryfall.com/file/scryfall-cards/png/front/a/b/ab55bb84-03c2-4989-8db4-0d5578ea0431.png?1562935409",
                    "art_crop": "https://c1.scryfall.com/file/scryfall-cards/art_crop/front/a/b/ab55bb84-03c2-4989-8db4-0d5578ea0431.jpg?1562935409",
                    "border_crop": "https://c1.scryfall.com/file/scryfall-cards/border_crop/front/a/b/ab55bb84-03c2-4989-8db4-0d5578ea0431.jpg?1562935409"
                },
                "mana_cost": "{6}",
                "oracle_text": "At the beginning of your upkeep, put a doom counter on Armageddon Clock.\nAt the beginning of your draw step, Armageddon Clock deals damage equal to the number of doom counters on it to each player.\n{4}: Remove a doom counter from Armageddon Clock. Any player may activate this ability but only during any upkeep step."
            }
        ]
    }),
    methods: {
        onInsert(event) {
            this.cards.splice(event.index, 0, event.data);
        },
        onReorder(event) {
            event.apply(this.cards)
        }
    }
}
</script>

<style lang="scss" scoped>

.cards {
    padding: 5px;
    border: 1px solid black;
}

</style>