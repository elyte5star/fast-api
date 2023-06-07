
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
                                        <div class="d-flex justify-content-between"><span>Card
                                                details</span><img v-if="user" class="rounded"
                                                :src="'../images/' + user_image" v-bind:alt="user.username" width="30">
                                        </div>
                                        <span class="type d-block mt-3 mb-1">Card type</span>
                                        <div id="card_type" class="card_type">
                                            <label class="radio"><input v-model="card" type="radio" name="card"
                                                    value="mastercard" checked>
                                                <span><img width="30" :src="'../images/credit_cards/mastercard.png'"
                                                        alt="mastercard" /></span>
                                            </label>

                                            <label class="radio"> <input v-model="card" type="radio" name="card"
                                                    value="visa">
                                                <span><img width="30" :src="'../images/credit_cards/visa.png'"
                                                        alt="visarcard" /></span> </label>

                                            <label class="radio"> <input v-model="card" type="radio" name="card"
                                                    value="amex">
                                                <span><img width="30" :src="'../images/credit_cards/amex.png'"
                                                        alt="amex" /></span>
                                            </label>


                                            <label class="radio"><input v-model="card" type="radio" name="card"
                                                    value="paypal"><span><img width="30"
                                                        :src="'../images/credit_cards/paypal.png'" alt="paypal" /></span>
                                            </label>
                                        </div>

                                        <div>
                                            <label class="credit-card-label">Name on card:</label><input type="text"
                                                class="form-control credit-inputs" v-model="nameOnCard" placeholder="Name"
                                                required>
                                        </div>
                                        <div>
                                            <label class="credit-card-label">Card number:</label>
                                            <input type="tel" class="form-control credit-inputs" v-model.number="cardNumber"
                                                pattern="[0-9]*" maxlength="16" placeholder="0000 0000 0000 0000"
                                                minlength="16" required>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6"><label class="credit-card-label">Card Expiry:
                                                </label><input type="month" v-model="expiryDate"
                                                    class="form-control credit-inputs" placeholder="12/24" required></div>
                                            <div class="col-md-6"><label class="credit-card-label">CVV</label><input
                                                    type="tel" v-model.number="cardCvv" class="form-control credit-inputs"
                                                    placeholder="342" pattern="[0-9]*" maxlength="3" required></div>
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
import { userAlertStore } from '@/stores/alert'


import { storeToRefs } from 'pinia';
export default {
    name: 'CartView',
    data() {
        return {
            cart: [], user: null, recommendationList: [], itemsInCart: 0,
            isDisabled: true, user_image: null, card: null, expiryDate: null, cardCvv: null,
            cardNumber: null, nameOnCard: null

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
            if (this.cardNumber && this.expiryDate && this.card && this.cardCvv && this.nameOnCard) {
                let paymentDetails = {
                    cardNumber: Number(this.cardNumber),
                    expiryDate: this.expiryDate,
                    cardCvv: Number(this.cardCvv),
                    cardType: this.card,
                    nameOnCard: this.nameOnCard
                }
                console.log(paymentDetails);

                this.cardNumber = null
                this.expiryDate = null
                this.cardCvv = null
                this.card = null
                this.nameOnCard = null
            } else {
                const alertStore = userAlertStore();
                if (!this.cardNumber) alertStore.error("Card number required");
                if (!this.card) alertStore.error("Card type required");
                if (!this.nameOnCard) alertStore.error("Card Holder name required");
                if (!this.expiryDate) alertStore.error("Expiry Date required");
                if (!this.cardCvv ) alertStore.error("CVV number required");
                

            }


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

