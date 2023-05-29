<template>
  <div v-if="user" class="user">
    <keep-alive>
      <component :is="activeComponent" :user_info="user" :user_image="user_image"
        @changeActiveComponent="_changeActiveComponent" />
    </keep-alive>
  </div>
</template>

<script>
import { userStore } from "@/stores/userAccount";
import { storeToRefs } from "pinia";
import EditUser from "@/components/EditUser.vue";
import UserProfile from "@/components/UserProfile.vue";

export default {
  name: "UserView",
  components: { EditUser, UserProfile },
  props: {
    userid: {
      type: String,
    }
  },
  data() {

    return {
      activeComponent: UserProfile,
      user_image: null,
      user: new Object(null),
    };
  },
  async created() {
    const user_store = userStore();
    await user_store.getUserById(this.userid);
    const { user } = storeToRefs(user_store);
    this.user = user;
    this.user_image = this.user.admin ? "admin-icon.png" : "user-icon.png";

  },

  methods: {
    _changeActiveComponent(str) {
      if (str === 'update_details') {
        this.activeComponent = EditUser;

      } else {
        this.activeComponent = UserProfile;


      }

    },
  },
};
</script>

