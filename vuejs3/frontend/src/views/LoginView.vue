<template>
    <div>
        <keep-alive>
            <component :is="activeComponent" @changeActiveComponent="_changeActiveComponent" />
        </keep-alive>
    </div>
</template>

<script>

import LoginUser from '@/components/LoginUser.vue'
import RegisterUser from '@/components/RegisterUser.vue'

export default {
    name: "LoginView",
    components: { LoginUser, RegisterUser },
    data() {
        return {
            activeComponent: LoginUser,

        }
    },
    methods: {
        _changeActiveComponent(str) {
            if (str === 'register_user') {
                this.activeComponent = RegisterUser;

            } else {
                this.activeComponent = LoginUser;

            }

        },
    },
};
</script>