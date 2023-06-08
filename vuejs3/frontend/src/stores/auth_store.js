import { defineStore } from 'pinia';



import { userAlertStore } from './alert';

import router from '@/router/index'

import { postToTokenEndpoint } from "@/helpers/script.js";

const baseURL = process.env.VUE_APP_API_URL + 'auth';

export const userAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user')),
        returnUrl: null,
    }),
    actions: {

        async login(userData) {


            const response = await postToTokenEndpoint(baseURL + '/token', userData)

            if (response["success"]) {

                this.user = response.token_data;

                localStorage.setItem('user', JSON.stringify(response.token_data));

                return router.push(this.returnUrl || '/');

            } else {
                const alertStore = userAlertStore();
                alertStore.error(response.message);
            }
        },
        logout() {
            this.user = null;
            localStorage.removeItem('user');
            router.push('/login');
        }

    }
});
