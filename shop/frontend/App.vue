<template>
    <div id="app">
        <b-navbar toggleable="lg" variant="light" class="m-0 fixed-top">
            <b-navbar-brand><router-link class='custom-link' :to="{ name: 'Hello' }">Home</router-link></b-navbar-brand>
            <b-navbar-brand><router-link class='custom-link' :to="{name: 'Preview'}">Gallery</router-link></b-navbar-brand>
            <b-navbar-brand><router-link class='custom-link' :to="{ name: 'Cart' }">Cart</router-link></b-navbar-brand>
            <b-navbar-brand><router-link class='custom-link' :to="{ name: 'Login' }">Login</router-link></b-navbar-brand>
            <b-navbar-brand @click="logout"><router-link class='custom-link' :to="{name: 'Hello'}">Logout</router-link></b-navbar-brand>
            <b-navbar-brand><router-link class='custom-link' :to="{ name: 'Report' }">Report</router-link></b-navbar-brand>
        </b-navbar>
        <div class='text-center m-2'>
          <div>{{currentDB}}</div>
            <b-button variant="outline-secondary" @click='fill_database'>Fill SQL database</b-button>
            <b-button variant="outline-secondary" @click='drop'>Drop SQL tables</b-button>
            <b-button variant="outline-secondary" @click='toggle'>Switch database</b-button>

        </div>
        <router-view></router-view>

        <b-alert
                :show="dismissCountDown"
                dismissible
                fade
                class="position-fixed fixed-top m-0 rounded-0 text-center"
                style="z-index: 2000;"
                variant="success"
                @dismiss-count-down="countDownChanged"
        >
            You are logged out!
        </b-alert>
    </div>
</template>

<script>
    import axios from 'axios'
    export default{
        name: 'HelloWorldApp',

        data(){
            return{
                dismissSecs: 2,
                dismissCountDown: 0,
                currentDB: ''
            }
        },

        mounted(){
          this.getCurrentDB()
        },
        methods:{
            getCurrentDB(){
                const path = 'http://localhost:5000/current'
                axios.get(path)
                  .then(res => {
                    this.currentDB = 'Current database: ' + res.data.current_db
                  })
            },
            drop() {
              const path = 'http://localhost:5000/drop'
              axios.get(path)
                .then(res => {
                  location.reload();
                })
            },

            fill_database() {
              const path = 'http://localhost:5000/fill'
              axios.get(path)
                .then(() => {
                  location.reload();
                })
            },
            logout(){
                localStorage.removeItem('accessToken');
                localStorage.removeItem('userID');
                localStorage.removeItem('username');
                this.dismissCountDown = this.dismissSecs;
            },
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown
            },
            toggle(){
              const path = 'http://localhost:5000/toggle'
              axios.get(path)
                .then(res => {
                  this.currentDB = 'Current database: ' + res.data.current_db
                  console.log('New database')
                })
            }
        }

    }
</script>

<style>
    #app {
        color: rgb(64, 63, 69);
        margin-top: 60px;
    }
    .custom-link{
        color: rgb(64, 63, 69);
    }
    .custom-link:hover{
        text-decoration: none;
    }
    span{
        font-size: 20px;
    }
</style>
