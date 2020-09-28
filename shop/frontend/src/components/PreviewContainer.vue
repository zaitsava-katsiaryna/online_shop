<template>
    <b-container class="p-1 text-center">
        <h2 class="text-center p-3">Gallery </h2>
        <div class='mb-3 w-50' style='display: inline-block'>
          <b-form-input list='search_list' type='search' v-model="search" placeholder="Search"></b-form-input>

          <datalist id="search_list">
            <option v-for="type in types">{{ type }}</option>
          </datalist>

          <b-form-checkbox
            id="checkbox-1"
            v-model="status"
            name="checkbox-1"
            value="available"
            unchecked-value="all"
            >
      Items availablility
    </b-form-checkbox>
        </div>
        <b-row>
            <b-col class="text-center" cols="4" v-for="item in items" :key="item.id">
                <ItemPreview :item="item"/>
            </b-col>
        </b-row>

    </b-container>

</template>

<script>
    import axios from 'axios'
    import ItemPreview from './ItemPreview.vue'

    export default {
        components:{
            ItemPreview
        },
        data() {
            return{
                items: [],
                search: '',
                types: ['Necklace', 'Bracelet', 'Earrings'],
                status: 'all'
            }
        },

        methods: {
          fetchData() {
            console.log('Do this')
            const path = 'http://localhost:5000/items';
            axios.get(path)
                .then(res => {
                  if (this.search == ''){
                    let new_items = {}

                      for (const item in res.data){
                        if (this.status == 'available'){
                          if (res.data[item].available != 0){
                            new_items[item] = res.data[item]
                          }
                        }
                        else{
                          new_items[item] = res.data[item]
                        }
                    }
                    this.items = new_items
                  }
                  else{
                    let new_items = {}
                    for (const item in res.data){
                      let type = res.data[item].type;

                      if(type.startsWith(this.search)){
                          new_items[item] = res.data[item]
                      }
                    }
                    if (this.status == 'available'){
                      for (const item in new_items){
                        if (new_items[item].available == 0){
                          delete new_items[item]
                        }
                      }
                    }
                    this.items = new_items;
                  }
                })
                .catch(error => {
                    console.log(error)
                });
          }
        },
        created() {
            this.fetchData();
        },
        watch: {
          search() {
            this.fetchData();
          },
          status() {
            console.log(this.status)
            this.fetchData();
          }
        }

    }

</script>

<style>


</style>
