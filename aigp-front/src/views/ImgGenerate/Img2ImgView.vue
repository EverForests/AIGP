<template>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <a-layout style="height: 100vh;">
        <a-layout-sider :style="siderStyle">
            <div v-if="op_selection === 'all_repaint'">
                <div>底图</div>

                <div v-if="has_input1">
                    <img :src="img.src" alt="" style="width: 100%;">
                </div>

                <ImgUpload v-if="!has_input1" style="width: 100%;" @uploadImage="uploadImage" />

                <a-button @click="resetImg">重新上传图片</a-button>

                <a-button type="primary" v-if="has_input1" @click="all_preview">全局重绘预览</a-button>
            </div>

            <div v-if="op_selection === 'area_repaint'">
                <div>
                    图片1
                    <div v-if="has_input1">
                        <img :src="img.src" alt="" style="width: 100%;">
                    </div>

                    <ImgUpload v-if="!has_input1" style="width: 100%;" @uploadImage="uploadImage" />
                </div>

                <hr>
                <div v-if="has_input1">
                    图片2
                    <div v-if="has_input2">
                        <img :src="supimg.src" alt="" style="width: 100%;">
                    </div>

                    <ImgUpload v-if="!has_input2" style="width: 100%;" @uploadImage="uploadImage" />
                </div>

                <a-button @click="resetImg">重新上传图片</a-button>

                <hr>

                <div v-if="has_input1 && has_input2">
                    <label for="is_mask_selection">是否将图片2作为蒙版</label>
                    <select v-model="is_mask_selection" name="is_mask_selection" id="is_mask_selection">
                        <option value='yes'>是</option>
                        <option value='no'>否</option>
                    </select>

                    <a-button type="primary" @click="area_preview">局部重绘预览</a-button>
                </div>
            </div>
        </a-layout-sider>

        <a-layout-content :style="contentStyle">
            <a-breadcrumb style="margin: 16px 0">
                <a-breadcrumb-item>
                    <router-link class="nav-link" :to="{ name: 'home' }">首页</router-link>
                </a-breadcrumb-item>

                <a-breadcrumb-item>
                    <router-link class="nav-link" :to="{ name: 'imggenerate' }">图像生成</router-link>
                </a-breadcrumb-item>

                <a-breadcrumb-item>
                    <router-link class="nav-link" :to="{ name: 'img2img' }">图生图</router-link>
                </a-breadcrumb-item>
            </a-breadcrumb>
            <label for="op_selection">选择进行的图像操作</label>
            <select v-model="op_selection" name="op_selection" id="op_selection">
                <option value="all_repaint">全局重绘</option>
                <option value="area_repaint">局部蒙版重绘</option>
            </select>

            <hr>

            <div v-if="op_selection !== 'all_repaint'" v-show="is_completed">白色区域为目标修饰位置</div>
            <div class="canvas-container">
                <canvas v-show="is_completed" ref="canvasRef"></canvas>
            </div>

            <div>
                <a-button v-if="is_processed" @click="saveCanvasImg">保存图像</a-button>
                <a v-if="is_saved" :href="dlink" :download="downloadName">{{ downloadName }}</a>
                <a-button @click="share" v-if="is_saved">
                    分享图像
                </a-button>
                <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                    :options="[{ id: 1, name: 'baseedit' }, { id: 2, name: 'imgmatting' }, { id: 4, name: 'imgcompress' }, { id: 5, name: 'img2img' }, { id: 6, name: 'imgbig' }]"
                    :hide_reset="true" />
            </div>
        </a-layout-content>

        <a-layout-sider :style="siderStyle">
            <div v-if="is_completed">
                <div>参数调节区域</div>
                <!-- 查看当前模型 -->

                <div>
                    当前模型：{{ sd_model_checkpoint }}
                    <button @click="get_sd_model_option" type="button" class="btn btn-sm">
                        <i class="fas fa-sync-alt"></i> <!-- 使用 Font Awesome 的刷新图标 -->
                    </button>
                </div>

                <!-- 模型列表 -->
                <div class="form-group">
                    <label for="modelSelect">模型选择</label>
                    <select v-model="sd_model_local" class="form-control form-select" id="modelSelect">
                        <option v-for="sd_model in sd_model_list" :key="sd_model.hash" :value="sd_model.model_name">{{
            sd_model.model_name }}</option>
                    </select>
                </div>

                <!-- 更换模型 -->

                <div class="mb-3">
                    <button @click="set_sd_model" type="button" class="btn btn-primary btn-sm">更换模型</button>
                    <span class="error_message">{{ change_model_status }}</span>
                </div>

                <a-button type="primary" @click="showModal" style="background-color: orange;">参数设置</a-button>
                <div>
                    <a-modal v-model:open="open" title="参数设置" @ok="handleOk">
                        <!-- 参数调节 -->
                        <div>
                            <div>
                                正向提示词
                                <a-textarea v-model:value="prompt" placeholder="编辑文本" :rows="4"></a-textarea>
                                <a-button @click="clip">逆向推理</a-button>
                                {{ clip_state }}
                            </div>
                            <hr>

                            <div>
                                负向提示词
                                <a-textarea v-model:value="negative_prompt" placeholder="编辑文本" :rows="4"></a-textarea>
                            </div>
                            <hr>

                            <div>
                                正向影响因子
                                <a-slider v-model:value="cfg_scale" :min="1" :max="10" :step="0.5"
                                    style="margin: 0 16px 0 16px" />
                                <a-input-number v-model:value="cfg_scale" :min="1" :max="10" :step="0.5" />
                            </div>
                            <hr>


                            <div>
                                迭代步数
                                <a-slider v-model:value="steps" :min="10" :max="50" :step="1"
                                    style="margin: 0 16px 0 16px" />
                                <a-input-number v-model:value="steps" :min="10" :max="50" :step="1" />
                            </div>
                            <hr>

                            <div>
                                重绘强度
                                <a-slider v-model:value="denoising_strength" :min="0" :max="1" :step="0.01"
                                    style="margin: 0 16px 0 16px" />
                                <a-input-number v-model:value="denoising_strength" :min="0" :max="1" :step="0.01" />
                            </div>
                            <hr>

                            <!-- 采样器选择 -->
                            <div class="form-group">
                                <label for="samplerSelect">采样器选择: </label>
                                <select v-model="sampler" class="form-control form-select sampler-select"
                                    id="samplerSelect" size="1">
                                    <option v-for="sampler in samplers" :key="sampler.name" :value="sampler.name">
                                        {{ sampler.name }}
                                    </option>
                                </select>
                            </div>
                            <hr>

                            <div v-if="op_selection === 'area_repaint'" class="mask-setting">
                                <div>蒙版设置</div>
                                <div class="container">
                                    <div class="range-container">
                                        <label for="mask_blur" class="range-label">蒙版模糊度: {{ mask_blur }}</label>
                                        <input v-model="mask_blur" type="range" id="mask_blur" min="0" max="64"
                                            step="1">
                                    </div>
                                </div>
                                <hr>

                                <div class="inpainting-fill">
                                    <div>蒙版遮住的内容</div>
                                    <label class="radio-container">填充
                                        <input type="radio" v-model="inpainting_fill" value=0>
                                        <span class="checkmark"></span>
                                    </label>

                                    <label class="radio-container">原图
                                        <input type="radio" v-model="inpainting_fill" value=1>
                                        <span class="checkmark"></span>
                                    </label>

                                    <label class="radio-container">潜在噪声
                                        <input type="radio" v-model="inpainting_fill" value=2>
                                        <span class="checkmark"></span>
                                    </label>

                                    <label class="radio-container">无潜在空间
                                        <input type="radio" v-model="inpainting_fill" value=3>
                                        <span class="checkmark"></span>
                                    </label>
                                </div>
                                <hr>

                                <div class="inpaint-full-res">
                                    <div>绘制区域</div>
                                    <label class="radio-container">全图
                                        <input type="radio" v-model="inpaint_full_res" value='false'>
                                        <span class="checkmark"></span>
                                    </label>

                                    <label class="radio-container">仅蒙版
                                        <input type="radio" v-model="inpaint_full_res" value='true'>
                                        <span class="checkmark"></span>
                                    </label>
                                </div>
                                <hr>

                                <div class="container inpaint-full-res-padding">
                                    <div class="range-container">
                                        <label for="inpaint_full_res_padding" class="range-label">仅蒙版绘制参考半径:
                                            {{ inpaint_full_res_padding }}</label>
                                        <input v-model="inpaint_full_res_padding" type="range"
                                            id="inpaint_full_res_padding" min="0" max="256" step="1">
                                    </div>
                                </div>
                                <hr>

                                <div class="inpainting-mask-invert">
                                    <div>蒙版模式</div>
                                    <label class="radio-container">绘制蒙版内容
                                        <input type="radio" v-model="inpainting_mask_invert" value=0>
                                        <span class="checkmark"></span>
                                    </label>

                                    <label class="radio-container">绘制非蒙版内容
                                        <input type="radio" v-model="inpainting_mask_invert" value=1>
                                        <span class="checkmark"></span>
                                    </label>
                                </div>
                            </div>
                            <!-- 蒙版设置结束，还可以进行更多设置 -->
                        </div>
                    </a-modal>
                </div>

                <a-button @click="img2img">生成</a-button>
            </div>
        </a-layout-sider>
    </a-layout>
</template>

<script>
import ImgUpload from '@/components/ImgUpload.vue'
import ContentBase from '@/components/ContentBase.vue'
import { ref, watch } from 'vue'
import { useStore } from 'vuex'
import router from '@/router'
import $ from 'jquery'

export default {
    name: "Img2ImgView",
    components: {
        ContentBase,
        ImgUpload,
    },
    setup() {
        const store = useStore();
        const canvasRef = ref(null);
        const op_selection = ref('all_repaint');

        const is_mask_selection = ref('yes')
        const is_show = ref(false);

        const img = new Image();  // canvas展示图片的信息
        const supimg = new Image();  // 辅助接口
        // 接收已经存在的img.image
        const has_input1 = ref(false);
        const has_input2 = ref(false);
        if (store.state.img.image) {
            img.onload = function () {
                has_input1.value = true;
                store.state.img.image = null;  // 准备后续上传
            }
            img.src = store.state.img.image.src;
        }

        // 如果不存在，则上传图片后更新，区分图片1和图片2
        const uploadImage = () => {
            if (!store.state.img.image) return;

            if (has_input1.value === false) {
                img.onload = function () {
                    has_input1.value = true;
                    store.state.img.image = null;  // 准备后续上传
                }
                img.src = store.state.img.image.src;
            }

            else {
                supimg.onload = function () {
                    has_input2.value = true;
                }
                supimg.src = store.state.img.image.src;
            }
        }

        // 重新上传图片
        const resetImg = () => {
            // 优先调整标志位
            has_input1.value = false;
            has_input2.value = false;
            is_saved.value = false;
            is_shared.value = false;
            is_processed.value = false;
            is_completed.value = false;

            store.state.img.image = null;  // 同步操作
            img.src = "";
            supimg.src = "";

            // 清空画布
            const canvas = canvasRef.value;
            if (canvas) {
                const ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }

        const originImg = new Image();
        const maskImg = new Image();

        // 全局重绘
        const all_preview = () => {
            is_completed.value = false;
            const canvas = canvasRef.value;

            maskImgURL = null;  // 控制后续请求

            originImg.onload = function () {
                canvas.width = originImg.width;
                canvas.height = originImg.height;
                draw(originImg);
                originImgURL = canvas.toDataURL();
                is_completed.value = true;
            }

            originImg.src = img.src;
        }

        // 局部蒙版重绘
        const to_imgmatting = () => {
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'imgmatting' });
        }

        // 存图+绘图
        let originImgURL = null;
        let maskImgURL = null;
        const is_completed = ref(false);  // 标志存图结束，存图后才提交请求

        const draw = (Img) => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(Img, 0, 0, Img.width, Img.height);
        }

        // 局部重绘预览
        const area_preview = () => {
            is_completed.value = false;
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');

            originImg.onload = function () {
                canvas.width = originImg.width;
                canvas.height = originImg.height;
                draw(originImg);
                originImgURL = canvas.toDataURL();
            }

            maskImg.onload = function () {
                canvas.width = maskImg.width;
                canvas.height = maskImg.height;
                draw(maskImg);
                maskImgURL = canvas.toDataURL();

                canvas.width = originImg.width;
                canvas.height = originImg.height;
                ctx.save();
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(originImg, 0, 0, originImg.width, originImg.height);
                ctx.globalCompositeOperation = 'lighter';
                ctx.drawImage(maskImg, 0, 0, maskImg.width, maskImg.height);
                ctx.restore();

                is_completed.value = true;
            }

            // 交换顺序，保证当前img为底图, supimg为蒙版
            if (is_mask_selection.value === 'no') {
                const temp = new Image();

                temp.onload = function () {
                    img.src = supimg.src;
                    supimg.src = temp.src;
                    originImg.src = img.src;
                    maskImg.src = supimg.src;
                }

                temp.src = img.src;
            }

            else {
                originImg.src = img.src;
                maskImg.src = supimg.src;
            }
        }

        // 调节参数
        // 获取当前模型信息
        const sd_model_checkpoint = ref('');
        const get_sd_model_option = async () => {
            await $.ajax({
                url: '/sdapi/v1/options',
                type: "GET",
                headers: {
                    'Content-Type': 'application/json'
                },
                success(resp) {
                    sd_model_checkpoint.value = resp.sd_model_checkpoint;
                },
                error(error) {
                    console.error('Error: ', error)
                }
            })
        }

        // 模型列表
        const sd_model_list = ref([]);
        const sd_model_local = ref('');  // 本地选中的模型
        $.ajax({
            url: '/sdapi/v1/sd-models',
            type: "GET",
            headers: {
                'Content-Type': 'application/json'
            },
            success(resp) {
                sd_model_list.value = resp;
            },
            error(error) {
                console.error('Error: ', error);
            }
        })

        // 更换模型
        const change_model_status = ref('');
        const set_sd_model = async () => {
            if (sd_model_local.value === '') {
                change_model_status.value = "请先选择模型";
                return;
            }

            change_model_status.value = "请稍候...";

            let option_payload = {
                "sd_model_checkpoint": sd_model_local.value,
                "CLIP_stop_at_last_layers": 2,
            };

            await $.ajax({
                url: '/sdapi/v1/options',
                type: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(option_payload),
                success(resp) {
                    sd_model_checkpoint.value = sd_model_local.value;
                    change_model_status.value = "模型更换成功！";
                },
                error(error) {
                    console.error('Error: ', error)
                }
            })
        }

        // 正负提示词
        const prompt = ref('');
        const negative_prompt = ref('');

        // 逆向推理
        const clip_state = ref('');
        const clip = async () => {
            clip_state.value = '请稍候...';

            const imageData = {
                "image": originImgURL,
                "model": "clip"
            }

            await $.ajax({
                url: '/sdapi/v1/interrogate',
                type: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(imageData),
                success(resp) {
                    prompt.value += resp.caption.replace(/<error>$/, '');
                    clip_state.value = '图像描述生成完毕!';
                },
                error(error) {
                    console.error('Error: ', error)
                }
            })
        }

        // 蒙版设置
        const inpainting_fill = ref(1);
        const mask_blur = ref(4);
        const inpaint_full_res = ref('false');
        const inpaint_full_res_padding = ref(32);
        const inpainting_mask_invert = ref(0);
        const denoising_strength = ref(0.75);

        // 正向提示因子和迭代步数
        const cfg_scale = ref(7);
        const steps = ref(20);

        // 采样器选择
        const sampler = ref('');
        const samplers = ref([]);
        $.ajax({
            url: '/sdapi/v1/samplers',
            type: "GET",
            headers: {
                'Content-Type': 'application/json'
            },
            success(resp) {
                samplers.value = resp;
            },
            error(error) {
                console.error('Error: ', error)
            }
        })

        // 生成
        const is_processed = ref(false);
        const img2img = async () => {
            is_saved.value = false;
            const imageData = {
                "prompt": prompt.value,
                "negative_prompt": negative_prompt.value,

                "sampler_name": sampler.value,
                "steps": steps.value,
                "cfg_scale": cfg_scale.value,

                "width": originImg.width,
                "height": originImg.height,
                "resize_mode": 1, // ["Just resize", "Crop and resize", "Resize and fill", "Just resize (latent upscale)"]

                "init_images": [
                    originImgURL,
                ],
                "mask": maskImgURL,

                "mask_blur": mask_blur.value, // 蒙版模糊度
                "inpainting_fill": inpainting_fill.value,  // 蒙版遮住的内容， 0填充， 1原图 2潜空间噪声 3潜空间数值零
                "inpaint_full_res": inpaint_full_res.value,  // inpaint area, False: whole picture True：only masked
                "inpaint_full_res_padding": inpaint_full_res_padding.value,  // Only masked padding, pixels 32
                "inpainting_mask_invert": inpainting_mask_invert.value,  // 蒙版模式 0重绘蒙版内容 1 重绘非蒙版内容

                "denoising_strength": denoising_strength.value, // 重绘幅度
            }

            console.log(imageData);

            await $.ajax({
                url: '/sdapi/v1/img2img',
                type: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(imageData),
                success(resp) {
                    console.log(resp);
                    const canvas = canvasRef.value;
                    const tempImg = new Image();
                    const tempsrc = `data:image/png;base64,${resp.images}`
                    tempImg.onload = function () {
                        canvas.width = tempImg.width;
                        canvas.height = tempImg.height;

                        draw(tempImg);
                        is_processed.value = true;
                    }
                    tempImg.src = tempsrc;

                },
                error(error) {
                    console.error('Error: ', error)
                }
            })
        }

        // 图像保存
        const is_saved = ref(false);
        const is_shared = ref(false);
        const dlink = ref('');
        const downloadName = ref('');

        const saveCanvasImg = () => {
            const canvas = canvasRef.value;

            const imageDataURL = canvas.toDataURL();
            downloadName.value = 'img2img.png'

            store.commit('setsavetool', imageDataURL.split(',')[1]);
            dlink.value = imageDataURL;

            is_saved.value = true;
            is_processed.value = false;
        }

        const share = () => {
            is_shared.value = true;
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

        const open = ref(false);
        const showModal = () => {
            open.value = true;
        };
        const handleOk = e => {
            console.log(e);
            open.value = false;
        };

        watch(
            () => op_selection.value,
            () => {
                is_completed.value = false;
            }
        )

        return {
            canvasRef,

            has_input1,
            has_input2,
            img,
            supimg,
            uploadImage,
            resetImg,

            op_selection,

            all_preview,

            is_mask_selection,
            is_show,
            to_imgmatting,
            area_preview,

            sd_model_checkpoint,
            get_sd_model_option,

            sd_model_local,
            sd_model_list,

            change_model_status,
            set_sd_model,

            prompt,
            negative_prompt,

            clip_state,
            clip,

            cfg_scale,
            steps,

            sampler,
            samplers,

            inpainting_fill,
            mask_blur,
            inpaint_full_res,
            inpaint_full_res_padding,
            inpainting_mask_invert,
            denoising_strength,

            is_completed,

            is_saved,
            is_shared,
            is_processed,
            dlink,
            downloadName,
            saveCanvasImg,
            share,

            img2img,

            siderStyle,
            contentStyle,

            open,
            showModal,
            handleOk,
        }
    }
}
</script>

<style scoped>
.canvas-container {
    overflow: hidden;
    max-width: 100%;
    max-height: 100%;
    background-color: gray;
}

canvas {
    max-width: 100%;
    max-height: auto;
}

img {
    border: 1px solid black;
    background-color: gray;
}
</style>