<template>
  <div class="home">
    <BigIcons />
    <ImageSlide v-bind:products="products" />
    <MainProducts v-bind:products="products" />
    <FooterContact />
  </div>
</template>

<script>
// @ is an alias to /src
import BigIcons from '@/components/BigIcons.vue'
import ImageSlide from '@/components/ImageSlide.vue';
import MainProducts from '@/components/Products.vue'
import FooterContact from '@/components/FooterContact.vue'
import { storeToRefs } from 'pinia';
import { productStore } from '@/stores/products'

export default {
  name: 'HomeView',
  components: {
    BigIcons, ImageSlide, MainProducts, FooterContact
  },
  data() {
    return {
      products: [],

    }
  },

  async created() {
    const pStore = productStore();
    await pStore.getProducts();
    const { products } = storeToRefs(pStore);
    this.products = products;
  
  },

}

</script>

