<template>
  <div>
    <header>
      <nav>
        <ul v-if="user">
          <li><router-link to="/"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
          <li v-show="user.admin"><router-link :to="{ name: 'admin' }"><i class="fa fa-cogs"></i>Admin page</router-link>
          </li>
          <li><router-link :to="{
            name: 'oneUser', params: {
              userid: user.userid
            }
          }"><i class="fa fa-user-circle" style="font-size: 25px"></i>Logged in as {{ user.username }}</router-link>
          </li>
          <li><a href="javascript:void(0)" v-on:click="authStore.logout()"><i class="fa fa-sign-out"></i>Logout</a></li>
          <li><router-link :to="{ name: 'cart' }"><i class="fa fa-shopping-cart" style="font-size: 25px"></i>Cart<span
                id="items">{{
                  itemsInCart }}</span></router-link></li>
        </ul>
        <ul v-else>
          <li><router-link to="/"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
          <li><router-link to="/login"><i class="fa fa-sign-in"></i>Login</router-link></li>
          <li><router-link :to="{ name: 'cart' }"><i class="fa fa-shopping-cart"
                style="font-size: 25px;color: white;"></i>Cart<span id="items">{{ itemsInCart }}</span></router-link></li>
        </ul>
      </nav>
     
    </header>
    <div>
      <AlertVue />
    </div>
    <router-view />
  </div>
</template>

<script setup>

import { storeToRefs } from 'pinia';

import { userCartStore } from '@/stores/cart'

import { userAuthStore } from './stores/auth_store';

import AlertVue from '@/components/Alert.vue';

const authStore = userAuthStore();
const cartStore = userCartStore();

const { user } = storeToRefs(authStore);

const { itemsInCart } = storeToRefs(cartStore);



</script>
