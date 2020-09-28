<template>
        <b-card
                :img-src="item.url"
                img-alt="Image"
                img-top
                tag="article"
                style="max-width: 20rem;"
                class="mb-2"


        >
            <b-card-title># {{item.id}}</b-card-title>
            <b-card-text>{{item.type}} </b-card-text>
            <b-card-text>{{item.price}} EUR</b-card-text>

            <b-button @click="viewDetails" variant="outline-secondary">View details</b-button>
        </b-card>

</template>

<script>
    export default {
        props: {
            item: Object
        },

        methods: {
            viewDetails() {
                this.$router.push('/item/' + this.$props.item.id)
            }
        }
    }
</script>

<style scoped>
    .card{
        border: none
    }

</style>
