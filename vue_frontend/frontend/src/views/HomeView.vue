<template>
  <div class="home">
    <BigIcons />
    <MainProducts/>
    <FooterContact/>
  </div>
</template>

<script>
// @ is an alias to /src
import BigIcons from '@/components/BigIcons.vue'
import MainProducts from '@/components/Products.vue'
import FooterContact from '@/components/FooterContact.vue'

export default {
  name: 'HomeView',
  components: {
    BigIcons, MainProducts,FooterContact
  }
}
</script>
