import { defineStore } from 'pinia';

import Swal from 'sweetalert2/dist/sweetalert2';

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
        returnUrl: null
    }),
    actions: {
        async login(userData) {
            try {

                const response = await postToTokenEndpoint(baseURL + '/token', userData)

                if (response["success"]) {

                    this.user = response.token_data;

                    localStorage.setItem('user', JSON.stringify(response.token_data));

                    return router.push(this.returnUrl || '/');

                } else {
                    return Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                        footer: '<a href="/">Return to home page.</a>'
                    });
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
