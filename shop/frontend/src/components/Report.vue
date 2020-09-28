<template>
    <div>
        <h2 class="text-center p-3">Report</h2>
        <b-container>
            <b-row class="text-center align-middle" style="height: 50px;">
                <b-col><h5>UserID</h5></b-col>
                <b-col><h5>Username</h5></b-col>
                <b-col><h5>OrderID</h5></b-col>
                <b-col md="3"><h5>Order date</h5></b-col>
                <b-col><h5>Status</h5></b-col>
                <b-col md="4"><h5>Items</h5></b-col>
            </b-row>
            <b-row class="border-bottom mb-2 mt-2 text-center" v-for="row in data" :key="row.order_id">
                <b-col>{{row.user_id}}</b-col>
                <b-col>{{row.username}}</b-col>
                <b-col>{{row.order_id}}</b-col>
                <b-col md="3">{{row.order_date}}</b-col>
                <b-col>{{row.order_status}}</b-col>
                <b-col md="4">
                    <b-row v-for="item in row.items" :key="item.item_id">
                        <b-col># {{item.item_id}}</b-col>
                        <b-col>{{item.item_type}}</b-col>
                        <b-col>{{item.item_price}} EUR</b-col>
                        <b-col>{{item.amount}}</b-col>
                    </b-row>

                </b-col>

            </b-row>
        </b-container>
    </div>

</template>

<script>
    import axios from 'axios'

    export default {
        created() {
            const path = 'http://localhost:5000/report'
            axios.get(path)
                .then(res => {
                    this.data = res.data
                })
        },
        data() {
            return {
                data: []
            }
        }
    }
</script>