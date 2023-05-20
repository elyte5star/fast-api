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
                        <input type="number" name="volume" :id="num_items" placeholder="e.g 1,2" step="1" :min="1"
                            :max="productQuantity" :value="1"></label>
                    <button class="form-btn" @click="addToCart(product.pid)" :disabled="!inStock" type="button" id="add_p">
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
            cart: 0,
            productQuantity: 0
        }
    },
    methods: {
        addToCart(id) {
            this.cart += 1;
            console.log(id)
        }
    },
    watch: {
        async productQuantity(newQuantity) {
            console.log(newQuantity);
        }
    },
    async created() {
        const pStore = productStore();
        await pStore.getProductById(this.pid);
        const { product } = storeToRefs(pStore);
        this.product = product;
        this.productQuantity = this.product.stock_quantity;
    },
    computed: {
        inStock() {
            return this.productQuantity;
        }
    }

}

</script>