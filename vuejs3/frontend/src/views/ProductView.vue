<template>
    <div v-if="product" class="product">
        <div id="product">
            <router-link id="cont_shopping_product" :to="{ name: 'Home' }"><i class="fa fa-arrow-left"></i> Continue
                shopping</router-link>
            <h1>Product number: {{ product.pid }}</h1>
            <div class="framed1">
                <div class="prod_left">
                    <img v-if="product.image" :src="'../images/products/' + product.image" :alt="product.name">
                    <div class="category1">{{ product.category }}</div>
                </div>
                <div class="prod_right1">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <h3>Price: £{{ product.price }}</h3>
                    <p id="average_review"><i class="fa fa-star"></i> 3.2 ({{ reviewCount }} Reviews)</p>
                </div>
                <div class="prod_order">
                    <label :id="lb4">Quantity(multiples of 1):
                        <input type="number" name="volume" id="num_items" placeholder="e.g 1,2" step="1"
                            :min="inStock ? 1 : 0" :max="inStock ? productQuantity : 0" :value="inStock ? 1 : 0"></label>
                    <button class="form-btn" @click="addToCart()" :disabled="!inStock" type="button" id="add_to_cart">
                        Add to Cart.
                    </button>
                </div>

            </div>
            <h1>Product Details</h1>
            <div class="product_details1">{{ product.details }}</div>
        </div>
        <div class="container">
            <div class="wrapper wrapper-content animated fadeInRight">
                <div class="row">
                    <div class="col-md-7">
                        <div class="ibox">
                            <div class="ibox-title">
                                <span class="pull-right">(<strong>{{ reviewCount }}</strong>) reviews</span>
                                <h5>Product Review</h5>
                            </div>
                            <div v-for="review in  product.reviews " v-bind:key="review" class="ibox-content">
                                <div class="table-responsive">
                                    <table class="table product-review-table">
                                        <tbody>
                                            <tr>
                                                <td>
                                                    <div class="cart-product-imitation">
                                                        <img :src="'../images/user-icon.png'" alt="client">
                                                    </div>

                                                </td>
                                                <td class="desc" :style="{ width: '500px' }">
                                                    <h5>Nickname :
                                                        {{ review.reviewer_name }}
                                                    </h5>
                                                    <dl class="small m-b-none">
                                                        <dt>Description</dt>
                                                        <dd>{{ review.comment }}</dd>
                                                    </dl>

                                                    <dl class="small m-b-none">
                                                        <dt>Rating</dt>
                                                        <span id="old_rating" v-for="star in review.rating" :key="star">
                                                            <i class="fa fa-star"></i>
                                                        </span>
                                                    </dl>
                                                </td>
                                                <td colspan="2">
                                                    <dl class="small m-b-none">
                                                        <dt>Date</dt>
                                                        <dd>{{ formatDate(review.created_at) }}</dd>
                                                    </dl>
                                                </td>

                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div class="ibox-content">
                                <router-link id="cont_shopping" :to="{ name: 'Home' }"><i class="fa fa-arrow-left"></i>
                                    Continue
                                    shopping</router-link>
                            </div>

                        </div>

                    </div>
                    <div class="col-md-5">
                        <div class="ibox">
                            <div class="ibox-title">
                                <h5>Write a Review</h5>
                            </div>
                            <div class="ibox-content">

                                <div class="review">
                                    <form @submit.prevent="onSubmitReview" class="reviewer-form" id="review_form">
                                        <p>
                                            <label for="reviewer_name">Nickname:</label>
                                            <input id="reviewer_name" v-model="reviewer_name" required>
                                        </p>
                                        <p>
                                            <label for="reviewer_email">Email(We won't publish it):</label>
                                            <input id="reviewer_email" v-model="reviewer_email" required>
                                        </p>
                                        <p>
                                            <label for="review">Review:</label>
                                            <textarea id="review" v-model="review" required></textarea>
                                        </p>

                                        <span id="evaluate">Evaluate this product : </span>
                                        <div class="rate">
                                            <input type="radio" v-model.number="rating" id="star5" name="rating"
                                                value="5" />
                                            <label for="star5" title="text">5 stars</label>
                                            <input type="radio" v-model.number="rating" id="star4" name="rating"
                                                value="4" />
                                            <label for="star4" title="text">4 stars</label>
                                            <input type="radio" v-model.number="rating" id="star3" name="rating"
                                                value="3" />
                                            <label for="star3" title="text">3 stars</label>
                                            <input type="radio" v-model.number="rating" id="star2" name="rating"
                                                value="2" />
                                            <label for="star2" title="text">2 stars</label>
                                            <input type="radio" v-model.number="rating" id="star1" name="rating"
                                                value="1" />
                                            <label for="star1" title="text">1 star</label>
                                        </div>


                                        <button class="form-btn" type="submit" id="submit_review">Submit review</button>
                                    </form>

                                </div>

                            </div>
                        </div>

                        <div class="ibox">
                            <div class="ibox-title">
                                <h5>Support</h5>
                            </div>
                            <hr>
                            <span class="text-muted small">
                                *For Norway, Denmark and Sweden applicable sales tax will be applied
                            </span>
                            <hr>
                            <div class="ibox-content text-center">
                                <h6><i class="fa fa-phone"></i> +47 409 78 057</h6>
                                <h6><a href="mailto:checkuti@gmail.com"><i class="fa fa-envelope-o"></i>
                                        checkuti@gmail.com</a></h6>
                                <h6><a href="https://github.com/elyte5star"><i class="fa fa-github"></i> elyte5star</a></h6>
                                <span class="small">
                                    Please contact with us if you have any questions. We are avalible 24h.
                                </span>
                            </div>
                        </div>

                        <div class="ibox">
                            <div class="ibox-content">

                                <p class="font-bold">
                                    Similar products you may be interested
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

import { productStore } from '@/stores/products'
import { userCartStore } from '@/stores/cart'
import { userAlertStore } from '@/stores/alert'

import { storeToRefs } from 'pinia';

import moment from "moment";


export default {
    name: "ProductView",
    props: {
        pid: {
            type: String,
        }
    },
    data() {
        return {
            product: Object,
            productQuantity: 0,
            reviewer_name: null,
            reviewer_email: null,
            rating: null,
            review: null,
            pStore: productStore(),
            cartStore: userCartStore(),
            reviews: []
        }
    },

    methods: {
        addToCart() {
            const volume = document.getElementById("num_items").value;
            this.cartStore.addToCart(this.product, volume)
        },
        formatDate(value) {
            if (value) {
                return moment(String(value)).format("DD-MM-YYYY hh:mm");
            }
        },
        async onSubmitReview() {
            if (this.rating) {
                let productReview = {
                    reviewer_name: this.reviewer_name,
                    email: this.reviewer_email,
                    rating: Number(this.rating),
                    comment: this.review,
                    product_id: this.product.pid
                }
                console.log(productReview)

                await this.pStore.submitReview(productReview)
                this.reviewer_name = null
                this.rating = null
                this.review = null
                this.reviewer_email = null
            }else{
                const alertStore = userAlertStore();
                if (!this.rating) alertStore.error("Product evaluation required!");

            }

        }

    },
    async created() {
        if (this.pid) {
            await this.pStore.getProductById(this.pid);
            const { product, quantity, reviews } = storeToRefs(this.pStore);
            this.product = product;
            this.productQuantity = quantity;
            this.reviews = reviews;
            const elem = document.getElementById("add_to_cart");
            if (!this.productQuantity) elem.innerHTML = "Out of Stock";
            else elem.innerHTML = "Add to Cart";
            document.getElementById('product').scrollIntoView();


        } else {
            this.$swal("<strong>Wrong!</strong> " + " Supply a Product ID!");
        }

    },
    computed: {
        inStock() {
            return Number(this.productQuantity);
        },
        reviewCount() {
            return Number(this.reviews.length)
        }

    }

}

</script>

