<template>
  <div>
    <div>
      <NavBar />
    </div>
    <div>
      <AlertVue />
    </div>
    <router-view />
  </div>
</template>

<script setup>


import AlertVue from '@/components/Alert.vue';
import NavBar from '@/components/Nav.vue'

</script>
