import { defineStore } from 'pinia';

import { userAlertStore } from './alert';
import { fetchMethodWrapper } from '@/helpers/methodWrapper';

const baseURL = process.env.VUE_APP_API_URL + 'products';


export const productStore = defineStore({
    id: 'products',
    state: () => ({
        products: [], product: {}, key: "", reviews: [], quantity: 0, productRecommendations:[]
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
        async submitReview(review) {
            const alertStore = userAlertStore();
            const response = await fetchMethodWrapper.post(baseURL + '/create/review', review);
            if (response["success"]) {
                alertStore.success('Good job!' + " Yor review has been saved!");
            } else {
                alertStore.error(response.message);

            }
        },
        async getProductById(pid) {
            const response = await fetchMethodWrapper.get(baseURL + '/' + pid);
            if (response["success"]) {
                this.product = response.product;
                this.quantity = response.product.stock_quantity;
                this.reviews = response.product.reviews

            } else {
                const alertStore = userAlertStore();
                alertStore.error(response.message);
            }

        },
        async deleteProductById(id) {
            await fetchMethodWrapper.delete(baseURL + '/' + id);

        },

        async sortProductsBykey(key) {
            try {
                this.key = key;
                this.products = await fetchMethodWrapper.get(baseURL + '/sort/' + key);

            } catch (error) {
                this.products = { error };
            }

        }

    }

});