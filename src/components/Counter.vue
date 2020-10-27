<template>
    <v-card
        class="counter"
    >
        <div class="d-flex flex-no-wrap justify-space-between">
                <v-card-title
                    v-text="name"
                    v-if="!editingCounterName"
                    @click="doEditCounterName"
                ></v-card-title>
                <v-card-title 
                    v-if="editingCounterName"
                    class="counter-title-edit"
                >
                    <v-text-field
                        class="edit-field"
                        v-model="name"
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
                <Stepper :count="count" icon="mdi-circle-outline"/>
                <v-btn
                    v-if="closefn"
                    icon
                    x-small
                    color="grey"
                    class="ma-1"
                    @click="doClose"
                >
                    <v-icon>mdi-close-circle</v-icon>
                </v-btn>
        </div>
    </v-card>

</template>

<script>
import Stepper from './Stepper';

export default {
    components: {
        Stepper,
    },
    props: ['counterdata', 'closefn'],
    data: () => ({
        name: "New Counter",
        count: {val: 1},
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

</style>