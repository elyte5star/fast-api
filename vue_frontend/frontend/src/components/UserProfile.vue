<template>
    <div v-if="user_info">
        <main id="user" class="container">
            <h1>Profile card for {{ user_info.username }}.</h1>
            <article class="framed columnx" id="{{ user.userid }}">
                <div class="close">
                    <a href="javascript:void(0)"><i class="fa fa-trash-o" style="font-size: 30px"></i></a>
                </div>
                <div class="item_left">
                    <img :src="'../images/' + user_image" v-bind:alt="user_info.username" />
                    <div class="discount">Discount : {{ user_info.discount }}%</div>
                </div>
                <div class="item_right">
                    <h3>Username : {{ user_info.username }}</h3>
                    <h5>Telephone : {{ user_info.telephone }}</h5>
                    <h5>Email : {{ user_info.email }}</h5>
                    <h6>User id : {{ user_info.userid }}.</h6>
                    <h6>Registered since {{ formatDate(user_info.created_at) }}.</h6>
                </div>
            </article>
            <button class="form-btn" @click="changeActiveComponent('update_details')" type="button" id="update_p">
                Update User Details.
            </button>
        </main>
    </div>
</template>


<script>
import moment from "moment";


export default {
    name: "UserProfile",
    props: {
        user_info: {
            type: new Object(null),
        },
        user_image: {
            type: String,
        },
    },
    methods: {
        formatDate(value) {
            if (value) {
                return moment(String(value)).format("DD-MM-YYYY hh:mm");
            }
        },
        changeActiveComponent(str){
            this.$emit('changeActiveComponent',str);
        },
    },
};
</script>