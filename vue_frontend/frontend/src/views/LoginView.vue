<template>
    <!-- Login panel -->
    <div id="login_access">
        <h2>Login</h2>
        <table>
            <tr>
                <td>Username :</td>
                <td><input type="text" name="username" id="username" size="20" /></td>
                <td rowspan="3">
                    <div class="container" id="g_id">
                        <div class="row justify-content-center">
                            <div class="col">
                                <a @mouseover="hide_add_entry('add_entry')" class="btn btn-outline-dark"
                                    href="javascript:void(0)" onclick="getGoogleToken()" role="button"
                                    style="text-transform:none">
                                    <img :src="'./images/gg.png'" class="google" v-bind:alt="'Google'" />
                                    Login with Google for registered Users
                                </a>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
            <tr>
                <td>Password :</td>
                <td> <input type="password" id="password" name="password" minlength="4" size="20" required></td>
            </tr>
            <tr>
                <td> Login :</td>
                <td><a href="javascript:void(0)" v-on:click="login()"><i class="fa fa-sign-in"
                            style="font-size:60px;"></i></a></td>
            </tr>
        </table>
    </div>
    <!-- Create user account -->
    <div id="add_entry" style="display: none">
        <div class="close">
            <a href="javascript:void(0)" @click="hide_add_entry('add_entry');"><i class="fa fa-remove"></i></a>
        </div>
        <h2>Please Create A User Account</h2>
        <table>
            <tr>
                <td>Username:</td>
                <td>
                    <input type="text" name="username_" id="username_" size="20" />
                </td>
            </tr>

            <tr>
                <td>Email:</td>
                <td>
                    <input type="text" name="email_" id="email_" size="20" />
                </td>
            </tr>

            <tr>
                <td>Password:</td>
                <td>
                    <input type="password" name="pass" id="pass" size="20" minlength="4" required>
                </td>
            </tr>

            <tr>
                <td>Confirm Password:</td>
                <td>
                    <input type="password" name="pass_" id="pass_" size="20" minlength="4" required>
                </td>
            </tr>

            <tr>
                <td>Telephone:</td>
                <td>
                    <input type="text" name="tel" id="tel" size="20" minlength="6" required>
                </td>
            </tr>
            <tr>
                <td>
                    <input id="b1" type="button" value="Create Account" v-on:click=" signUP(); " style="width: 100%" />
                </td>
                <td>
                    <input id="b2" type="button" value="Cancel" v-on:click=" hide_add_entry('add_entry'); "
                        style="width: 100%" />
                </td>
            </tr>
        </table>

    </div>

    <div><span id="info"></span></div>

    <!-- the button to Sign up -->
    <button class="form-btn" @click=" show_add_entry('add_entry') " role="link" type="button" id="add_p">Please, create a
        User
        Account.</button>
</template>
<script>

import { userAuthStore } from '@/stores/auth_store';


export default {
    name: 'LoginView',
    methods: {
        async login() {
            let userName = document.getElementById("username").value;
            let passWord = document.getElementById("password").value;

            if (userName != "" || passWord != "") {

                let form = new FormData();
                form.append("username", userName);
                form.append("password", passWord);
                const userData = new URLSearchParams();

                for (const pair of form) {
                    userData.append(pair[0], pair[1]);
                }
                const authStore = userAuthStore();
                await authStore.login(userData);

            } else {
                document.getElementById("info").innerHTML = "<strong>Wrong!</strong> " + " Empty fields!";
            }

        },
        show_add_entry(id) {
            let element = document.getElementById(id);
            element.style.display = "";

        },
        hide_add_entry(id) {
            let element = document.getElementById(id);
            element.style.display = "none";
        }


    }

}
</script>