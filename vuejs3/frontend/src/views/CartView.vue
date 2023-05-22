
<template>
    <div id="basket">
        <h1>Shopping Cart</h1>

        <div id="cart-items">
            <!-- Add your cart items here -->
        </div>

        <div id="cart-total">
            <!-- Display the total price of the cart here -->
        </div>

        <button class="form-btn" @click="checkOut()" type="button" id="checkout">
            Checkout.
        </button>

    </div>
</template>
<script>
//import { userAuthStore } from '@/stores/auth_store'
export default {
    name: 'CartView',


}
</script>
<style scoped>


#cart-items {
    border: 5px solid #ececec;
}
#checkout:hover {
    background-color: lightgoldenrodyellow;
}


#basket h1 {
    background-color: #BCBCBC;
    color: white;
    padding: 5px;
    font-size: 1.2em;
    margin-top: 5px;
    text-align: center;
}
.contact {
    border-width: 1px 1px 1px 5px;
    border-style: solid;
    border-color: #999999;
    background-color: white;
    padding: 5px;
    margin: 3px;
    position: relative;
    font-family: Verdana, serif;
    font-size: 0.8em;
}

.contact_name {
    font-weight: bold;
}

.contact_details {
    font-size: 0.8em;    
}

.contact_details a, .contact_details a:visited {
    color: blue;
}

.contact_operations {
    width: 1.2em;
    position: absolute;
    text-align: center;
    padding: 3px;
    right: 0;
    top: 0;
}

</style>