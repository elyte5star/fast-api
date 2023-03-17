<template>
  <div class="about">
    <h1>Products</h1>
    <article class="framed column" v-for="product in products" v-bind:key="product">
      <div class="prod_left">
        <img :src="'../images/products/' + product.image" v-bind:alt="product.name">
        <div class="place">{{ product['category'] }}</div>
      </div>

      <div class="prod_right">
        <h3>{{ product.name }}</h3>
        <p>{{ product.description }}</p>
        <h4 v-if="product.discount"><span style="text-decoration: line-through;">{{ product['price'] }} Kr.</span>{{
          product.discount[0]["new_price"] }} Kr.</h4>
        <h4 v-else>{{ product['price'] }} Kr.</h4>
      </div>
      <a href="{{ url_for('one_product', pid=product.pid) }}">
        <div class="details">Details</div>
      </a>

    </article>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      products: [
        {
          "name": "Angry Bird-l",
          "price": 100.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.The word ergonomic gets tossed around like it's the star ingredient in a wellness-word salad. We ourselves are guilty of blindly buying into products that are stamped with its body-support seal of approval — especially now that we're stuck at home in a make-shift office",
          "image": "1.png",
          "category": "black"
        },
        {
          "name": "Angry Bird-i",
          "price": 500.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "2.png",
          "category": "yellow"
        },
        {
          "name": "Angry Bird-w",
          "price": 900.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "3.png",
          "category": "grey"
        },
        {
          "name": "Angry Bird",
          "price": 900.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "4.png",
          "category": "red"
        },
        {
          "name": "Clash of clans-v",
          "price": 1000.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "5.png",
          "category": "pink"
        },
        {
          "name": "Clash of clans-a",
          "price": 700.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "6.png",
          "category": "coal"
        },
        {
          "name": "Clash of clans-q",
          "price": 8900.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "7.png",
          "category": "rock"
        },
        {
          "name": "Clash of clans-r",
          "price": 1300.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "8.png",
          "category": "mat"
        },
        {
          "name": "Super Mario",
          "price": 5800.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "9.png",
          "category": "pale"
        },
        {
          "name": "Clash of clans-o",
          "price": 1200.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "10.png",
          "category": "pale"
        },
        {
          "name": "Clash of clans-n",
          "price": 10000.89,
          "description": "For small office",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "11.png",
          "category": "pale"
        },
        {
          "name": "Clash of clans -m",
          "price": 14500.89,
          "description": "For small office downtown",
          "details": "Ergonomic product for small office.Ahead, a shopping guide we hope will make your at-home office feel less makeshift and more professionally aligned — broken down by what each ergonomic item is supporting, backed by people who actually felt supported by it",
          "image": "12.png",
          "category": "pale"
        }
      ]
    }
  }
}
</script>

<style scoped>
img {
  height: 200px;
  width: 200px;
}

/** product **/
.prod_left {
  width: 200px;
  float: left;
}

.prod_right {
  float: none;
  /* just to make it clear */
  padding-left: 10px;
  width: auto;
  overflow: hidden;
  height: auto;
}

article .details {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 50px;
  background-color: #3299BB;
  padding: 5px;
  text-align: center;
  font-weight: bold;
  color: #E9E9E9;
  border: 1px solid white;
  outline: 1px solid #BCBCBC;
}

.framed {
  border: 3px solid #E9E9E9;
  padding: 5px;
  margin-bottom: 10px;
  position: relative;
  height: auto;
  overflow: hidden;
  font-size: 0.8em;
}

.column {
  width: 32%;
  /* set the amount of columns */
  margin: 0.5%;
  float: left;
}

article .details:hover {
  background-color: #FF9900;
}

article:hover {
  background-color: lightgoldenrodyellow;
}

article h3 {
  margin: 0;
}

.place {
  position: absolute;
  left: 5px;
  bottom: 8px;
  width: 200px;
  /* width of the image */
  z-index: 1;
  background-color: #E9E9E9;
  opacity: 0.7;
  text-align: center;
}
</style>