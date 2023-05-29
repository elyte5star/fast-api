
<template>
    <div v-if="cart" id="basket">
        <div class="container">
            <div class="wrapper wrapper-content animated fadeInRight">
                <div class="row">
                    <div class="col-md-9">
                        <div class="ibox">
                            <div class="ibox-title">
                                <span class="pull-right">(<strong>{{ itemsInCart }}</strong>) items</span>
                                <h5>Items in your cart</h5>
                            </div>
                            <div v-for="product in  cart " v-bind:key="product" class="ibox-content">
                                <div class="table-responsive">
                                    <table class="table shoping-cart-table">
                                        <tbody>
                                            <tr>
                                                <td :style="{ width: '90px' }">
                                                    <div class="cart-product-imitation">
                                                        <img :src="'../images/products/' + product.image"
                                                            v-bind:alt="product.name">
                                                    </div>
                                                </td>
                                                <td class="desc">
                                                    <h3>
                                                        <router-link
                                                            :to="{ name: 'oneProduct', params: { pid: product.pid } }"
                                                            class="text-navy">
                                                            {{ product.name }}
                                                        </router-link>
                                                    </h3>
                                                    <p class="small">
                                                        {{ product.details }}
                                                    </p>
                                                    <dl class="small m-b-none">
                                                        <dt>Description</dt>
                                                        <dd>{{ product.description }}</dd>
                                                    </dl>

                                                    <div class="m-t-sm">
                                                        <a href="#" class="text-muted"><i class="fa fa-gift"></i> Add gift
                                                            package</a>
                                                        |
                                                        <a href="javascript:void(0)" v-on:click="removeFromCart(product)"
                                                            class="text-muted"><i class="fa fa-trash"></i> Remove
                                                            item</a>
                                                    </div>
                                                </td>

                                                <td v-if="product.discount.length > 0">
                                                    £{{ product.price }} 
                                                    <s class="small text-muted">$230,00</s>
                                                </td>
                                                <td :style="{ width: '65px' }">
                                                    <input type="text" :disabled="isDisabled" class="form-control"
                                                        placeholder="1">
                                                </td>
                                                <td>
                                                    <h4 :style="{ width: '130px' }">
                                                        £{{ product.price }}
                                                    </h4>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div class="ibox-content">
                                <button :disabled="!itemsInCart" @click="checkOut()" class="btn btn-primary pull-right"><i
                                        class="fa fa fa-shopping-cart"></i>
                                    Checkout</button>
                                <router-link id="cont_shopping" :to="{ name: 'home' }"><i
                                        class="fa fa-arrow-left"></i>Continue
                                    shopping</router-link>
                            </div>
                            <router-view />
                        </div>

                    </div>
                    <div class="col-md-3">
                        <div class="ibox">
                            <div class="ibox-title">
                                <h5>Cart Summary</h5>
                            </div>
                            <div class="ibox-content">
                                <span>
                                    Total
                                </span>
                                <h2 class="font-bold">
                                    £{{ totalPrice }}
                                </h2>

                                <hr>
                                <span class="text-muted small">
                                    *For Norway, Denmark and Sweden applicable sales tax will be applied
                                </span>
                                <div class="m-t-sm">
                                    <div class="btn-group">
                                        <button :disabled="!itemsInCart" @click="checkOut()"
                                            class="btn btn-primary pull-right"><i class="fa fa fa-shopping-cart"></i>
                                            Checkout</button> |
                                        <button :disabled="!itemsInCart" @click="emptyCart()" id="empty_cart"
                                            class="btn btn-warning pull-right"><i class="fa fa-cart-arrow-down"></i> Empty
                                            cart</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="ibox">
                            <div class="ibox-title">
                                <h5>Support</h5>
                            </div>
                            <div class="ibox-content text-center">
                                <h3><i class="fa fa-phone"></i> +47 409 78 057</h3>
                                <h3><i class="fa fa-envelope-o"></i> checkuti@gmail.com</h3>
                                <h3><i class="fa fa-github"></i> elyte5star</h3>
                                <span class="small">
                                    Please contact with us if you have any questions. We are avalible 24h.
                                </span>
                            </div>
                        </div>

                        <div class="ibox">
                            <div class="ibox-content">

                                <p class="font-bold">
                                    Other products you may be interested
                                </p>
                                <hr>
                                <div>
                                    <a href="#" class="product-name"> Product 1</a>
                                    <div class="small m-t-xs">
                                        Many desktop publishing packages and web page editors now.
                                    </div>
                                    <div class="m-t text-righ">

                                        <a href="#" class="btn btn-xs btn-outline btn-primary">Info <i
                                                class="fa fa-long-arrow-right"></i> </a>
                                    </div>
                                </div>
                                <hr>
                                <div>
                                    <a href="#" class="product-name"> Product 2</a>
                                    <div class="small m-t-xs">
                                        Many desktop publishing packages and web page editors now.
                                    </div>
                                    <div class="m-t text-righ">

                                        <a href="#" class="btn btn-xs btn-outline btn-primary">Info <i
                                                class="fa fa-long-arrow-right"></i> </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import { userCartStore } from '@/stores/cart'
import { userAuthStore } from '@/stores/auth_store'

import { storeToRefs } from 'pinia';
export default {
    name: 'CartView',
    data() {
        return {
            cart: [], user: Object, recommendationList: [], itemsInCart: 0, isDisabled: true
        }
    },
    methods: {
        removeFromCart(product) {
            const cartStore = userCartStore();
            cartStore.removeFromCart(product)
        },
        emptyCart() {
            const cartStore = userCartStore();
            cartStore.clearCart();
        },
        async checkOut() {
            const cartStore = userCartStore();
            cartStore.checkOut({ "cart": this.cart,"total_price":this.totalPrice})

        }

    },
    mounted() {
        const cartStore = userCartStore();
        const authStore = userAuthStore();
        const { user } = storeToRefs(authStore);
        const { cart, itemsInCart } = storeToRefs(cartStore);
        this.itemsInCart = itemsInCart
        this.cart = cart;
        this.user = user;


    },
    computed: {
        totalPrice() {
            let amount = 0;
            for (let item of this.cart) {

                amount += item.price;
            }
            return amount.toFixed(2);
        }
    }

}
</script>

<style scoped>
body {
    margin-top: 20px;
    background: #eee;
}

#cont_shopping {
    position: relative;
    float: left;

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