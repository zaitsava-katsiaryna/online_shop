import Vue from 'vue'
import Router from 'vue-router'
import Hello from '../components/Home.vue'
import Cart from '../components/Cart.vue'
import Login from '../components/Login.vue'
import PreviewContainer from "../components/PreviewContainer.vue";
import Signup from "../components/Signup.vue";
import Checkout from "../components/Checkout.vue"
import Item from '../components/Item.vue'
import Report from "../components/Report.vue";

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Hello',
            component: Hello
        },
        {
            path: '/preview',
            name: 'Preview',
            component: PreviewContainer
        },
        {
            path: '/cart',
            name: 'Cart',
            component: Cart
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/signup',
            name: 'Signup',
            component: Signup,
        },
        {
            path: '/checkout',
            name: 'Checkout',
            component: Checkout
        },
        {
            path: '/item/:id',
            name: 'Item',
            component: Item
        },
        {
            path: '/report',
            name: 'Report',
            component: Report
        }
    ]

})

