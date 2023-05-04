<template>
  <div class="home">
    <BigIcons />
    <MainProducts />
    <FooterContact />
  </div>
</template>

<script>

// @ is an alias to /src
import BigIcons from '@/components/BigIcons.vue'
import MainProducts from '@/components/Products.vue'
import FooterContact from '@/components/FooterContact.vue'

import { productStore } from '@/stores/products'
import { storeToRefs } from 'pinia';

const prodStore = productStore()

const products = storeToRefs(prodStore)

export default {
  name: 'HomeView',
  components: {
    BigIcons, MainProducts, FooterContact
  },
  data() {
    return {
      products: products.products
    }
  }

};
</script>
