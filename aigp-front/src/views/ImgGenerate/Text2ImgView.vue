<template>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <ContentBase>
        <div>
            <!-- 查看当前模型 -->
            <div class="d-flex align-items-center justify-content-center">
                <div class="mb-3">
                    <span class="ml-2">当前模型：{{ sd_model_checkpoint }}</span>
                </div>
                <div class="mb-3 ms-2">
                    <button @click="get_sd_model_option" type="button" class="btn btn-sm">
                        <i class="fas fa-sync-alt"></i> <!-- 使用 Font Awesome 的刷新图标 -->
                    </button>
                </div>
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

            <!-- 输入框和生成图片按钮 -->
            <div>
                <label for="prompt" class="form-label text">正向提示词</label>
                <textarea v-model="prompt" class="form-control" id="prompt" rows="3"></textarea>

                <label for="negative_prompt" class="form-label text">负向提示词</label>
                <textarea v-model="negative_prompt" class="form-control" id="negative_prompt" rows="3"></textarea>

                <div class="container">
                    <!-- 显示和调整cfg_scale -->
                    <div class="range-container">
                        <label for="rangeInput" class="range-label">正向提示因子: {{ cfg_scale }}</label>
                        <input v-model="cfg_scale" type="range" id="rangeInput1" min="1.0" max="10.0" step="0.5">
                    </div>
                </div>

                <div class="container">
                    <!-- 显示和调整steps -->
                    <div class="range-container">
                        <label for="rangeInput" class="range-label">迭代步数: {{ steps }}</label>
                        <input v-model="steps" type="range" id="rangeInput2" min="10" max="50" step="1">
                    </div>
                </div>

                <!-- 采样器选择 -->
                <div class="form-group">
                    <label for="samplerSelect">采样器选择: </label>
                    <select v-model="sampler" class="form-control form-select sampler-select" id="samplerSelect"
                        size="1">
                        <option v-for="sampler in samplers" :key="sampler.name" :value="sampler.name">{{
                        sampler.name }}</option>
                    </select>
                </div>

                <button @click="text2img" type="button" class="btn btn-primary btn-sm mt-3">生成图片</button>
            </div>



            <!-- 显示生成图片 -->
            <div>
                <div>{{ img_generate_status }}</div>
                <img v-if="decodedImageData" :src="decodedImageData" alt="Decoded Image" class="mt-3 img-small" />
            </div>

            <ImgUpload v-if="decodedImageData" :image="rawdata"
                :options="[{ id: 3, name: 'imgmatting' }, { id: 4, name: 'imgmerge' }]" :shared="true"
                :hide_reset=true />

        </div>
    </ContentBase>

</template>

<script>
import { ref } from 'vue'
import ContentBase from '@/components/ContentBase.vue'
import ImgUpload from '@/components/ImgUpload.vue'
import $ from 'jquery'
import router from '@/router';
import { useStore } from 'vuex';
import { handleImageScale } from '@/helpers/scaleHelpers';


export default {
    name: "Text2ImgView",
    components: {
        ContentBase,
        ImgUpload,
    },
    setup() {
        let decodedImageData = ref('');
        let rawdata = ref('');
        let change_model_status = ref('');
        let img_generate_status = ref('');
        let filename = ref('');

        let sd_model_checkpoint = ref('');
        let sd_model_list = ref([]);
        let sd_model_local = ref('');  // 本地选中的模型

        let prompt = ref('');
        let negative_prompt = ref('');
        let cfg_scale = ref(1.0);
        let steps = ref(10);
        let sampler = ref('');
        let samplers = ref([]);

        const store = useStore();

        // 获取模型列表
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

        // 获取采样器列表
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

        // 获取当前使用的模型
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

        // 设置需要使用的模型
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

        // text2img
        const text2img = async () => {
            decodedImageData.value = '';

            let requestData = {
                "prompt": prompt.value,
                "negative_prompt": negative_prompt.value,
                "styles": [
                    "string"
                ],
                "seed": -1,
                "subseed": -1,
                "subseed_strength": 0,
                "seed_resize_from_h": -1,
                "seed_resize_from_w": -1,
                "sampler_name": sampler.value,
                "batch_size": 1,
                "n_iter": 1,
                "steps": steps.value,
                "cfg_scale": cfg_scale.value,
                "width": 1920,
                "height": 1080,
                "restore_faces": false,
                "tiling": false,
                "do_not_save_samples": true,
                "do_not_save_grid": true,
                "eta": 0,
                "denoising_strength": 0,
                "s_min_uncond": 0,
                "s_churn": 0,
                "s_tmax": 0,
                "s_tmin": 0,
                "s_noise": 1,
                "override_settings": {},
                "override_settings_restore_afterwards": true,
                "refiner_checkpoint": "",
                "refiner_switch_at": 0,
                "disable_extra_networks": false,
                "firstpass_image": "",
                "comments": {},
                "enable_hr": false,
                "firstphase_width": 0,
                "firstphase_height": 0,
                "hr_scale": 2,
                "hr_upscaler": "",
                "hr_second_pass_steps": 0,
                "hr_resize_x": 0,
                "hr_resize_y": 0,
                "hr_checkpoint_name": "",
                "hr_sampler_name": "",
                "hr_prompt": "",
                "hr_negative_prompt": "",
                "force_task_id": "",
                "sampler_index": "Euler",
                "script_args": [],
                "send_images": true,
                "save_images": true,
                "alwayson_scripts": {},
                "infotext": "string"  // 需要为string
            };

            img_generate_status.value = "请稍候...";

            await $.ajax({
                url: '/sdapi/v1/txt2img',
                type: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(requestData),
                success(resp) {
                    rawdata.value = resp.images;
                    decodedImageData.value = `data:image/png;base64,${resp.images}`;
                    img_generate_status.value = "图像生成完毕!";
                },
                error(error) {
                    console.error('Error: ', error)
                }
            })
        }

        // const editGeneratedImg = async () => {
        //     const byteCharacters = atob(rawdata.value);
        //     const byteNumbers = new Array(byteCharacters.length);
        //     for (let i = 0; i < byteCharacters.length; i++) {
        //         byteNumbers[i] = byteCharacters.charCodeAt(i);
        //     }
        //     const byteArray = new Uint8Array(byteNumbers);
        //     // 创建 Blob 对象，表示二进制数据
        //     const blob = new Blob([byteArray], { type: 'image/png' });

        //     let formData = new FormData();
        //     formData.append("username", store.state.user.username);
        //     formData.append("image", blob, filename.value + ".png");
        //     formData.append("title", filename);
        //     formData.append("flag", true);

        //     await $.ajax({
        //         url: "/agapi/postimg/",
        //         type: "POST",
        //         data: formData,
        //         processData: false,  // 禁止 jQuery 对 FormData 进行处理
        //         contentType: false,  // 禁止 jQuery 设置请求头的 Content-Type
        //         headers: {
        //             // 'Content-Type': 'multipart/form-data',
        //             'Authorization': "Bearer " + store.state.user.access,
        //         },
        //         success(resp) {
        //             if (resp.result === "success") {
        //                 store.commit('setImgId', resp.id);
        //                 const img = new Image();
        //                 img.src = resp.image;
        //                 img.onload = () => {
        //                     const { height, width, samScale } = handleImageScale(img);

        //                     img.width = width;
        //                     img.height = height;
        //                     store.commit('setImage', img);
        //                 };

        //                 router.push({ name: "imgedit" });
        //             }
        //         }
        //     })
        // }

        return {
            prompt,
            negative_prompt,
            decodedImageData,
            rawdata,
            sd_model_checkpoint,
            sd_model_list,
            sd_model_local,
            change_model_status,
            img_generate_status,
            cfg_scale,
            steps,
            sampler,
            samplers,
            filename,
            text2img,
            set_sd_model,
            get_sd_model_option,
        }
    }
}


</script>

<style scoped>
.text {
    margin-top: 30px
}

img {
    margin-top: 30px
}

.error_message {
    color: red;
}

.SetProgress {
    margin-top: 30px
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    /* 填充整个视口高度 */
}

.range-container {
    display: flex;
    align-items: center;
}

.range-label {
    margin-right: 10px;
}

.sampler-select {
    max-height: 50px;
    /* 设置下拉列表的最大高度 */
    overflow-y: auto;
    /* 启用垂直滚动条 */
}

.form-group {
    margin-top: 10px
}

.img-small {
    width: 50%;
    height: auto;
}

button {
    margin-top: 10px
}

* {
    margin-top: 3px
}
</style>
