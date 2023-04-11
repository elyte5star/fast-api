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
                </div>
                <a href="{{ url_for('one_product', pid=product.pid) }}">
                    <div class="details">Details</div>
                </a>

            </article>
        </main>
    </div>
</template>
  
<script>
export default {
    name: 'MainProducts',
    data() {
        return {
            products: [
                {
                    "name": "Angry Bird-l",
                    "price": 100.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.The word ergonomic gets tossed around like it's the star ingredient in a wellness-word salad. We ourselves are guilty of blindly buying into products that are stamped with its body-support seal of approval — especially now that we're stuck at home in a make-shift office",
                    "image": "1.png",
                    "category": "black",
                    "stock_quantity": 30
                },
                {
                    "name": "Angry Bird-i",
                    "price": 500.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "2.png",
                    "category": "yellow",
                    "stock_quantity": 30
                },
                {
                    "name": "Angry Bird-w",
                    "price": 900.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "3.png",
                    "category": "grey",
                    "stock_quantity": 30
                },
                {
                    "name": "Angry Bird",
                    "price": 900.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "4.png",
                    "category": "red",
                    "stock_quantity": 30
                },
                {
                    "name": "Clash of clans-v",
                    "price": 1000.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "5.png",
                    "category": "pink",
                    "stock_quantity": 30
                },
                {
                    "name": "Clash of clans-a",
                    "price": 700.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "6.png",
                    "category": "coal",
                    "stock_quantity": 10
                },
                {
                    "name": "Clash of clans-q",
                    "price": 8900.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "7.png",
                    "category": "rock",
                    "stock_quantity": 60
                },
                {
                    "name": "Clash of clans-r",
                    "price": 1300.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "8.png",
                    "category": "mat",
                    "stock_quantity": 90
                },
                {
                    "name": "Super Mario",
                    "price": 5800.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "9.png",
                    "category": "pale",
                    "stock_quantity": 10
                },
                {
                    "name": "Clash of clans-o",
                    "price": 1200.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "10.png",
                    "category": "pale",
                    "stock_quantity": 3
                },
                {
                    "name": "Clash of clans-n",
                    "price": 10000.89,
                    "description": "For small office",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "11.png",
                    "category": "pale",
                    "stock_quantity": 45
                },
                {
                    "name": "Clash of clans -m",
                    "price": 14500.89,
                    "description": "For small office downtown",
                    "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
                    "image": "12.png",
                    "category": "pale",
                    "stock_quantity": 3
                }
            ]
        }
    }
}
</script>
  
<style scoped>

</style>