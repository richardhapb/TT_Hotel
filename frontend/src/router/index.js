import { createRouter, createWebHistory } from 'vue-router';


import CustomerLogin from '@/views/CustomerLogin.vue';
import RegisterView from '@/views/RegisterView.vue';
import MainDashboard from '@/views/MainDashboard.vue';
import ResetPassword from '@/views/ResetPassword.vue';
import VerifyEmail from '@/views/VerifyEmail.vue';


const routes = [
  {
    path: '/login',
    name: 'CustomerLogin',
    component: CustomerLogin,
  },
  {
    path: '/',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/customers/password_reset/:token',
    name: 'ResetPassowrd',
    component: ResetPassword,
  },
  {
    path: '/customer/dashboard',
    name: 'Dashboard',
    component: MainDashboard,
    meta: { requiresAuth: true }  
  },
  {
    path: '/email/verify/:token',
    name: 'VerifyEmail',
    component: VerifyEmail,
  }
];


const router = createRouter({
  history: createWebHistory(),  // Esto es para el modo 'history'
  routes,
});


router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Verificar si el usuario está autenticado (cookie refresh_token)
    const isAuthenticated = !!document.cookie.match(/refresh_token/);
    if (!isAuthenticated) {
      next({ name: 'CustomerLogin' });
    } else {
      next();
    }
  } else {
    next(); 
  }
});

export default router;
