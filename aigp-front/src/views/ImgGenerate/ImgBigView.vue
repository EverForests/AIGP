<template>
    <ContentBase>
        <h1>图像无损放大</h1>
        <hr>
        <div v-if="has_input">
            当前处理图片：
            <img :src="img.src" alt="" style="width: 100%;">
            <a-button @click="resetImg">重新上传图片</a-button>
        </div>

        <ImgUpload v-if="!has_input" style="width: 100%;" @uploadImage="uploadImage" />
        <hr>

        <div class="canvas-container">
            <canvas ref="canvasRef"></canvas>
        </div>

        <div>
            <label for="upscale_option">指定图像修复的方式</label>
            <select v-model="upscale_option" name="upscale_option" id="upscale_option">
                <option value="from_ratio">等比伸缩</option>
                <option value="from_resolution">指定分辨率伸缩</option>
            </select>

            <div v-if="upscale_option === 'from_ratio'">
                <label for="upscale_ratio" class="range-label">伸缩比例: {{ upscale_ratio }}</label>
                <input v-model="upscale_ratio" type="range" id="upscale_ratio" min="1" max="8" step="0.05">
            </div>

            <div v-else>
                <label for="width_set" class="range-label">宽度: {{ width_set }}</label>
                <input v-model="width_set" type="range" id="width_set" min="64" max="8192" step="1">

                <label for="height_set" class="range-label">高度: {{ height_set }}</label>
                <input v-model="height_set" type="range" id="height_set" min="64" max="8192" step="1">
            </div>

            <label for="upscalerSelect">超分辨率模型选择: </label>
            <select v-model="upscaler_1" class="upscaler-select" id="upscalerSelect" size="1">
                <option v-for="upscaler in upscalers" :key="upscaler.name" :value="upscaler.name">{{
            upscaler.name }}</option>
            </select>

            <div v-if="has_input">
                <button @click="bigimg">开始修复</button>
                <a-button v-if="is_processed" @click="saveCanvasImg">保存图像</a-button>
                <a v-if="is_saved" :href="dlink" :download="downloadName">{{ downloadName }}</a>
                <a-button @click="share" v-if="is_saved">
                    分享图像
                </a-button>
                <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                    :options="[{ id: 1, name: 'baseedit' }, { id: 2, name: 'imgmatting' }, { id: 3, name: 'imgmerge' }, { id: 4, name: 'imgcompress' }, { id: 5, name: 'img2img' }]"
                    :hide_reset="true" />
            </div>
        </div>
    </ContentBase>
</template>

<script>
import ContentBase from '@/components/ContentBase.vue';
import ImgUpload from '@/components/ImgUpload.vue';
import { onMounted, ref, watch } from 'vue';
import { useStore } from 'vuex';
import $ from 'jquery';

export default {
    name: "ImgBigView",
    components: {
        ContentBase,
        ImgUpload,
    },
    setup() {
        const store = useStore();
        const canvasRef = ref(null);
        const is_processed = ref(false);

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
            is_saved.value = false;
            is_shared.value = false;

            store.state.img.image = null;  // 同步操作
            img.src = "";

            // 清空画布
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        // 画布重绘
        const draw = () => {
            is_saved.value = false;
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, img.width, img.height);
        }

        // 处理跳转过来的图片
        const drawImg = () => {
            if (!store.state.img.image) return;
            const canvas = canvasRef.value;

            canvas.width = img.width;
            canvas.height = img.height;
            draw();
        }

        // 图像无损放大
        const upscale_option = ref('from_ratio');
        const upscale_ratio = ref(2);
        const width_set = ref(512);
        const height_set = ref(512);
        const upscalers = ref([]);
        const upscaler_1 = ref('');

        const bigimg = async () => {
            if (!store.state.img.image) return;

            is_saved.value = false;

            const canvas = canvasRef.value;
            const imageDataURL = canvas.toDataURL();
            const imageData = {
                "upscale_resize": upscale_ratio.value,
                "upscaling_resize_w": width_set.value,
                "upscaling_resize_h": height_set.value,
                "upscaling_crop": true,
                "upscaler_1": upscaler_1.value,
                "image": imageDataURL,
            }

            await $.ajax({
                url: '/sdapi/v1/extra-single-image',
                type: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(imageData),
                success(resp) {
                    console.log(resp);

                    const tempImg = new Image();
                    const tempsrc = `data:image/png;base64,${resp.image}`
                    tempImg.onload = function () {
                        img.onload = function () {  // 需进行异步优化
                            canvas.width = img.width;
                            canvas.height = img.height;
                            draw();
                            is_processed.value = true;
                        }
                        img.src = tempsrc;
                        img.width = tempImg.width;
                        img.height = tempImg.height;
                    }
                    tempImg.src = tempsrc;

                },
                error(error) {
                    console.error('Error: ', error)
                }
            })
        }

        $.ajax({
            url: '/sdapi/v1/upscalers',
            type: "GET",
            headers: {
                'Content-Type': 'application/json'
            },
            success(resp) {
                upscalers.value = resp;
            },
            error(error) {
                console.error('Error: ', error);
            }
        })

        // 图像保存
        const is_saved = ref(false);
        const is_shared = ref(false);
        const dlink = ref('');
        const downloadName = ref('');

        const saveCanvasImg = () => {
            const canvas = canvasRef.value;
            let imageDataURL = '';

            imageDataURL = canvas.toDataURL();
            downloadName.value = 'bigimg.png'

            store.commit('setsavetool', imageDataURL.split(',')[1]);
            dlink.value = imageDataURL;

            is_saved.value = true;
            is_processed.value = false;
        }

        const share = () => {
            is_shared.value = true;
        }

        onMounted(
            () => {
                drawImg();
            }
        )

        watch(
            () => store.state.img.image,
            () => {
                drawImg();
            }
        )

        return {
            canvasRef,

            has_input,
            img,
            uploadImage,
            resetImg,

            is_processed,

            upscale_option,
            upscale_ratio,
            width_set,
            height_set,
            upscalers,
            upscaler_1,
            bigimg,

            is_saved,
            is_shared,
            dlink,
            downloadName,
            saveCanvasImg,
            share,
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
</style>