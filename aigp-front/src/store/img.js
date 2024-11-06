import {modelInputProps} from '@/helpers/interfaces'

const ModuleImg = {
  state: {
    // 全局标志
    is_PushNavigation: false,

    // 原始图像
    id: "",
    image: null,  // new Image()

    // 辅助图像
    clicks: [modelInputProps],
    maskImg: null,
    
    click_list: [modelInputProps],
    stmaskImg: null,  // imgmatting辅助量

    fobImg: null,  // imgmerge辅助量

    originImg: null,  // img2img辅助量

    savetool: null  // 图片保存中介
  },
  getters: {
  },
  mutations: {
    setImgId(state, id) {
      state.id = id;
    },
    setImage(state, image) {
      state.image = image;
      state.click_list = [{x: 0, y: 0, clickType: 0}];
      state.maskImg = null;
    },
    

    setClick(state, clicks) {
      state.clicks = clicks;
    },
    setmaskImg(state, maskImg) {
      state.maskImg = maskImg;
    },

    addClickList(state, click){
      if (state.click_list.length && state.click_list[0].clickType === 0) state.click_list.pop();
      state.click_list.push(click);
    },
    setstmaskImg(state, stmaskImg) {
      state.stmaskImg = stmaskImg;
    },
    clearMatting(state) {
      state.click_list = [{x: 0, y: 0, clickType: 0}];
      state.stmaskImg = null;
    },

    setfobImg(state, fobImg) {
      state.fobImg = fobImg;
    },

    setoriginImg(state, originImg) {
      state.originImg = originImg;
    },

    setsavetool(state, savetool) {
      state.savetool = savetool;
    },

    resetImgState(state) {
      // 原始图像
      state.id = "";
      state.image = null,  // new Image()

      // 辅助图像
      state.clicks = [modelInputProps];
      state.maskImg = null;
      
      state.click_list = [modelInputProps];
      state.stmaskImg = null;

      state.fobImg = null;  // 可做前/后景

      state.originImg = null;

      state.savetool = null;
    }
  },
  actions: {
  },
  modules: {   
  }
}

export default ModuleImg;