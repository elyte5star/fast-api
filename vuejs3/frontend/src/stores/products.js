import { defineStore } from 'pinia';

import { userAlertStore } from './alert';
import { fetchMethodWrapper } from '@/helpers/methodWrapper';
import Swal from 'sweetalert2/dist/sweetalert2';
const baseURL = process.env.VUE_APP_API_URL + 'products';

export const productStore = defineStore({
    id: 'products',
    state: () => ({
        products: [], product: {}, key: "",
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
            const response = await fetchMethodWrapper.post(baseURL + '/create/review', review);
            if (response["success"]) {
                Swal.fire('Good job!', "Review with ID " + response.rid + " has been created!", 'success');
            } else {
                const alertStore = userAlertStore();
                alertStore.error(response.message);

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
                this.key = key;
                this.products = await fetchMethodWrapper.get(baseURL + '/sort/' + key);

            } catch (error) {
                this.products = { error };
            }

        }

    }

});