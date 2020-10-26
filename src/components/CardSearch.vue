<template>
    <div>
        <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            :loading="loading"
            loader-height="5"
            ref="cardsearchfield"
            single-line
            hide-details
        ></v-text-field>

        <v-simple-table
            height="300"
        >
            <template v-slot:default>
                <tr
                    v-for="item in items"
                    :key="item.oracle_id"
                >
                    <td>
                        <drag :key="item.table_card_id" :data="item" @dragstart="onDragStart" @cut="onCut">
                            <Card v-bind:carddata="item"/>
                        </drag>
                    </td>
                </tr>
            </template>
        </v-simple-table>
    </div>
    
</template>

<script>
const axios = require('axios').default;
import { Drag } from "vue-easy-dnd";
import Card from './Card';

export default {
    components: {
        Card,
        Drag,
    },
    data: () => ({
        loading: false,
        items: [],
        search: null,
        select: null,
        inputWait: false,
        headers: [{ text: 'Card', value: 'card' }]
    }),
    watch: {
      search (val) {
        if (val && !this.inputWait && val.length >= 3 && val !== this.select) {
            this.inputWait = true
            window.setTimeout(this.resetInputWait, 1000, this)
        }
      },
    },
    methods: {
        resetInputWait: function(scope) {
            scope.inputWait = false
            scope.searchCards(scope.search)
        },
        searchCards: function(searchText) {
            this.items = []
            let api_url = process.env.VUE_APP_CARD_API_URL
            let call_url = `${api_url}/cards/search?q=${searchText}`
            call_url = encodeURI(call_url)
            this.loading = true
            axios
                .get(call_url)
                .then(response => {
                    let data = response.data
                    if (data.total_cards > 0) {
                        let cards = data.data
                        cards.forEach(element => (function(scope){
                            element.table_card_id = scope.getCardId()
                            // console.log(element)
                            scope.items = scope.items.concat(element)
                        })(this));
                    }
                    this.search = ""
                    this.loading = false
                })
                .catch(err => {
                    this.loading = false
                    if (err.response) {
                    console.log("response error")
                    console.log(err.response)
                    if (err.response.status == 404) {
                        this.setError("The requested token was not found. It likely expired.")
                    } else if (err.response.status == 403) {
                        this.setError("The requested token has expired.")
                    } else {
                        this.etError("Something went wrong trying to retrive credentials.")
                    }
                    } else if (err.request) {
                    console.log("request error")
                    console.log(err.request)
                    } else {
                    console.log(err)
                    }
                })
        },
        onDragStart: (event) => {
          console.log(event);
        },
        onCut: (event) => {
            console.log(event)
        }
    }
}
</script>
