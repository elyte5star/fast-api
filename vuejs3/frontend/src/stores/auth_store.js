import { defineStore } from 'pinia';


import { userAlertStore } from './alert';

import router from '@/router/index'

import { fetchMethodWrapper } from '@/helpers/methodWrapper';

import { postToTokenEndpoint } from "@/helpers/script.js";

const baseURL = process.env.VUE_APP_API_URL + 'auth';

export const userAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user')),
        returnUrl: null,
        cart: [], itemsInCart: 0
    }),
    actions: {

        addToCart(pid, volume) {

            for (let i = 1; i < volume; i++) {
                this.cart.unshift(pid);

            }
            this.cart.unshift(pid);
            this.itemsInCart = this.cart.length;
            console.log(volume, this.cart);

        },
        removeFromCart(pid) {
            const index = this.cart.indexOf(pid);
            if (index > -1) {
                this.cart.splice(index, 1);
                this.itemsInCart = this.cart.length;
            }

        },
        clearCart() {
            while (this.cart.length > 0) {
                this.cart.pop();
            }
            this.itemsInCart = 0;
        },
        async login(userData) {
            try {

                const response = await postToTokenEndpoint(baseURL + '/token', userData)

                if (response["success"]) {

                    this.user = response.token_data;

                    localStorage.setItem('user', JSON.stringify(response.token_data));

                    return router.push(this.returnUrl || '/');

                }

            } catch (error) {
                const alertStore = userAlertStore();
                alertStore.error(error);
            }
        },
        async logout() {

            const response = await fetchMethodWrapper.get(baseURL + '/logout');

            if (response.success) {
                this.user = null;
                localStorage.removeItem('user');
                router.push('/');

            } else {

                this.user = null;
                localStorage.removeItem('user');
                const alertStore = userAlertStore();
                alertStore.error(response.message);

            }

        }
    }
});
