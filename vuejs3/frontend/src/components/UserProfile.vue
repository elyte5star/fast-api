<template>
    <div v-if="user_info">
        <main id="user" class="container">
            <h1>Profile card for {{ user_info.username }}</h1>
            <article class="framed columnx" id="{{ user.userid }}">
                <div class="edit">
                    <a href="javascript:void(0)" @click="changeActiveComponent('update_details')"><i
                            class="fa fa-pencil-square-o" style="font-size: 40px"></i></a>
                </div>
                <div class="delete_contact">
                    <a href="javascript:void(0)" v-on:click="deleteUser(user_info.userid)"><i class="fa fa-trash-o"
                            style="font-size: 40px"></i></a>
                </div>
                <div class="item_left">
                    <img :src="'../images/' + user_image" v-bind:alt="user_info.username" />
                    <div class="discount">Discount : {{ user_info.discount }}%</div>
                </div>
                <div class="item_right">
                    <h3>Username : {{ user_info.username }}</h3>
                    <h5>Telephone : {{ user_info.telephone }}</h5>
                    <h5>Email : {{ user_info.email }}</h5>
                    <h6>User id : {{ user_info.userid }}.</h6>
                    <h6>Registered since {{ formatDate(user_info.created_at) }}.</h6>
                </div>
            </article>
            <div v-if="user_info.bookings">
                <div class="container">
                    <div class="wrapper wrapper-content animated fadeInRight">
                        <div class="row">
                            <div class="col-md-7">
                                <div class="ibox">
                                    <div class="ibox-title">
                                        <span class="pull-right">(<strong>{{ user_info.bookings.length }}</strong>)
                                            orders</span>
                                        <h5>Order History</h5>
                                    </div>
                                    <div v-for="booking in user_info.bookings " v-bind:key="booking" class="ibox-content">
                                        <div class="table-responsive">
                                            <table class="table shoping-cart-table" id="order_history"
                                                @click="orderDetailsTable(booking.cart)">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            Date: {{ formatDate(booking.created_at) }}
                                                            <p>Order number: {{ booking.oid }}</p>
                                                        </td>
                                                        <td :style="{ width: '65px' }">
                                                            <input type="text" :disabled="isDisabled" class="form-control"
                                                                :placeholder="booking.cart.length"
                                                                :value="booking.cart.length">
                                                        </td>
                                                        <td>
                                                            <h4 :style="{ width: '130px' }">
                                                                £{{ booking.total_price }}
                                                            </h4>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>

                                        </div>

                                    </div>

                                </div>
                            </div>

                            <div class="col-md-5">
                                <div class="ibox-title">
                                    <h5>Products per order</h5>
                                </div>
                                <div class="table-responsive" id="items_order">


                                </div>
                                <div class="ibox-content">
                                    <span>
                                        Total amount spent on shopping
                                    </span>
                                    <h2 class="font-bold">
                                        £{{ overallTotal }}
                                    </h2>

                                    <hr>

                                    <div class="m-t-sm">
                                        <div class="btn-group">
                                            <router-link id="cont_shopping" :to="{ name: 'Home' }"><i
                                                    class="fa fa-arrow-left"></i> Continue
                                                shopping</router-link>
                                        </div>
                                        <router-view />
                                    </div>
                                </div>
                                <div class="ibox">
                                    <div class="ibox-title">
                                        <h5>Support</h5>
                                    </div>
                                    <div class="ibox-content text-center">
                                        <h3><i class="fa fa-phone"></i> +47 409 78 057</h3>
                                        <h3><a href="mailto:checkuti@gmail.com"><i class="fa fa-envelope-o"></i>
                                                checkuti@gmail.com</a></h3>
                                        <h3><a href="https://github.com/elyte5star"><i class="fa fa-github"></i>
                                                elyte5star</a></h3>
                                        <span class="small">
                                            Please contact with us if you have any questions. We are avalible 24h.
                                        </span>
                                    </div>
                                </div>

                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>


<script>
/* eslint-disable */

import moment from "moment";
import { userStore } from "@/stores/userAccount";

export default {
    name: "UserProfile",
    props: ["user_info", "user_image"],

    methods: {
        orderDetailsTable(itemsArray) {
            let tableDiv = document.getElementById("items_order");
            tableDiv.innerHTML = "";
            tableDiv.innerHTML = '<table id=\"order_table\" class=\"table table-bordered table-sm\"><thead><tr><th>#</th><th>Name of product</th><th>Product number</th><th>Price</th></tr></thead><tfoot></tfoot><tbody></tbody></table>'
            for (let i = 0; i < itemsArray.length; i++) {
                let htmltxt = "<tr>";
                htmltxt += "<td>" + (parseInt(i) + 1) + "</td>";
                htmltxt += "<td>" + itemsArray[i].name + "</td>";
                htmltxt += "<td>" + itemsArray[i].pid + "</td>";
                htmltxt += "<td>" + "£" + itemsArray[i].price + "</td>";
                htmltxt += "</tr>";
                let tableRef = document.getElementById('order_table').getElementsByTagName('tbody')[0];
                let newRow = tableRef.insertRow(tableRef.rows.length);
                newRow.innerHTML = htmltxt;

            }

        },
        formatDate(value) {
            if (value) {
                return moment(String(value)).format("DD-MM-YYYY hh:mm");
            }
        },
        changeActiveComponent(str) {
            this.$emit('changeActiveComponent', str);
        },
        async deleteUser(id) {
            const user_store = userStore();
            await user_store.deleteUserAccount(id);

        }
    },
    computed: {
        overallTotal() {
            let amount = 0;
            for (let price of this.user_info.bookings) {
                amount += price.total_price;
            }
            return amount.toFixed(2);
        }
    }

};
</script>
<style scoped>
body {
    margin-top: 20px;
    background: #eee;
}

#order_history:hover {
    background-color: lightgoldenrodyellow;
    cursor: pointer;
}

#cont_shopping {
    position: relative;
    float: left;

}

a {
    text-decoration: none;
}

h3 {
    font-size: 16px;
}

#basket img {
    width: 50px;
    height: 50px;
}

.text-navy {
    color: #3299BB;
}

.cart-product-imitation {
    text-align: center;
    padding-top: 30px;
    height: 80px;
    width: 80px;
    background-color: #f8f8f9;
}


table.shoping-cart-table {
    margin-bottom: 0;
}

table.shoping-cart-table tr td {
    border: none;
    text-align: right;
}

table.shoping-cart-table tr td.desc,
table.shoping-cart-table tr td:first-child {
    text-align: left;
}

table.shoping-cart-table tr td:last-child {
    width: 80px;
}

.ibox {
    clear: both;
    margin-bottom: 25px;
    margin-top: 0;
    padding: 0;
}

.ibox.collapsed .ibox-content {
    display: none;
}

.ibox:after,
.ibox:before {
    display: table;
}

.ibox-title {
    -moz-border-bottom-colors: none;
    -moz-border-left-colors: none;
    -moz-border-right-colors: none;
    -moz-border-top-colors: none;
    background-color: #ffffff;
    border-color: #e7eaec;
    border-image: none;
    border-style: solid solid none;
    border-width: 3px 0 0;
    color: inherit;
    margin-bottom: 0;
    padding: 14px 15px 7px;
    min-height: 48px;
}

.ibox-content {
    background-color: #ffffff;
    color: inherit;
    padding: 15px 20px 20px 20px;
    border-color: #e7eaec;
    border-image: none;
    border-style: solid solid none;
    border-width: 1px 0;
}
</style>