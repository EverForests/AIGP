<template>
    <ContentBase>
        <h1>图像压缩</h1>
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

        <div v-if="has_input">
            <button @click="compress">压缩图像</button>
            <a-button v-if="is_processed" @click="saveCanvasImg">保存图像</a-button>
            <a v-if="is_saved" :href="dlink" :download="downloadName">{{ downloadName }}</a>
            <a-button @click="share" v-if="is_saved">
                分享图像
            </a-button>
            <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                :options="[{ id: 3, name: 'imgmatting' }, { id: 4, name: 'imgmerge' }, { id: 6, name: 'img2img' }]"
                :hide_reset="true" />
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
    name: "ImgCompressView",
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

        // 图像压缩
        const maxWidth = ref(1)
        const compress = () => {
            is_saved.value = false;
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');

            if (!img.src) return;
            let maxWidth = 1024;
            let maxHeight = 1024;

            let ratio;
            let needCompress = false;

            if (img.width > maxWidth) {
                needCompress = true;
                ratio = img.width / maxWidth;
                maxHeight = img.height / ratio;
            }

            if (img.height > maxHeight) {
                needCompress = true;
                ratio = img.height / maxHeight;
                maxWidth = img.width / ratio;
            }

            if (!needCompress) {
                maxWidth = img.width;
                maxHeight = img.height;
            }

            img.width = maxWidth;
            img.height = maxHeight;

            canvas.width = maxWidth;
            canvas.height = maxHeight;

            draw();

            is_processed.value = true;
        }

        // 重绘函数
        const draw = () => {
            is_saved.value = false;
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, img.width, img.height);
        }

        const drawImg = () => {
            if (!store.state.img.image) return;
            const canvas = canvasRef.value;

            canvas.width = img.width;
            canvas.height = img.height;
            draw();
        }

        // 图像保存
        const is_saved = ref(false);
        const is_shared = ref(false);
        const dlink = ref('');  // 下载链接
        const downloadName = ref('');  // 文件名

        const saveCanvasImg = () => {
            const canvas = canvasRef.value;
            let imageDataURL = '';

            imageDataURL = canvas.toDataURL('image/jpeg', 0.8);
            downloadName.value = 'compression.jpeg'

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
            is_processed,

            has_input,
            img,
            uploadImage,
            resetImg,

            compress,

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