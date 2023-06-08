<template>
    <div>
        <div v-if="user_info" id="update_entry">
            <div class="close">
                <a href="javascript:void(0)" @click="changeActiveComponent('user_details')"><i class="fa fa-remove"></i></a>
            </div>
            <h2>Please Modify Account Details</h2>
            <table>
                <tr>
                    <td>Username:</td>
                    <td>
                        <input type="text" name="username_" id="mod_username" size="20" />
                    </td>
                </tr>

                <tr>
                    <td>Email:</td>
                    <td>
                        <input type="text" name="email_" id="mod_email" size="20" />
                    </td>
                </tr>

                <tr>
                    <td>Password:</td>
                    <td>
                        <input type="password" name="pass" id="mod_pass" size="20" minlength="4" required />
                    </td>
                </tr>

                <tr>
                    <td>Confirm Password:</td>
                    <td>
                        <input type="password" name="pass_" id="mod_pass_" size="20" minlength="4" required />
                    </td>
                </tr>

                <tr>
                    <td>Telephone:</td>
                    <td>
                        <input type="text" name="tel" id="mod_tel" size="20" minlength="6" required />
                    </td>
                </tr>
                <tr>
                    <td>
                        <input id="b1" type="button" value="Modify Details" v-on:click="updateDetails(user_info.userid)"
                            style="width: 100%" />
                    </td>
                    <td>
                        <input id="b2" type="button" value="Cancel" v-on:click="changeActiveComponent('user_details')"
                            style="width: 100%" />
                    </td>
                </tr>
            </table>
        </div>
        <button class="form-btn" @click="deleteUser(user_info.userid)" type="button" id="delete_user">
            Delete Account.
        </button>

    </div>
</template>

<script>

import { userStore } from "@/stores/userAccount";


export default {
    name: 'EditUser',
    props: {
        user_info: {
            type: Object,
        }
    },
    methods: {
        changeActiveComponent(str) {
            this.$emit('changeActiveComponent', str);
        },
        async updateDetails(id) {
            this.$swal('Hello Vue world!!!');
            console.log(id);
        },
        async deleteUser(id) {
            const user_store = userStore();
            await user_store.deleteUserAccount(id);

        }

    },
    mounted() {
        document.getElementById("mod_username").value = this.user_info.username;
        document.getElementById("mod_tel").value = this.user_info.telephone;
        document.getElementById("mod_email").value = this.user_info.email;
    },

}
</script>