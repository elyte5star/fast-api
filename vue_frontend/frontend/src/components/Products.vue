<template>
    <div class="products">
        <main id="container_" class="container">
            <h1>Products</h1>
            <article class="framed column" v-for="product in products" v-bind:key="product">
                <div class="prod_left">
                    <img :src="'../images/products/' + product.image" v-bind:alt="product.name">
                    <div class="place">{{ product['category'] }}</div>
                </div>

                <div class="prod_right">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <h4 v-if="product.discount"><span style="text-decoration: line-through;">{{ product['price'] }}
                            Kr.</span>{{
                                product.discount[0]["new_price"] }} Kr.</h4>
                    <h4 v-else>{{ product['price'] }} Kr.</h4>
                    <p>Available in stock {{ product['stock_quantity'] }}.</p>
                </div>
                <a href="{{ url_for('one_product', pid=product.pid) }}">
                    <div class="details">Details</div>
                </a>

            </article>
        </main>
    </div>
</template>
  
<script>
import axios from 'axios'

export default {
    name: 'MainProducts',
    data() {
        return { products: [] }
    }
    ,
    mounted() {
    axios
      .get('/')
      .then((response) => {
        this.products = response.products
      })
  }

}
</script>