<template>
    <div v-if="product" class="product">
        <div id="product">
            <router-link id="cont_shopping_product" :to="{ name: 'home' }"><i class="fa fa-arrow-left"></i>Continue
                shopping</router-link>
            <h1>Product number: {{ product.pid }}</h1>
            <div class="framed">
                <div class="prod_left">
                    <img :src="'../images/products/' + product.image" v-bind:alt="product.name">
                    <div class="category1">{{ product.category }}</div>
                </div>
                <div class="prod_right1">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <h3>Unit Price: £{{ product.price }}.</h3>
                </div>
                <div class="prod_order">
                    <label :id="lb4">Quantity(multiples of 1):
                        <input type="number" name="volume" id="num_items" placeholder="e.g 1,2" step="1"
                            :min="inStock ? 1 : 0" :max="inStock ? productQuantity : 0" :value="inStock ? 1 : 0"></label>
                    <button class="form-btn" @click="addToCart()" :disabled="!inStock" type="button" id="add_to_cart">
                        Add to Cart.
                    </button>
                </div>
                <form @submit.prevent="onSubmit" class="reviewer-form">
                    <p>
                        <label for="reviewer_name">Name:</label>
                        <input id="reviewer_name" v-model="reviewer_name" required>
                    </p>
                    <p>
                        <label for="review">Review:</label>
                        <textarea id="review" v-model="review" required></textarea>
                    </p>
                    <span id="evaluate">Evaluate this product : </span>
                    <div class="rate">
                        <input type="radio" v-model.number="rating" id="star5" name="rating" value="5" />
                        <label for="star5" title="text">5 stars</label>
                        <input type="radio" v-model.number="rating" id="star4" name="rating" value="4" />
                        <label for="star4" title="text">4 stars</label>
                        <input type="radio" v-model.number="rating" id="star3" name="rating" value="3" />
                        <label for="star3" title="text">3 stars</label>
                        <input type="radio" v-model.number="rating" id="star2" name="rating" value="2" />
                        <label for="star2" title="text">2 stars</label>
                        <input type="radio" v-model.number="rating" id="star1" name="rating" value="1" />
                        <label for="star1" title="text">1 star</label>
                    </div>

                    <button class="form-btn" type="submit" id="submit_review">Submit review</button>
                </form>
            </div>
            <h1>Product Details</h1>
            <div class="framed">{{ product.details }}</div>
        </div>
        <router-view />
    </div>
</template>

<script>

import { productStore } from '@/stores/products'
import { userCartStore } from '@/stores/cart'

import { storeToRefs } from 'pinia';




export default {
    name: "ProductView",
    props: {
        pid: {
            type: String,
        }
    },
    data() {
        return {
            product: {},
            productQuantity: 0,
            reviewer_name: null,
            rating: null,
            review: null
        }
    },
    methods: {
        addToCart() {
            const cartStore = userCartStore();
            const volume = document.getElementById("num_items").value;
            cartStore.addToCart(this.product, volume)
        },
        onSubmit() {
            let productReview = {
                rname: this.reviewer_name,
                rating: this.rating,
                review: this.review,
                pid: this.product.pid
            }
            console.log(productReview);
            this.reviewer_name = null
            this.rating = null
            this.review = null

        }

    },
    watch: {
        async productQuantity(newQuantity) {
            console.log(newQuantity);
        },

    },
    async created() {
        if (this.pid) {
            const pStore = productStore();
            await pStore.getProductById(this.pid);
            const { product } = storeToRefs(pStore);
            this.product = product;
            this.productQuantity = this.product.stock_quantity;
            const elem = document.getElementById("add_to_cart");
            if (!this.productQuantity) elem.innerHTML = "Out of Stock";
            else elem.innerHTML = "Add to Cart";
            document.getElementById('product').scrollIntoView();

        } else {
            this.$swal("<strong>Wrong!</strong> " + " Product not found!");
        }

    },
    computed: {
        inStock() {
            return this.productQuantity;
        }
    }

}

</script>
<style scoped>
* {
    margin: 0;
    padding: 0;
}

#product h1 {
    background-color: #BCBCBC;
    color: white;
    padding: 5px;
    font-size: 1.2em;
    margin-top: 5px;
    text-align: center;
}

.prod_right1 {
    float: none;
    /* just to make it clear */
    padding-left: 10px;
    width: auto;
    overflow: hidden;
    position: relative;
    left: 100px;
    height: auto;
}

.prod_order {
    position: absolute;
    bottom: 0px;
    left: 250px;
}

#product img {
    height: 250px;
    width: 250px;
}

form {
    background-color: white;
    float: right;
}

textarea {
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
    background-color: #f8f8f8;
    resize: none;
    margin: 5px;
}

#evaluate {
    position: absolute;
    right: 170px;
    margin-top: 15px;

}

#add_to_cart:hover {
    background-color: lightgoldenrodyellow;
}

#submit_review:hover {
    background-color: lightgoldenrodyellow;
}

#reviewer_name {
    border-radius: 4px;
    margin: 5px;
    background-color: #f8f8f8;
    border: 2px solid #ccc;
}

#submit_review {
    margin: 5px;

}

#cont_shopping_product {
    color: black;
    text-decoration: none;

}

.rate {
    float: right;
    height: 46px;
    padding: 0 10px;
}

.rate:not(:checked)>input {
    position: absolute;
    top: -9999px;
}

.rate:not(:checked)>label {
    float: right;
    width: 1em;
    overflow: hidden;
    white-space: nowrap;
    cursor: pointer;
    font-size: 32px;
    color: #ccc;
}

.rate:not(:checked)>label:before {
    content: '★ ';
}

.rate>input:checked~label {
    color: #ffc700;
}

.rate:not(:checked)>label:hover,
.rate:not(:checked)>label:hover~label {
    color: #deb217;
}

.rate>input:checked+label:hover,
.rate>input:checked+label:hover~label,
.rate>input:checked~label:hover,
.rate>input:checked~label:hover~label,
.rate>label:hover~input:checked~label {
    color: #c59b08;
}
</style>