<template>
    <div v-if="product" class="product">
        <div id="product">
            <router-link id="cont_shopping_product" :to="{ name: 'home' }"><i class="fa fa-arrow-left"></i> Continue
                shopping</router-link>
            <h1>Product number: {{ product.pid }}</h1>
            <div class="framed1">
                <div class="prod_left">
                    <img :src="'../images/products/' + product.image" v-bind:alt="product.name">
                    <div class="category1">{{ product.category }}</div>
                </div>
                <div class="prod_right1">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <h3>Unit Price: £{{ product.price }}</h3>
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
                        <label for="reviewer_email">Email(We won't publish it):</label>
                        <input id="reviewer_email" v-model="reviewer_email" required>
                    </p>
                    <p>
                        <label for="review">Review:</label>
                        <textarea id="review" v-model="review" required></textarea>
                    </p>
                    <label for="rating">Rating:</label>
                    <select v-model.number="rating" id="rating" required>
                        <option>5</option>
                        <option>4</option>
                        <option>3</option>
                        <option>2</option>
                        <option>1</option>
                    </select>
                    <button class="form-btn" type="submit" id="submit_review">Submit review</button>
                </form>
            </div>
            <h1>Product Details</h1>
            <div class="product_details1">{{ product.details }}</div>
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
            reviewer_email: null,
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
                reviewer_name: this.reviewer_name,
                reviewer_email: this.reviewer_email,
                rating: this.rating,
                comment: this.review,
                product_id: this.product.pid
            }
            console.log(productReview);
            this.reviewer_name = null
            this.rating = null
            this.review = null
            this.reviewer_email = null

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



