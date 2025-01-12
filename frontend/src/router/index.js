import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import RegisterView from '../views/RegisterView.vue'
import PostForm from '../views/PostForm.vue'
import OtherUserInfoView from '../views/OtherUserInfoView.vue'

const routes = [
  {
    path: '/Home',
    name: 'HomeView',
    component: HomeView,
    // meta: { requiresAuth: true }
  },
  {
    path: '/questions/:id',
    name: 'QuestionView',
    component: () => import('../views/QuestionView.vue'),
    // meta: { requiresAuth: true }
  },
  {
    path: '/Post',
    name: 'PostForm',
    component: PostForm,
    // meta: { requiresAuth: true }
  },
  {
    path: '/',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    // meta: { requiresAuth: true }
  },
  {
    path: '/edit',
    name: 'EditProfile',
    component: EditProfileView,
    // meta: { requiresAuth: true }
  },
  {
    path: '/userinfos/:id',
    name: 'UserInfo',
    component: OtherUserInfoView,
    props: true,
    // meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router