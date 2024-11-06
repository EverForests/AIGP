import { createStore } from 'vuex';
import ModuleUser from './user';
import ModuleImg from './img';

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    user: ModuleUser,
    img: ModuleImg,
  }
})
