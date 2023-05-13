<template>
  <div v-if="user">
    <main id="user" class="container">
      <h1>Profile card for {{ user.username }}.</h1>
      <article class="framed columnx" id="{{ user.userid }}">
        <div class="close">
          <a href="javascript:void(0)" @click="hide_delete_entry('modify_entry')"
            ><i class="fa fa-trash-o" style="font-size:30px;text-shadow: 2px 2px 2px #aaa;"></i
          ></a>
        </div>
        <div class="item_left">
          <img :src="'../images/' + user_image" v-bind:alt="user.name" />
          <div class="customer_id">{{ user.userid }}</div>
        </div>
        <div class="item_right">
          <h3>{{ user.username }}</h3>
          <h5>{{ user.email }}</h5>
          <p>Registered since {{ formatDate(user.created_at) }}.</p>
          <h4>user id : {{ user.userid }}.</h4>
        </div>
      </article>
      <button
        class="form-btn"
        @click="modify('modify_entry')"
        type="button"
        id="update_p"
      >
        Update User Details.
      </button>
    </main>
  </div>
</template>

<script>
import { userStore } from "@/stores/userAccount";
import { userAuthStore } from "@/stores/auth_store";
import { storeToRefs } from "pinia";
import moment from "moment";

export default {
  name: "UserView",
  data() {
    const authStore = userAuthStore();
    const { user } = storeToRefs(authStore);
    return {
      user_image: null,
      user,
    };
  },
  async created() {
    const user_store = userStore();
    await user_store.getUserById(this.user.userid);
    this.user_image = this.user.admin ? "admin-icon.png" : "user-icon.png";
  },
  methods: {
    formatDate(value) {
      if (value) {
        return moment(String(value)).format("DD-MM-YYYY hh:mm");
      }
    },
  },
};
</script>

