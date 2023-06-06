<template>
    <div id="admin">
        <div v-if="user.admin">
            <h1>Hi {{ user.username }}!</h1>
            <p>You're logged in as a superuser!</p>
            <p><router-link to="/users">Manage Users</router-link></p>
        </div>
    </div>
</template>

<script setup>

import { storeToRefs } from 'pinia';
import { userAuthStore } from '@/stores/auth_store';
const authStore = userAuthStore();
const { user } = storeToRefs(authStore);



</script>