import { defineStore } from 'pinia';

//import { fetchMethodWrapper } from '@/helpers/methodWrapper';

import { userAlertStore } from './alert';

import router from '@/router/index'

const baseURL = process.env.VUE_APP_API_URL + 'auth';

async function postToTokenEndpoint(url = "", data = {}) {
    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: data // JSON.stringify(data)
    }
    const response = await fetch(url, options);
    return response.json();
}

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

                this.user = response.token_data;

                localStorage.setItem('user', JSON.stringify(response.token_data));

                return router.push(this.returnUrl || '/');


            } catch (error) {
                const alertStore = userAlertStore();
                alertStore.error(error);
            }
        },
        async logout() {

            //await fetchMethodWrapper.get(baseURL + '/logout');
            this.user = null;
            localStorage.removeItem('user');
            router.push('/');


        }
    }
});
