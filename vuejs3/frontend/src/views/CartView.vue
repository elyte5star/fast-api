
<template>
    <div v-if="cart" id="basket">
        <div class="container">
            <div class="wrapper wrapper-content animated fadeInRight">
                <div class="row">
                    <div class="col-md-8">
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
                                <router-link id="cont_shopping" :to="{ name: 'home' }"><i class="fa fa-arrow-left"></i>
                                    Continue
                                    shopping</router-link>
                            </div>

                        </div>

                    </div>
                    <div class="col-md-4">
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
                                <hr>
                                <div class="payment-info">
                                    <form @submit.prevent="onSubmit" class="payment-form">
                                        <div class="d-flex justify-content-between align-items-center"><span>Card
                                                details</span><img v-if="user" class="rounded" :src="'../images/' + user_image" v-bind:alt="user.username"
                                                width="30" ></div><span class="type d-block mt-3 mb-1">Card
                                            type</span><label class="radio"> <input type="radio" name="card" value="payment"
                                                checked> <span><img width="30"
                                                    :src="'../images/credit_cards/mastercard.png'"
                                                    alt="mastercard" /></span> </label>

                                        <label class="radio"> <input type="radio" name="card" value="payment"> <span><img
                                                    width="30" :src="'../images/credit_cards/visa.png'"
                                                    alt="visarcard" /></span> </label>

                                        <label class="radio"> <input type="radio" name="card" value="payment"> <span><img
                                                    width="30" :src="'../images/credit_cards/amex.png'" alt="amex" /></span>
                                        </label>


                                        <label class="radio"> <input type="radio" name="card" value="payment"> <span><img
                                                    width="30" :src="'../images/credit_cards/paypal.png'"
                                                    alt="paypal" /></span>
                                        </label>
                                        <div><label class="credit-card-label">Name on card</label><input type="text"
                                                class="form-control credit-inputs" placeholder="Name" required></div>
                                        <div><label class="credit-card-label">Card number</label><input type="tel"
                                                class="form-control credit-inputs" pattern="[0-9]*" maxlength="16"
                                                placeholder="0000 0000 0000 0000" minlength="16" required></div>
                                        <div class="row">
                                            <div class="col-md-6"><label class="credit-card-label">Card Expiry:
                                                </label><input type="month" class="form-control credit-inputs"
                                                    placeholder="12/24" required></div>
                                            <div class="col-md-6"><label class="credit-card-label">CVV</label><input
                                                    type="tel" class="form-control credit-inputs" placeholder="342"
                                                    pattern="[0-9]*" maxlength="3" required></div>
                                        </div>
                                        <hr class="line">
                                        <div class="d-flex justify-content-between information">
                                            <span>Subtotal</span><span>£{{
                                                totalPrice
                                            }}</span>
                                        </div>
                                        <div class="d-flex justify-content-between information">
                                            <span>Shipping</span><span>£0.00</span>
                                        </div>
                                        <div class="d-flex justify-content-between information"><span>Total(Incl.
                                                taxes)</span><span>£{{ totalPrice }}</span>
                                        </div>
                                        <hr>
                                        <div class="m-t-sm">
                                            <div class="btn-group">
                                                <button :disabled="!itemsInCart" class="btn btn-primary pull-right"
                                                    type="submit" id="submit_payment"><i class="fa fa fa-shopping-cart"></i>
                                                    Checkout</button> |
                                                <button :disabled="!itemsInCart" @click="emptyCart()" id="empty_cart"
                                                    class="btn btn-warning pull-right"><i class="fa fa-cart-arrow-down"></i>
                                                    Empty
                                                    cart</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>


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
                                <h3><a href="https://github.com/elyte5star"><i class="fa fa-github"></i> elyte5star</a></h3>
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
            cart: [], user: null, recommendationList: [], itemsInCart: 0, isDisabled: true,user_image: null
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
        async onSubmit() {
            console.log("payment");
            //const cartStore = userCartStore();
            //cartStore.checkOut({ "cart": this.cart, "total_price": this.totalPrice })

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
        this.user_image = this.user.admin ? "admin-icon.png" : "user-icon.png";


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
.payment-info {
    background:lightgoldenrodyellow;
    padding: 10px;
    border-radius: 6px;
    color: #fff;
    font-weight: bold;
}

.type {
    font-weight: 400;
    font-size: 10px;
}
label.radio input {
    position: absolute;
    top: 0;
    left: 0;
    visibility: hidden;
    pointer-events: none;
}
label.radio span {
    padding: 1px 12px;
    border: 2px solid #ada9a9;
    display: inline-block;
    color: #8f37aa;
    border-radius: 3px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: 300;
}

label.radio input:checked+span {
    border-color: #fff;
    background-color: blue;
    color: #fff;
}

.credit-inputs {
    background: rgb(102, 102, 221);
    color: #fff !important;
    border-color: rgb(102, 102, 221);
}

.credit-inputs::placeholder {
    color: #fff;
    font-size: 13px;
}

.credit-card-label {
    font-size: 9px;
    font-weight: 300;
}

.form-control.credit-inputs:focus {
    background: rgb(102, 102, 221);
    border: rgb(102, 102, 221);
}

.line {
    border-bottom: 1px solid rgb(102, 102, 221);
}

.information span {
    font-size: 12px;
    font-weight: 500;
}


.information {
    margin-bottom: 5px;
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