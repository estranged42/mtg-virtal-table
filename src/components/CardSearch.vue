<template>
    <v-autocomplete
        v-model="select"
        :loading="loading"
        :items="items"
        :search-input.sync="search"
        cache-items
        class="mx-4"
        flat
        hide-no-data
        hide-details
        label="Search Cards"
        solo-inverted
    ></v-autocomplete>
    
</template>

<script>
const axios = require('axios').default;

export default {
    data: () => ({
        loading: false,
        items: [],
        search: null,
        select: null,
    }),
    created() {
        this.searchCards()
    },
    methods: {
        searchCards: function() {
            let api_url = process.env.VUE_APP_CARD_API_URL
            let call_url = `${api_url}/cards/search?q=armaged`
            axios
                .get(call_url)
                .then(response => {
                    let data = response.data
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
