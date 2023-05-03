<template>
  <header>
    <nav>
      <ul v-if="user">
        <li><router-link to="/"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
        <li v-if="user.username =='elyte'"><router-link to="/admin"><i class="fa fa-lock"></i>Manage Users</router-link></li>
        <li><router-link to="javascript:void(0)">Signed in as {{ user.username }}</router-link></li>
        <li><router-link to="javascript:void(0)" v-on:click="authStore.logout()"><i class="fa fa-sign-out"></i>Logout</router-link></li>
        <li><router-link to="/basket"><i class="fa fa-shopping-cart" style="font-size: 25px"></i><span id="items">0</span></router-link></li>
      </ul>
      <ul v-else>
        <li><router-link to="/login"><i class="fa fa-sign-in"></i>Login</router-link></li>
        <li><router-link to="/basket"><i class="fa fa-shopping-cart" style="font-size: 25px;color: white;"></i><span id="items">0</span></router-link></li>
      </ul>
    </nav>
  </header>
  <router-view />
  
</template>

<script setup>

import { storeToRefs } from 'pinia';

import { userAuthStore } from './stores/auth_store';

const authStore = userAuthStore();

const { user } = storeToRefs(authStore);

</script>
