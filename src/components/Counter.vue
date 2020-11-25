<template>
    <v-hover>
        <template v-slot:default="{ hover }">
            <v-card
                v-bind:class="[{ 'is_tapped': counterdata.table_card_is_tapped }, 'counter']"
                height=72
                dark
                @click="doToggleTap"
            >
                <div class="d-flex flex-no-wrap">
                    <v-img 
                        :src="counterdata.background_image"
                        width=100%
                        :max-width=maxwidth
                        max-height=72
                        min-height=72
                    >
                        <Stepper :count="counterdata.count" icon="mdi-hexagon"/>
                        <v-card-title
                            v-text="counterdata.name"
                            v-if="!editingCounterName"
                            @click.stop="doEditCounterName"
                        ></v-card-title>
                        <v-card-title 
                            v-if="editingCounterName"
                            class="counter-title-edit"
                        >
                            <v-text-field
                                class="edit-field"
                                v-model="counterdata.name"
                                label="Press enter to save"
                                placeholder="Counter Name"
                                outlined
                                dense
                                hide-details="true"
                                @keydown.enter="endEditCounterName"
                                @blur="endEditCounterName"
                                ref="counterNameEditField"
                            ></v-text-field>
                        </v-card-title>

                        <v-btn
                            v-if="closefn && hover"
                            icon
                            x-small
                            color="grey"
                            class="ma-1 close-btn"
                            @click="doClose"
                        >
                            <v-icon>mdi-close-circle</v-icon>
                        </v-btn>
                    </v-img>
                </div>
            </v-card>
        </template>
    </v-hover>

</template>

<script>
import Stepper from './Stepper';

export default {
    components: {
        Stepper,
    },
    props: ['counterdata', 'closefn', 'maxwidth'],
    data: () => ({
        editingCounterName: false
    }),
    created() {
        if (this.maxwidth == undefined) {
            this.maxwidth = 350
        }
    },
    methods: {
        doEditCounterName() {
            this.editingCounterName = true
            this.$nextTick(() => {
                let el = this.$refs.counterNameEditField
                el.focus()
            });
        },
        endEditCounterName() {
            this.editingCounterName = false
            this.$root.$data.sendGameData()
        },
        doToggleTap() {
            this.counterdata.table_card_is_tapped = !this.counterdata.table_card_is_tapped
            this.$root.$data.sendGameData()
        },
        doClose() {
            if (this.closefn != undefined) {
                this.closefn(this.counterdata)
            }
        }
    }
}
</script>

<style>

.counter {
    margin: 2px;
    position: relative;
    text-shadow: 0 0 0.4em black;
}

.counter .v-card__title {
    padding: 0px 5px;
    font-size: 1rem;
    word-break: break-word;
}

.counter .close-btn {
    position: absolute;
    top: 0px;
    right: 0px;
    margin: 2px;
}

.counter .stepper-box {
    position: absolute;
    right: 0px;
    bottom: 0px;
}

.counter .v-image__image {
  filter: brightness(80%) contrast(80%) blur(1px);;
}

.counter.is_tapped {
    transform: rotate(8deg);
}


</style>