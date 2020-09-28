<template>
    <div class="text-center">
        <b-jumbotron style="background-image: url('https://images.unsplash.com/photo-1492892132812-a00a8b245c45?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')">
            <h1 style="color: whitesmoke"><i>IMAKA</i></h1>
            <h3 style="color: whitesmoke">Wooden jewellery store</h3>
            <b-button class="m-3" variant="outline-light" @click="viewMore">View collection</b-button>
        </b-jumbotron>
        <h2>Bestsellers</h2>
        <b-container>
            <b-row>
                <b-col cols="4" v-for="item in previewItems" :key="item.id">
                    <ItemPreview :item="item"/>
                </b-col>
            </b-row>
        </b-container>

    </div>
</template>

<script>
    import axios from 'axios'
    import ItemPreview from './ItemPreview.vue'

    export default {
        data(){
            return {
                previewItems: [],

            }
        },
       methods: {
           viewMore() {
               this.$router.push('/preview')
           }
       },
       created() {
           const path = 'http://localhost:5000/items';
           axios.get(path)
               .then(res => {
                 if (res.data){
                   this.previewItems = res.data;
                   this.previewItems = [res.data['1'], res.data['2'], res.data['3']]
                 }

               })

       },
       components: {
            ItemPreview
       }
    }
</script>


<style scoped>
    p{
        font-size: 2em;
        text-aligh: center;

    }
    .jumbotron{
        min-height: 400px;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }


</style>
