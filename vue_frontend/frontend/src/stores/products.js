import { defineStore } from 'pinia';


import { fetchMethodWrapper } from '@/helpers/methodWrapper';

const baseURL = process.env.VUE_APP_API_URL + 'products';

export const productStore = defineStore({
    id: 'products',
    state: () => ({
        products: [], product: {}, key: ""
    }),
    actions: {
        async getProducts() {
            try {
                const response = await fetchMethodWrapper.get(baseURL);
                this.products = response.products;
            
            } catch (error) {
                this.products = { error };
            }

        },
        async getProductById(id) {
            try {
                const response = await fetchMethodWrapper.get(baseURL + '/' + id);
                this.product = response.product;

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