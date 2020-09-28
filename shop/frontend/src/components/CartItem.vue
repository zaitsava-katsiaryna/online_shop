<template>

        <b-row class="align-middle border-bottom m-2" style="height: 70px; line-height: 70px;">
            <b-col cols="6">
                <b-media>
                    <template v-slot:aside>
                        <b-img :src="url" width="64" height="64" alt="placeholder"></b-img>
                    </template>
                    <h5># {{id}}</h5>
                    <p style="line-height: 20px">{{type}}</p>
                </b-media>
            </b-col>
            <b-col class="text-center align-middle">{{price}} EUR</b-col>
            <b-col @click="updateAmount" class="text-center align-middle"><b-form-spinbutton id="sb-inline" v-model="amount" inline></b-form-spinbutton></b-col>
            <b-col class="text-center"><b-button variant="outline-danger" @click="removeItem">Remove</b-button>
            </b-col>
        </b-row>


</template>

<script>

    import axios from 'axios'

    export default{
        props: {
            id: Number,
            type: String,
            price: Number,
            value: Number,
            url: String
        },
        data(){
            return{
                amount: 1
            }
        },
        mounted(){
            this.amount = this.$props.value
        },
        methods:{
            removeItem(){
                /**
                 * Remove item from the cart
                 */
                let customerID = localStorage.getItem('userID');
                let itemID = this.id;
                const path = 'http://localhost:5000/remove_cart_item/' + customerID + '/' + itemID;
                axios.delete(path)
                    .then(() => {
                        location.reload();
                    })
                    .catch(err => {
                        console.log('Something went wrong: ' + err);
                    });

            },
            updateAmount(){
                /**
                 * Update amount of items in the cart
                 */
                let customerID = localStorage.getItem('userID');
                let itemID = this.id;
                let newAmount = this.amount;
                const path = 'http://localhost:5000/update_cart_item/' + customerID + '/' + itemID + '/' + newAmount;
                axios.put(path)
                    .then(() => {
                        location.reload();
                    })
                    .catch(err => {
                        console.log('Something went wrong: ' + err);
                    });
            }
        },

    }
</script>
