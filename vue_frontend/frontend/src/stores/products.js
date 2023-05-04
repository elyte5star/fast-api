import { defineStore } from 'pinia';


import { fetchMethodWrapper } from '@/helpers/methodWrapper';

const baseURL = process.env.VUE_APP_API_URL + 'products';

export const productStore = defineStore({
    id: 'products',
    state: () => ({
        products: {}, product: {}
    }),
    actions: {
        async getProducts() {
            try {
                this.products = await fetchMethodWrapper.get(baseURL);

            } catch (error) {
                this.products = { error };
            }

        },
        async getProductById(id) {
            try {
                this.product = await fetchMethodWrapper.get(baseURL + '/' + id);

            } catch (error) {
                this.product = { error };
            }


        },
        async deleteProductById(id) {
            await fetchMethodWrapper.delete(baseURL + '/' + id);

        },
        async sortProductsBykey(key) {
            try {
                this.products = await fetchMethodWrapper.get(baseURL + '/sort/' + key);

            } catch (error) {
                this.products = { error };
            }

        }

    }

});