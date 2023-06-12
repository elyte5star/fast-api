<template>
    <div v-if="alert" class="container">
        <div class="m-3">
            <div :class="'alert alert-dismissable  fade show ' + alert.type" role=alert >
                <strong>Error !</strong> {{ alert.message }}
                <button @click="alertstore.clear()" class="btn btn-link close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>

import { storeToRefs } from 'pinia';
import { userAlertStore } from '@/stores/alert'


export default {
    name: 'AlertVue',
    data() {
        return {
            alert: null, alertstore: null
        }
    },
    mounted() {
        const alertStore = userAlertStore();
        this.alertstore = alertStore
        const { alert } = storeToRefs(alertStore);
        this.alert = alert;

    },

}

</script>


