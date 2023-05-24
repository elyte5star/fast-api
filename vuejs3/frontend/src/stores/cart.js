import { defineStore } from 'pinia';

import Swal from 'sweetalert2/dist/sweetalert2';

import router from '@/router/index'
import { userAlertStore } from './alert';

import { storeToRefs } from 'pinia';

//Persisting the Cart and cart count
let cart = localStorage.getItem('cart');
let itemsInCart = window.localStorage.getItem('cartCount');

import { fetchMethodWrapper } from '@/helpers/methodWrapper';

const baseURL = process.env.VUE_APP_API_URL + 'booking';

import { userAuthStore } from '@/stores/auth_store'



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
        async checkOut(cart) {
            if (cart) {
                try {
                    const response = await fetchMethodWrapper.post(baseURL + '/create', cart);

                    Swal.fire("<strong> Success! </strong> " + "Booking with id " + response.oid + " created!");
                    this.clearCart();

                } catch (error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Operation not successful!!',
                        confirmButtonText: 'Home',
                        footer: '<a href="/">Continue Shopping.</a>'
                    })
                    const alertStore = userAlertStore();
                    alertStore.error(error);
                }

            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Cart is empty!!',
                    confirmButtonText: 'Home',
                    footer: '<a href="/">Continue Shopping.</a>'
                }).then((result) => {
                    if (result.value) {
                        const auth = userAuthStore();
                        const { returnUrl } = storeToRefs(auth);
                        return router.push(returnUrl || '/');
                    }
                });

            }


        }
    }
});