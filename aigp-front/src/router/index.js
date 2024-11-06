import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import UserProfileView from '../views/UserProfileView.vue';
import UserListView from '../views/UserListView.vue';
import RegisterView from '../views/RegisterView.vue';
import LoginView from '../views/LoginView.vue';
import ImgEditView from '../views/ImgEditView.vue'
import ImgGenerateView from '../views/ImgGenerateView.vue'
import NotFoundView from '../views/NotFoundView.vue';

import Text2ImgView from '../views/ImgGenerate/Text2ImgView.vue'
import Img2ImgView from '../views/ImgGenerate/Img2ImgView.vue'
import ImgBigView from '../views/ImgGenerate/ImgBigView.vue'

import BaseEditView from '../views/ImgEdit/BaseEditView.vue'
import ImgMattingView from '../views/ImgEdit/ImgMattingView.vue'
import ImgMergeView from '../views/ImgEdit/ImgMergeView.vue'
import ImgCompressView from '../views/ImgEdit/ImgCompressView.vue'

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/userprofile/:userId',
    name: 'userprofile',
    component: UserProfileView
  },
  {
    path: '/userlist',
    name: 'userlist',
    component: UserListView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/404/',
    name: '404',
    component: NotFoundView
  },
  {
    path: '/imgEdit',
    name: 'imgedit',
    component: ImgEditView
  },
  {
    path: '/imggenerate',
    name: 'imggenerate',
    component: ImgGenerateView
  },

  {
    path: '/imggenerate/text2img',
    name: 'text2img',
    component: Text2ImgView
  },

  {
    path: '/imggenerate/img2img',
    name: 'img2img',
    component: Img2ImgView
  },

  {
    path: '/imggenerate/imgbig',
    name: 'imgbig',
    component: ImgBigView
  },

  {
    path: '/imgedit/baseedit',
    name: 'baseedit',
    component: BaseEditView
  },

  {
    path: '/imgedit/imgmatting',
    name: 'imgmatting',
    component: ImgMattingView
  },

  {
    path: '/imgedit/imgmerge',
    name: 'imgmerge',
    component: ImgMergeView
  },

  {
    path: '/imgedit/imgcompress',
    name: 'imgcompress',
    component: ImgCompressView
  },

  {
    path: '/:catchAll(.*)',
    redirect: "/404/"
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  // 在每次路由导航前重置图片状态
  if (!store.state.img.is_PushNavigation) store.commit('resetImgState');
  store.state.img.is_PushNavigation = false;
  next();
});

export default router;
