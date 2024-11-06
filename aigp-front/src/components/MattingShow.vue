<template>
    <div class="show-stage">
        <div>
            <div class="canvas-container">
                <canvas ref="canvasRef" class="draw"></canvas>
            </div>
        </div>

        <div>
            <a-button @click="saveCanvasImg">保存图像</a-button>
            <a v-if="is_saved" :href="dlink" :download="downloadName">{{ downloadName }}</a>
            <a-button @click="share" v-if="is_saved">
                分享图像
            </a-button>
            <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                :options="[{ id: 1, name: 'baseedit' }, { id: 3, name: 'imgmerge' }, { id: 4, name: 'imgcompress' }, { id: 5, name: 'img2img' }]"
                :hide_reset="true" />
        </div>
    </div>
</template>

<script>
import ImgUpload from './ImgUpload.vue';
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex';
export default {
    name: "MattingShow",
    components: {
        ImgUpload,
    },
    setup() {
        const store = useStore();
        const canvasRef = ref(null);
        const is_saved = ref(false);
        const is_shared = ref(false);
        const downloadName = ref('');  // 文件名
        const dlink = ref('');

        const drawCanvas = () => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');

            // 加载原始图像和掩膜
            const originalImage = new Image();
            originalImage.src = store.state.img.image.src;

            const maskImg = new Image();
            maskImg.src = store.state.img.stmaskImg.src;

            // 等待图像加载完成后执行操作
            originalImage.onload = function () {
                // 设置 Canvas 尺寸与原始图像一致
                canvas.width = originalImage.width;
                canvas.height = originalImage.height;

                // 绘制原始图像
                ctx.drawImage(originalImage, 0, 0);

                // 绘制掩膜
                ctx.globalCompositeOperation = 'destination-in'; // 设置合成操作为"destination-in"，将绘制限制在原始图像上
                ctx.drawImage(maskImg, 0, 0);
            };
        }

        const saveCanvasImg = () => {
            const canvas = canvasRef.value;
            let imageDataURL = '';

            imageDataURL = canvas.toDataURL('image/png');
            downloadName.value = 'matting.png'

            store.commit('setsavetool', imageDataURL.split(',')[1]);
            dlink.value = imageDataURL;

            is_saved.value = true;
        }

        const share = () => {
            is_shared.value = true;
        }

        onMounted(
            () => {
                drawCanvas();
            }
        )

        return {
            canvasRef,
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
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: gray;
}

canvas {
    max-width: 100%;
}
</style>
