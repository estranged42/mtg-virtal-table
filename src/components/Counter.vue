<template>
    <v-hover>
        <template v-slot:default="{ hover }">
            <v-card
                class="counter"
            >
                <div class="d-flex flex-no-wrap">
                        <Stepper :count="counterdata.count" icon="mdi-hexagon"/>
                        <v-card-title
                            v-text="counterdata.name"
                            v-if="!editingCounterName"
                            @click="doEditCounterName"
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
    props: ['counterdata', 'closefn'],
    data: () => ({
        editingCounterName: false,
    }),
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
}

.counter .v-card__title {
    padding: 0px 5px;
    font-size: 1rem;
}

.counter .close-btn {
    position: absolute;
    top: 0px;
    right: 0px;
    margin: 2px;
}
</style>