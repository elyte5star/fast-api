<template>
    <div>
        <header>
            <nav>
                <ul v-if="user">
                    <li v-show="greeting"><router-link :to="{ name: 'Home' }" id="greeting" v-html="greeting"></router-link>
                    </li>
                    <li><router-link :to="{ name: 'Home' }"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
                    <li v-show="user.admin"><router-link :to="{ name: 'Admin' }"><i class="fa fa-cogs"></i>Admin
                            page</router-link>
                    </li>
                    <li><router-link :to="{
                        name: 'oneUser', params: {
                            userid: user.userid
                        }
                    }"><i class="fa fa-user-circle" style="font-size: 25px"></i>Logged in as {{ user.username
}}</router-link>
                    </li>
                    <li><a href="javascript:void(0)" v-on:click="logout()"><i class="fa fa-sign-out"></i>Logout</a></li>
                    <li><router-link :to="{ name: 'Cart' }"><i class="fa fa-shopping-cart"
                                style="font-size: 25px"></i>Cart<span id="items">{{
                                    itemsInCart }}</span></router-link></li>
                </ul>
                <ul v-else>
                    <li v-show="greeting"><router-link :to="{ name: 'Home' }" id="greeting" v-html="greeting"></router-link>
                    </li>
                    <li><router-link :to="{ name: 'Home' }"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
                    <li><router-link :to="{ name: 'Login' }"><i class="fa fa-sign-in"></i>Login</router-link></li>
                    <li><router-link :to="{ name: 'Cart' }"><i class="fa fa-shopping-cart"
                                style="font-size: 25px;color: white;"></i>Cart<span id="items">{{ itemsInCart
                                }}</span></router-link></li>
                </ul>
            </nav>
        </header>


    </div>
</template>
<script>

import { storeToRefs } from 'pinia';

import { userCartStore } from '@/stores/cart'

import { userAuthStore } from '@/stores/auth_store';

import { greet } from '@/helpers/script';





export default {
    name: 'NavBar',
    data() {
        return {
            user: null, itemsInCart: 0, authStore: userAuthStore(), cartStore: userCartStore()
        }
    },
    methods: {
        logout() {
            this.authStore.logout();
        },
    },
    mounted() {
        const { user } = storeToRefs(this.authStore);
        const { itemsInCart } = storeToRefs(this.cartStore);
        this.user = user
        this.itemsInCart = itemsInCart

    },
    computed: {
        greeting() {
            return greet();
        }

    }


}

</script>