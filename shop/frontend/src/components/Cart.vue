<template>
    <div>
        <h2 class="text-center p-3">Shopping cart</h2>
        <h2 class="text-center p-3">{{cartMessage}}</h2>
        <b-container class="bv-example-row">
            <b-row class="text-center align-middle" style="line-height: 50px; height: 50px">
                <b-col cols="6"><h5>Product</h5></b-col>
                <b-col><h5>Price</h5></b-col>
                <b-col><h5>Quantity</h5></b-col>
                <b-col><h5>Remove</h5></b-col>
            </b-row>
            <div v-for="item in items">
                <CartItem :id="item.id" :type="item.type" :price="item.price" :value="item.amount" :url="item.url"/>
            </div>
        </b-container>
        <b-container class="bv-example-row p-5">
            <b-row class="pb-3"><h5>Total price: {{totalPrice}} EUR</h5></b-row>
            <b-row><div class="text-right"><b-button @click="checkout" :disabled="!check" :variant="buttonStyle">Check out</b-button></div></b-row>
        </b-container>

        <b-alert
                :show="dismissCountDown"
                dismissible
                fade
                class="position-fixed fixed-top m-0 rounded-0 text-center"
                style="z-index: 2000;"
                variant="danger"
                @dismiss-count-down="countDownChanged"
        >
            You are not logged in!
        </b-alert>
    </div>


</template>

<script>

    import CartItem from './CartItem.vue'
    import axios from 'axios'

    export default {
        name: 'CartComponent',
        data(){
            return {
                items: [],
                buttonStyle: '',
                dismissSecs: 2,
                dismissCountDown: 0,
            }
        },
        created(){
            if (localStorage.getItem('userID') === null){
              console.log('no access to cart')
            }
            else{
              const path = 'http://localhost:5000/cart_items/' + localStorage.getItem('userID');
              console.log(localStorage.getItem('userID'))
              axios.get(path, {
              params: {
                  access_token: localStorage.getItem('accessToken'),
              }
              })
              .then(res => {
                  let counter = 0;
                  this.items = res.data;
                  console.log(this.items)
                  for (let item in this.items){
                      counter++;
                  }
                  this.buttonStyle = counter === 0 ? 'outline-secondary':'outline-success';
              })
            }




        },
        components: {
            CartItem
        },
        computed: {
            totalPrice() {
                let total = 0;
                for (let item in this.items){
                    total +=  this.items[item].price * this.items[item].amount;
                }

                return Math.round((total + Number.EPSILON) * 100) / 100;
            },
            cartMessage(){
                if (this.items.length === 0){
                    return 'Cart is empty!'
                }
                return ''
            },
            check(){
                let counter = 0;
                for (let item in this.items){
                    counter++;
                }
                return counter > 0;
            }
        },
        methods: {
            checkout() {
                if (localStorage.accessToken){
                    this.$router.push('/checkout');
                    const path = 'http://localhost:5000/checkout/' + localStorage.getItem('userID');
                    axios.get(path)
                        .then(() => {
                            console.log('Checked out!')
                        })
                        .catch(err => {
                            console.log('Something went wrong :(', err)
                        })
                }
                else{
                    this.dismissCountDown = this.dismissSecs;
                }
            },
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown;
                if (this.dismissCountDown === 0){
                    this.$router.push('/login')
                }
            },
        }



    }

</script>
