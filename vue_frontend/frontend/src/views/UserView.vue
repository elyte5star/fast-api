<template>
  <div v-if="user" class="user">
    <keep-alive>
      <component :is="activeComponent" :user_info="user_info" :user_image="user_image"
        @changeActiveComponent="_changeActiveComponent" />
    </keep-alive>
  </div>
</template>

<script>
import { userStore } from "@/stores/userAccount";
import { userAuthStore } from "@/stores/auth_store";
import { storeToRefs } from "pinia";
import EditUser from "@/components/EditUser.vue";
import UserProfile from "@/components/UserProfile.vue";

export default {
  name: "UserView",
  components: { EditUser, UserProfile },
  data() {
    const authStore = userAuthStore();
    const { user } = storeToRefs(authStore);
    return {
      activeComponent: UserProfile,
      user_image: null,
      user_info: null,
      user,
    };
  },
  async created() {
    const user_store = userStore();
    await user_store.getUserById(this.user.userid);
    this.user_image = this.user.admin ? "admin-icon.png" : "user-icon.png";
    const { user } = storeToRefs(user_store);
    this.user_info = user;
  },

  methods: {
    _changeActiveComponent(str) {
      if (str === 'update_details') {
        this.activeComponent = EditUser;
        console.log(str);

      } else {
        this.activeComponent = UserProfile;
        console.log(str);

      }

    },
  },
};
</script>

