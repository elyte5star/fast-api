import { defineStore } from 'pinia';

//import { fetchMethodWrapper } from '@/helpers/methodWrapper';

import { userAlertStore } from './alert';

import { router } from '@/router/index'

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
                
                // update pinia state
                this.user = response.token_data;

                // store user details and jwt in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(response.token_data));

                // redirect to previous url or default to home page
                return router.push(this.returnUrl || '/products');


            } catch (error) {
                const alertStore = userAlertStore();
                alertStore.error(error);
            }
        },
        async logout() {
            try {
                //await fetchMethodWrapper.get(baseURL + '/logout');
                this.user = null;
                localStorage.removeItem('user');
                router.push('/');

            } catch (error) {
                const alertStore = userAlertStore();
                alertStore.error(error);

            }

        }
    }
});
