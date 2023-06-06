<template>
    <div id="slide_image">
        <transition-group name="fade" tag="div">
            <div v-for="i in [currentIndex]" :key="i">
                <router-link v-if="currentPid" :to="{
                    name: 'oneProduct',
                    params: {
                        pid: currentPid
                    }
                }"><img v-if="currentImg !== null" :src="'../images/products/' + currentImg" v-bind:alt="currentImg" />
                </router-link>
            </div>
        </transition-group>
        <a class="prev" @click="prev" href="#">&#10094; Previous</a>
        <a class="next" @click="next" href="#">Next &#10095;</a>

    </div>
</template>
<script>

export default {
    name: 'ImageSlide',
    props: {
        products: {
            type: Array,
        }
    },

    data() {
        return {
            timer: null, currentIndex: 0
        }
    },
    methods: {
        startSlide: function () {
            this.timer = setInterval(this.next, 4000);
        },

        next: function () {
            this.currentIndex += 1;
        },
        prev: function () {
            this.currentIndex -= 1;
        }
    },
    computed: {
        currentImg: function () {
            return this.images[Math.abs(this.currentIndex) % this.images.length];
        },
        currentPid: function () {
            return this.pids[Math.abs(this.currentIndex) % this.pids.length];
        },
        images: function () {
            let imgList = [];
            for (let product of this.products) {
                imgList.push(product.image)
            }
            return imgList

        },
        pids: function () {
            let pidList = [];
            for (let product of this.products) {
                pidList.push(product.pid)
            }
            return pidList

        },
        
    },
    mounted() {
        this.startSlide();

    },


}

</script>
<style scoped>
#slide_image img {
    width: 300px;
    height: 200px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}


.fade-enter-active,
.fade-leave-active {
    transition: all 0.9s ease;

}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateX(30px);
}

.fade-leave-active {
    position: absolute;
}


.prev,
.next {
    cursor: pointer;
    position: absolute;
    top: 20%;
    width: auto;
    padding: 16px;
    color: #3299BB;
    font-weight: bold;
    font-size: 18px;
    transition: 0.7s ease;
    border-radius: 0 4px 4px 0;
    text-decoration: none;
    user-select: none;
}

.next {
    right: 0;
}

.prev {
    left: 0;
}

.prev:hover,
.next:hover {
    background-color: #FF9900;
}
</style>