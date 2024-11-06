import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

// 引入element plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入Ant Design
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

createApp(App).use(router).use(store).use(ElementPlus).use(Antd).mount('#app')
