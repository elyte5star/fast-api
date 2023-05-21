<template>
    <div>
        <!-- Login panel -->
        <div id="login_access">
            <h2>Login</h2>
            <table>
                <tr>
                    <td>Username :</td>
                    <td><input type="text" placeholder='username' name="username" id="username" size="20" /></td>
                    <td rowspan="3">
                        <div class="container" id="g_id">
                            <div class="row justify-content-center">
                                <div class="col">
                                    <a id:="google_img" class="btn btn-outline-dark" href="javascript:void(0)"
                                        @click="getGoogleToken()" role="button" style="text-transform: none">
                                        <img :src="'./images/gg.png'" class="google" v-bind:alt="'Google'" />
                                        Login with Google
                                    </a>
                                    <a id:="msoft" class="btn btn-outline-dark" href="javascript:void(0)" @click="MToken()"
                                        role="button" style="text-transform: none">
                                        <img :src="'./images/microsoft.png'" class="microsoft" v-bind:alt="'microsoft'" />
                                        Login with Microsoft
                                    </a>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>Password :</td>
                    <td>
                        <input placeholder='password' type="password" @keyup.enter='login()' id="password" name="password"
                            minlength="4" size="20" required />
                    </td>
                </tr>
                <tr>
                    <td>Login :</td>
                    <td>
                        <a href="javascript:void(0)" v-on:click="login()"><i class="fa fa-sign-in"
                                style="font-size: 60px"></i></a>
                    </td>
                </tr>
            </table>
        </div>
        <button class="form-btn" @click="changeActiveComponent('register_user')" type="button" id="add_p">
            Please, create a User Account.
        </button>
    </div>
</template>

<script>

import { userAuthStore } from "@/stores/auth_store.js";
import { isUserNameValid } from "@/helpers/script";

export default {
    name: 'LoginUser',
    methods: {

        changeActiveComponent(str) {
            this.$emit('changeActiveComponent', str);
        },
        async login() {
            const userName = document.getElementById("username").value;
            const passWord = document.getElementById("password").value;
            if ((userName == null || userName == "") && (passWord == null || passWord == "")) {

                this.$swal("<strong>Wrong!</strong> " + "Please Fill In All Required Fields!");

                return false;

            } else if (!isUserNameValid(userName)) {

                this.$swal("<strong>Wrong!</strong> " + "Invalid Username!");
                return false;

            } else {

                let form = new FormData();
                form.append("username", userName);
                form.append("password", passWord);
                const userData = new URLSearchParams();

                for (const pair of form) {
                    userData.append(pair[0], pair[1]);
                }
                const authStore = userAuthStore();
                await authStore.login(userData);
            }

        },
        

    },


}

</script>