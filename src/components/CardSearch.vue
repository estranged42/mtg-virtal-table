<template>
    <v-autocomplete
        v-model="select"
        :loading="loading"
        :items="items"
        :search-input.sync="search"
        class="mx-4"
        flat
        hide-no-data
        hide-details
        item-text="name"
        item-value="oracle_id"
        label="Search Cards"
        solo-inverted
    >
    <template v-slot:item="data">
        <Card v-bind:carddata="data.item"/>
    </template>
    
    </v-autocomplete>
    
</template>

<script>
const axios = require('axios').default;
import Card from './Card';

export default {
    components: {
        Card,
    },
    data: () => ({
        loading: false,
        items: [],
        search: null,
        select: null,
        inputWait: false,
    }),
    created() {
        // this.searchCards("dingus egg")
    },
    watch: {
      search (val) {
        if (val && !this.inputWait && val.length >= 3 && val !== this.select) {
            console.log(val)
            this.inputWait = true
            window.setTimeout(this.resetInputWait, 1000, this)
        }
        // val && length(val) >= 3 && val !== this.select  && this.searchCards(val)
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
            axios
                .get(call_url)
                .then(response => {
                    let data = response.data
                    if (data.total_cards > 0) {
                        let cards = data.data
                        cards.forEach(element => (function(scope){
                            scope.items = scope.items.concat(element)
                        })(this));
                    }
                    console.log(data)
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
        }
    }
}
</script>
