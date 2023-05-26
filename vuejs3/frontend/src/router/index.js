import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView'
import LoginView from '../views/LoginView'
import UserView from '../views/UserView'
import CartView from '@/views/CartView'
import NotFound from '@/views/NotFound'
import ProductView from '@/views/ProductView'
import AdminView from '@/views/AdminView'
import { userAuthStore } from '@/stores/auth_store'
import { userAlertStore } from '@/stores/alert'




const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView
  },
  {
    path: '/user/:userid',
    name: 'oneUser',
    component: UserView,
    props: true

  },
  {
    path: '/cart',
    name: 'cart',
    component: CartView
  },
  {
    path: '/product/:pid',
    name: 'oneProduct',
    component: ProductView,
    props: true
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView

  },
  {
    path: "/:catchAll(.*)",
    component: NotFound
  },
  {
    path: "/logout",
    name: "logout",
    component: {
      async beforeRouteEnter(to, from, next) {
        console.log({ from });
        const destination = {
          path: from.path || "/",
          query: from.query,
          params: from.params
        };
        if (!from) {
          console.log("no from");
        }
        console.log("running before hook");
        const auth = userAuthStore();
        await auth.logout();
        next(destination);
      }

    },

  }

]

const router = createRouter({
  history: createWebHistory(process.env.VUE_APP_BASE_URL),
  routes
})

router.beforeEach(async (to) => {

  // clear alert on route change
  const alertStore = userAlertStore();

  alertStore.clear();

  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/', '/cart'];

  const authRequired = !publicPages.includes(to.path);

  const auth = userAuthStore();

  if (authRequired && !auth.user) {
    auth.returnUrl = to.fullPath;
    return { name: 'login' }
  }



});

export default router