<template>
    <div id="user" class="card">
        <img :src="'../images/' + user_image" v-bind:alt="man" style="width:100%">
        <h1></h1>
        <p class="title">{{user.username}}</p>
        <p>Harvard University</p>
        
        <p><button>Update Contact</button></p>
        <!-- the button to Sign up -->
    </div>
    
</template>

<script>

import { userStore } from '@/stores/userAccount';
import { userAuthStore } from '@/stores/auth_store';
import { storeToRefs } from 'pinia';


export default {
    name: 'UserView',
    data(){
        const authStore = userAuthStore();
        const { user } = storeToRefs(authStore);
      return {
        user_image:null,user
      }},
  async created () {
    const user_store = userStore();
    await user_store.getUserById(this.user.userid);
    this.user_image = this.user.admin ? 'admin-icon.png' :'user-icon.png';
  
  },
} 

</script>




<style scoped>
.card {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    max-width: 300px;
    margin: auto;
    text-align: center;
  }
  
  .title {
    color: grey;
    font-size: 18px;
  }
  
  button {
    border: none;
    outline: 0;
    display: inline-block;
    padding: 8px;
    color: white;
    background-color: #000;
    text-align: center;
    cursor: pointer;
    width: 100%;
    font-size: 18px;
  }
  
  a {
    text-decoration: none;
    font-size: 22px;
    color: black;
  }
  
  button:hover, a:hover {
    opacity: 0.7;
  }
    
</style>