<template>
    <a-layout class="layout">
        <a-layout-sider :style="siderStyle">
            <div v-if="has_input">
                当前处理图片：
                <img :src="img.src" alt="" style="width: 100%;">
                <a-button @click="resetImg">重新上传图片</a-button>
            </div>

            <ImgUpload v-if="!has_input" style="width: 100%;" @uploadImage="uploadImage" />
        </a-layout-sider>

        <a-layout-content :style="contentStyle">
            <a-breadcrumb style="margin: 16px 0">
                <a-breadcrumb-item>
                    <router-link class="nav-link" :to="{ name: 'home' }">首页</router-link>
                </a-breadcrumb-item>

                <a-breadcrumb-item>
                    <router-link class="nav-link" :to="{ name: 'imgedit' }">图像编辑</router-link>
                </a-breadcrumb-item>

                <a-breadcrumb-item>
                    <router-link class="nav-link" :to="{ name: 'imgmatting' }">图像抠取</router-link>
                </a-breadcrumb-item>
            </a-breadcrumb>

            <div style="min-height: 70vh; background-color: gray;">
                <Tool v-if="has_input" class="img-show" :img="img" @handleMouseMove="handleMouseMove"
                    @handleClick="handleClick" @mattingSelect="mattingSelect" @resetMattingSelect="resetMattingSelect"
                    @getmaskImg="getmaskImg" :caputure_status="caputure_status" />
            </div>
            <div>
                <MattingShow class="matting-show" v-if="show_matting" />
            </div>
        </a-layout-content>

        <a-layout-sider :style="siderStyle">

        </a-layout-sider>
    </a-layout>
</template>

<script>
import Tool from '@/components/Tool.vue';
import ImgUpload from './ImgUpload.vue';
import MattingShow from '@/components/MattingShow.vue'
import { useStore } from 'vuex'
import * as underall from 'underscore'

import '@/App.scss'
import { InferenceSession, Tensor } from 'onnxruntime-web'
import { handleImageScale } from '@/helpers/scaleHelpers'
import { modelScaleProps } from '@/helpers/interfaces'
import { onnxMaskToImage } from '@/helpers/maskUtils'
import { modelData } from '@/helpers/onnxModelAPI'

import * as ort from 'onnxruntime-web'
import { ref, onMounted, watch } from 'vue'
import $ from 'jquery'
import * as tf from '@tensorflow/tfjs';

export default {
    name: "Stage",
    components: {
        ImgUpload,
        Tool,
        MattingShow,
    },
    setup() {
        const store = useStore();

        const img = new Image();  // canvas展示图片的信息

        // 接收已经存在的img.image
        const has_input = ref(false);
        if (store.state.img.image) {
            img.onload = function () {
                has_input.value = true;
            }
            img.src = store.state.img.image.src;
        }

        // 如果不存在，则上传图片后更新
        const uploadImage = () => {
            if (!store.state.img.image) return;
            img.onload = function () {
                has_input.value = true;
            }
            img.src = store.state.img.image.src;
        }

        // 重新上传图片
        const resetImg = () => {
            // 优先调整标志位
            has_input.value = false;
            show_matting.value = false;

            store.state.img.image = null;  // 同步操作
            img.src = "";
        }

        /**
        * 获取鼠标位置并将(x, y)坐标缩放回原始图像的比例。\
        * 使用setClicks更新点击状态， 并通过useEffect ，触发ONNX模型运行生成一个新的mask
        */
        let show_matting = ref(false);

        const xhandleMouseMove = p => {
            console.log('handleMouseMove');
            const click = p;
            console.log(click);
            if (click) store.commit('setClick', [click]);
        }

        const handleMouseMove = p => {
            underall.throttle(xhandleMouseMove(p), 15);
        }

        const handleClick = p => {
            const click = p;
            if (click) store.commit('addClickList', click);
        }

        const mattingSelect = async e => {
            // 生成选择位置的掩膜
            console.log(store.state.img.click_list);
            await runONNX(1);  // 采用多点选择

            if (store.state.img.stmaskImg) show_matting.value = true;
        }

        const resetMattingSelect = async e => {
            store.commit('clearMatting');
            show_matting.value = false;
        }

        // 配置onnxruntime
        ort.env.debug = true;
        ort.env.logLevel = 'verbose';
        // // Enable proxy worker
        // ort.env.wasm.proxy = true;

        ort.env.wasm.numThreads = 2;
        ort.env.wasm.simd = true;

        // Set the WebAssembly binary file path to jsdelivr CDN for a specific release version
        ort.env.wasm.wasmPaths = {
            'ort-wasm.wasm': '/ort-wasm..wasm',
            'ort-wasm-simd.wasm': '/ort-wasm-simd..wasm',
            'ort-wasm-threaded.wasm': '/ort-wasm-threaded..wasm',
            'ort-wasm-simd-threaded.wasm': '/ort-wasm-simd-threaded..wasm',
        };

        const MODEL_DIR = '/sam_onnx_quantized_example.onnx';

        const model = ref(null);
        const tensor = ref(null);
        // The modelScale state variable keeps track of the scale values.
        const modelScale = ref(modelScaleProps);
        const caputure_status = ref('');

        // 初始化onnx模型
        const initModel = async () => {
            try {
                if (MODEL_DIR === undefined) return;

                model.value = await InferenceSession.create(MODEL_DIR);
            } catch (e) {
                console.log('Error initializing model:', e);
            }
        }

        // 解码npy掩码文件成一个张量
        const loadNpyTensor = async () => {
            try {
                let npy_data = {};
                let reshapedData = null;
                await $.ajax({
                    url: "/agapi/embedding/",
                    type: "POST",
                    data: {
                        img_id: store.state.img.id
                    },
                    headers: {
                        'Authorization': "Bearer " + store.state.user.access,
                    },
                    success(resp) {
                        if (resp.result === "success") {
                            reshapedData = tf.tensor4d(resp.data, [1, 256, 64, 64], 'float32');
                            npy_data.data = reshapedData;
                            npy_data.shape = resp.shape;
                            npy_data.dType = resp.dType;
                        }
                        console.log(npy_data);
                    }
                })
                // @ts-ignore
                const tensor = new ort.Tensor(npy_data.dType, npy_data.data.dataSync(), npy_data.shape);
                return tensor;
            } catch (error) {
                console.error('Error loading npy tensor:', error);
                return null;
            }
        }

        const getmaskImg = async () => {
            caputure_status.value = "请稍候...";
            store.commit('setmaskImg', null);
            const { height, width, samScale } = handleImageScale(store.state.img.image);

            modelScale.value = {
                height: height, // 原始图像大小
                width: width, // 原始图像大小
                samScale: samScale // 被调整到最长边长1024的图像的缩放比例
            };

            const embedding = await loadNpyTensor();
            tensor.value = embedding;
            console.log('LoadImage:', store.state.img.image);
            console.log('Tensor', tensor.value);
            caputure_status.value = "信息捕捉完成!";
        }

        // 跑onnx模型
        const runONNX = async (flag) => {
            try {
                if (
                    model.value === null ||
                    (store.state.img.clicks === null && store.state.img.click_list === null) ||
                    tensor.value === null ||
                    modelScale.value === null
                ) {
                    console.log('run fail');
                    return;
                } else {
                    const feeds = await modelData({
                        clicks: flag ? store.state.img.click_list : store.state.img.clicks,
                        tensor: tensor.value,
                        modelScale: modelScale.value
                    });
                    if (feeds === undefined) return;
                    // Run the SAM ONNX model with the feeds returned from modelData()
                    const results = await model.value.run(feeds);
                    const output = results[model.value.outputNames[0]];
                    // The predicted mask returned from the ONNX model is an array which is
                    // rendered as an HTML image using onnxMaskToImage() from maskUtils.tsx.
                    if (!flag) store.commit('setmaskImg', onnxMaskToImage(output.data, output.dims[2], output.dims[3]));
                    else store.commit('setstmaskImg', onnxMaskToImage(output.data, output.dims[2], output.dims[3]));
                    console.log('run success');
                }
            } catch (e) {
                console.log(2, e);
            }
        }

        // 动态样式
        const siderStyle = {
            // textAlign: 'center',
            lineHeight: '50px',
            color: 'black',
            backgroundColor: 'rgba(173, 216, 230, 0.5)',
        };

        const contentStyle = {
            textAlign: 'center',
            minHeight: 120,
            lineHeight: '50px',
            color: 'black',
            // backgroundColor: '#108ee9',
            padding: '0 50px',
        };

        onMounted(async () => {
            try {
                // 初始化 ONNX 模型
                await Promise.all([
                    initModel()
                ]);

                console.log('Model:', model.value);

            } catch (error) {
                console.error('Error during initialization:', error);
            }
        });

        watch(
            () => store.state.img.clicks,
            (newVal, oldVal) => {
                if (newVal !== null) runONNX()
            }
        );

        return {
            has_input,
            img,
            uploadImage,
            resetImg,

            caputure_status,
            show_matting,
            handleMouseMove,
            handleClick,
            mattingSelect,
            resetMattingSelect,
            underall,
            initModel,
            getmaskImg,
            loadNpyTensor,
            runONNX,

            siderStyle,
            contentStyle,
        }
    }
}
</script>

<style scoped>
.matting-show {
    margin-top: 10px;
}

.layout {
    height: 100vh;
}
</style>