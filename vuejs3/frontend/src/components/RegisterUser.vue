<template>
    <div>
        <!-- Create user account -->
        <div id="add_entry">
            <div class="close">
                <a href="javascript:void(0)" @click="changeActiveComponent('login_user')"><i class="fa fa-remove"></i></a>
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
                        <input type="text" name="email" id="email_" size="20" />
                    </td>
                </tr>

                <tr>
                    <td>Password:</td>
                    <td>
                        <input type="password" name="pass" id="pass" size="20" minlength="4" required />
                    </td>
                </tr>

                <tr>
                    <td>Confirm Password:</td>
                    <td>
                        <input type="password" name="pass_" id="pass_" size="20" minlength="4" required />
                    </td>
                </tr>

                <tr>
                    <td>Telephone:</td>
                    <td>
                        <input type="text" name="tel" id="tel" size="20" minlength="6" required />
                    </td>
                </tr>
                <tr>
                    <td>
                        <input id="b1" type="button" value="Create Account" v-on:click="registerUser()"
                            style="width: 100%" />
                    </td>
                    <td>
                        <input id="b2" type="button" value="Cancel" v-on:click="changeActiveComponent('login_user')"
                            style="width: 100%" />
                    </td>
                </tr>
            </table>
        </div>

        <div><span id="info"></span></div>
        <!-- the button to Sign up -->
        <button class="form-btn" @click="changeActiveComponent('login_user')" type="button" id="add_p">
            Return to login.
        </button>


    </div>
</template>

<script>

import { is_Input_Error } from '@/helpers/script';
import { userStore } from "@/stores/userAccount";

export default {
    name: 'RegisterUser',
    methods: {
        changeActiveComponent(str) {
            this.$emit('changeActiveComponent', str);
        },
        async registerUser() {
            const userName = document.getElementById("username_").value;
            const email = document.getElementById("email_").value;
            const password1 = document.getElementById("pass").value;
            const passWord2 = document.getElementById("pass_").value;
            const tel = document.getElementById("tel").value;
            if (!is_Input_Error(userName, email, password1, passWord2, tel)) {
                const user = { "username": userName, "email": email, "password": password1, "telephone": tel };
                const user_store = userStore();
                await user_store.signUP(user);
            }

        }
    },
    mounted: function () {
        document.getElementById("username_").value=" ";
        document.getElementById("email_").value=" ";
        document.getElementById("pass").value=" ";
        document.getElementById("pass_").value=" ";
        document.getElementById("tel").value=" ";
    }
}

</script>