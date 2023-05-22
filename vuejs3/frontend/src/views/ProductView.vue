<template>
    <div v-if="product">
        <div id="product">
            <div class="framed">
                <div class="prod_left">
                    <img :src="'../images/products/' + product.image" v-bind:alt="product.name">
                    <div class="place">{{ product.category }}</div>
                </div>
                <div class="prod_right">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <h3>Unit Price: {{ product.price }} Kr.</h3>
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
            <div class="framed">{{ product.details }}</div>
        </div>

    </div>
</template>

<script>

import { productStore } from '@/stores/products'
import { userAuthStore } from "@/stores/auth_store.js";

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
            productQuantity: 0
        }
    },
    methods: {
        addToCart() {
            const authStore = userAuthStore();
            const volume = document.getElementById("num_items").value;
            authStore.addToCart(this.product, volume)
        },

    },
    watch: {
        async productQuantity(newQuantity) {
            console.log(newQuantity);
        }
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