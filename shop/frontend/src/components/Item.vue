<template>
    <div >
        <b-card no-body class="overflow-hidden mx-auto" style="width: 70%">
            <b-row no-gutters>
                <b-col class='img-style' md="6" :style="{ backgroundImage: 'url(' + item.url + ')' }"
                >
                </b-col>
                <b-col md="6">
                    <b-card-body class="pl-5">
                        <b-container class="h-100">
                            <b-row><h2># {{item.id}}</h2></b-row>
                            <b-row><span class="span-title">{{item.type}}</span></b-row>
                            <b-row><span class="span-title">Price: </span><span> {{item.price}} EUR</span></b-row>
                            <b-row><span class="description">{{item.description}}</span></b-row>
                            <b-row :style="{color: inStockColor}">{{isAvailable}}</b-row>
                            <b-row><b-button :disabled="!check" class="float-left" :variant="buttonStyle" @click="addToCart">Add to cart</b-button></b-row>
                        </b-container>
                    </b-card-body>
                </b-col>
            </b-row>
        </b-card>
        <b-alert
                :show="dismissCountDown"
                dismissible
                fade
                class="position-fixed fixed-top m-0 rounded-0 text-center"
                style="z-index: 2000;"
                :variant="variant"
                @dismiss-count-down="countDownChanged"
        >
            {{alertMessage}}
        </b-alert>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {

        data(){
            return {
                item: {
                    id: '',
                    type: '',
                    price: '',
                    description: '',
                    url: '',
                    available: '',
                },
                dismissSecs: 2,
                dismissCountDown: 0,
                inStockColor: 'green',
                buttonStyle: 'outline-primary',
                alertMessage: '',
                variant: ''

            }
        },
        mounted(){
            let id = this.$route.params.id;
            // fetch item information by given id
            const path = 'http://localhost:5000/item/' + id;
            axios.get(path)
                .then(res => {
                    this.item.id = res.data.id;
                    this.item.type = res.data.type;
                    this.item.price = res.data.price;
                    this.item.description = res.data.description;
                    this.item.url = res.data.url;
                    this.item.available = res.data.available;
                })

        },
        computed: {
            isAvailable(){

                if (this.item.available > 0){
                    this.inStockColor = 'green';
                    this.buttonStyle = 'outline-success';
                    return 'In stock'
                }
                this.inStockColor = 'red';
                this.buttonStyle = 'outline-secondary';
                return 'Not in stock'
            },
            check(){
                return this.item.available > 0
            }
        },
        methods: {
            addToCart(){
                if (localStorage.accessToken){
                    const userID = localStorage.getItem('userID');
                    const itemID = this.item.id;
                    const path = 'http://localhost:5000/add_cart_item/' + userID + '/' + itemID;
                    axios.get(path)
                        .then(() => {
                            this.alertMessage = 'Item was successfully added to the cart!';
                            this.variant = 'success';
                            this.dismissCountDown = this.dismissSecs;
                        })
                        .catch(() => {
                            this.alertMessage = 'Item is already in the cart';
                            this.variant = 'danger';
                            this.dismissCountDown = this.dismissSecs;

                        })
                }
                else {
                    this.alertMessage = 'You are not logged in!';
                    this.variant = 'danger';
                    this.dismissCountDown = this.dismissSecs;
                }
            },
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown;
            },

        }
    }
</script>


<style scoped>
    .card{
        border: none;
    }

    .row{
        line-height: 50px;
    }

    .span-title{
        font-weight: bold;

    }
    .img-style{
        background-repeat: no-repeat;
        background-position: center;
    }
    .description{
        font-size: 15px;
    }
    .disabledButton{
        variant: outline-primary
    }
    .button{

    }


</style>