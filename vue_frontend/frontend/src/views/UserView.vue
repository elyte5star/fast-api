<template>
    <div id="user" class="card">
        <img src="img.jpg" alt="John" style="width:100%">
        <h1>John Doe</h1>
        <p class="title">CEO & Founder, Example</p>
        <p>Harvard University</p>
        <a href="#"><i class="fa fa-dribbble"></i></a>
        <a href="#"><i class="fa fa-twitter"></i></a>
        <a href="#"><i class="fa fa-linkedin"></i></a>
        <a href="#"><i class="fa fa-facebook"></i></a>
        <p><button>Update Contact</button></p>
        <!-- the button to Sign up -->
    <button class="form-btn" @click=" showHistory('history') " type="button" id="add_p">Shopping History.</button>
    </div>
    </div>
</template>

<script>

import { userStore } from '@/stores/userAccount';


export default {
    name: 'UserView',
    methods: {
        async updateUser() {
            console.log("Hello");

        }
    }

}
</script>