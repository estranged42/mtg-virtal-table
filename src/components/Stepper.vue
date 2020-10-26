<template>
    <v-sheet class="stepper-box" width="50" height="50">
        <p class="stepper-count">{{ count.val }}</p>
        <v-hover>
            <template v-slot:default="{ hover }">
                <div class="changecount add" @click="updateCount(1)">
                    <v-fade-transition>
                        <v-overlay
                            v-if="hover"
                            absolute
                            color="#036358"
                        >
                            <v-icon>mdi-chevron-up</v-icon>
                        </v-overlay>
                    </v-fade-transition>
                </div>
            </template>
        </v-hover>

        <v-hover>
            <template v-slot:default="{ hover }">
                <div class="changecount subtract" @click="updateCount(-1)">
                    <v-fade-transition>
                        <v-overlay
                            v-if="hover"
                            absolute
                            color="#036358"
                        >
                            <v-icon>mdi-chevron-down</v-icon>
                        </v-overlay>
                    </v-fade-transition>
                </div>
            </template>
        </v-hover>
    </v-sheet>
</template>

<script>
export default {
    props: ['count'],
    methods: {
        updateCount(inc) {
            this.count.val = this.count.val + inc
        }
    }
}
</script>

<style lang="scss" >

.stepper-box {
    display: inline-block;
    margin: 8px;
    position: relative;
}

p.stepper-count {
    margin: 0;
    padding: 0;
    text-align: center;
    font-size: 2em;
    font-weight: bold;
    line-height: 50px;
}

.stepper-box {
    .changecount {
        position: absolute;
        width: 50px;
        height: 25px;
        box-sizing: border-box;
    }

    .add {
        top: 0;
    }

    .subtract {
        top: 25px;
    }
}

</style>