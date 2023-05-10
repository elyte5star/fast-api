import { defineStore } from 'pinia';


import { fetchMethodWrapper } from '@/helpers/methodWrapper';

import { userAuthStore } from '@/stores/auth_store'

const baseURL = process.env.VUE_APP_API_URL + 'users';

export const userStore = defineStore({
    id: 'users',
    state: () => ({
        users: [], user: {}
    }),
    actions: {
        async getUsers() {
            try {
                const response = await fetchMethodWrapper.get(baseURL + '/all');
                this.users = response.users;

            } catch (error) {
                this.users = { error };
            }

        },
        async signUP(user) {
            await fetchMethodWrapper.post(baseURL + '/signup', user);
        },
        async getUserById(id) {
            try {
                const response = await fetchMethodWrapper.get(baseURL + '/' + id);
                this.user = response.user;

            } catch (error) {
                this.user = { error };
            }


        },
        async updateUserById(id, new_data) {
            try {
                await fetchMethodWrapper.put(baseURL + '/' + id, new_data);
                const authStore = userAuthStore();
                if (id === authStore.user.userid) {
                    const user = { ...authStore.user, ...new_data };
                    localStorage.setItem('user', JSON.stringify(user));
                }
            } catch (error) {
                this.user = { error };
            }


        },

        async deleteUserAccount(id) {

            await fetchMethodWrapper.delete(baseURL + '/' + id);
            // remove user from list after deleted
            this.users = this.users.filter(x => x.id !== id);
            
            const authStore = userAuthStore();
            if (id === authStore.user.userid) {
                authStore.logout();
            }

        },

    }

});