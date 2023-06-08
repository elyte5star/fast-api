
import { defineStore } from 'pinia';


//Persisting the Cart and cart count
let cart = localStorage.getItem('cart');
let itemsInCart = window.localStorage.getItem('cartCount');

import { fetchMethodWrapper } from '@/helpers/methodWrapper';

const baseURL = process.env.VUE_APP_API_URL + 'booking';

import { userAlertStore } from './alert';


export const userCartStore = defineStore({
    id: 'cart',
    state: () => ({
        cart: cart ? JSON.parse(cart) : [], itemsInCart: itemsInCart ? parseInt(itemsInCart) : 0,
    }),
    actions: {
        addToCart(product, volume) {

            for (let i = 0; i < volume; i++) {
                this.cart.push(product);
            }

            localStorage.setItem('cart', JSON.stringify(this.cart));
            const kart = JSON.parse(localStorage.getItem('cart'));
            this.itemsInCart = kart.length;
            localStorage.setItem('cartCount', JSON.stringify(this.itemsInCart));


        },
        removeFromCart(product) {
            const itemToBeRemoved = product
            this.cart.splice(this.cart.findIndex(a => a.pid === itemToBeRemoved.pid), 1)
            localStorage.setItem('cart', JSON.stringify(this.cart));
            const kart = JSON.parse(localStorage.getItem('cart'));
            this.itemsInCart = kart.length;
            localStorage.setItem('cartCount', JSON.stringify(this.itemsInCart));
        },
        clearCart() {
            while (this.cart.length > 0) {
                this.cart.pop();
            }
            this.itemsInCart = 0;
            this.cart = [];
            localStorage.removeItem('cart');
            localStorage.removeItem('cartCount');

        },
        async checkOut(bookingDetails) {
            const alertStore = userAlertStore();
            const response = await fetchMethodWrapper.post(baseURL + '/create', bookingDetails);
            if (response.success) {
                alertStore.success("<strong> Success! </strong> " + "Booking with id " + response.oid + " created!")
                this.clearCart();

            } else {
                alertStore.error(response.message);

            }

        }
    }
});