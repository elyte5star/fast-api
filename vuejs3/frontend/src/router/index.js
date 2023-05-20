import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import UserView from '../views/UserView'
import NotFound from '@/views/NotFound'
import ProductView from '@/views/ProductView'
import { userAuthStore } from '@/stores/auth_store'
import { userAlertStore } from '@/stores/alert'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/profile',
    name: 'oneUser',
    component: UserView
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
    path: '/:pathMatch(.*)*',
    component: NotFound
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
  const publicPages = ['/login', '/', '/product'];

  const authRequired = !publicPages.includes(to.path);

  const auth = userAuthStore();

  if (authRequired && !auth.user) {
    auth.returnUrl = to.fullPath;
    return { name: 'login' }
  }



});

export default router