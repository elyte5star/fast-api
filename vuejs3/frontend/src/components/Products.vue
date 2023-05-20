<template>
    <div class="products">
        <main id="container_" class="container">
            <h1 v-if="products">Products</h1>
            <article class="framed column" :id="'' + product.pid" v-for="product in products" v-bind:key="product">
                <div class="prod_left">
                    <img :src="'../images/products/' + product.image" v-bind:alt="product.name">
                    <div class="place">{{ product['category'] }}</div>
                </div>

                <div class="prod_right">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>

                    <h4>{{ product.price }} Kr.</h4>
                    <p>Available in stock {{ product.stock_quantity }}.</p>
                </div>
                <router-link :to="{
                    name: 'oneProduct',
                    params: {
                        pid: product.pid
                    }
                }">
                    <div class="details">Details</div>
                </router-link>
            </article>
        </main>
    </div>
</template>

<script>

export default {
    name: 'MainProducts',
    props: {
        products: {
            type: Array,
        }
    }

}
</script>
