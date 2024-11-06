<template>
    <ContentBase>
        <h1>图像融合</h1>
        <div>先上传两张图片</div>
        <hr>
        <div>
            <div>
                请上传图片1
                <div v-if="has_input1">
                    <img :src="img.src" alt="" style="width: 100%;">
                </div>

                <ImgUpload v-if="!has_input1" style="width: 100%;" @uploadImage="uploadImage" />
            </div>

            <hr>
            <div v-if="has_input1">
                请上传图片2
                <div v-if="has_input2">
                    <img :src="supimg.src" alt="" style="width: 100%;">
                </div>

                <ImgUpload v-if="!has_input2" style="width: 100%;" @uploadImage="uploadImage" />
            </div>

            <a-button @click="resetImg">重新上传图片</a-button>
        </div>
        <hr>
        <div v-if="has_input1 && has_input2">
            <div>
                <input type="radio" id="yes" value="yes" v-model="choose">
                <label for="yes">是</label>

                <input type="radio" id="no" value="no" v-model="choose">
                <label for="no">否</label>

                <p>是否将1号图片作为前景 {{ choose }}</p>
            </div>
            <div>
                <button @click="startMerging">开始整合</button>
                <div>
                    调节前景大小
                    <label for="shrink_factor" class="range-label">伸缩系数: {{ shrink_factor }}</label>
                    <input v-model="shrink_factor" type="range" id="shrink_factor" min="0" max="2" step="0.1">
                </div>
                <button @click="reset_frontImg">前景复位</button>
                <div>
                    调节透明度
                    <label for="opacity_factor" class="range-label">不透明度: {{ opacity_factor }}</label>
                    <input v-model="opacity_factor" type="range" id="opacity_factor" min="0" max="1" step="0.1">
                </div>
                <div>
                    旋转调整
                    <label for="rotationAngle" class="range-label">旋转角度: {{ rotationAngle }}</label>
                    <input v-model="rotationAngle" type="range" id="rotationAngle" min="0" max="360" step="1">
                </div>
                <div class="canvas-container">
                    <canvas ref="canvasRef"></canvas>
                </div>

                <div v-if="is_processed">
                    <a-button @click="saveCanvasImg">保存图像</a-button>
                    <a v-if="is_saved" :href="dlink" :download="downloadName">{{ downloadName }}</a>
                    <a-button @click="share" v-if="is_saved">
                        分享图像
                    </a-button>
                    <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                        :options="[{ id: 1, name: 'baseedit' }, { id: 2, name: 'imgmatting' }, { id: 4, name: 'imgcompress' }, { id: 5, name: 'img2img' }, { id: 6, name: 'imgbig' }]"
                        :hide_reset="true" />
                </div>
            </div>
        </div>

    </ContentBase>


</template>

<script>
import ImgUpload from '@/components/ImgUpload.vue';
import ContentBase from '@/components/ContentBase.vue';
import { useStore } from 'vuex';
import { ref, watch } from 'vue';
import { FromPixels } from '@tensorflow/tfjs';

export default {
    name: "ImgMergeView",
    components: {
        ImgUpload,
        ContentBase,
    },
    setup() {
        const store = useStore();
        const canvasRef = ref(null);
        const choose = ref('');

        let isDragging = false;
        let offsetX = 0, offsetY = 0;
        let startX = 0, startY = 0;
        let scale = 0;
        const shrink_factor = ref(1);
        const opacity_factor = ref(1);
        const rotationAngle = ref(0);

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

        const frontImg = new Image();
        const backImg = new Image();

        // // 特判router.push
        // if (store.state.img.image) {
        //     store.commit('setfobImg', store.state.img.image);
        //     store.commit('setImage', null);
        // }

        // const uploadImage = () => {
        //     store.commit('setfobImg', store.state.img.image);
        //     store.commit('setImage', null);
        // }

        const draw = () => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(backImg, 0, 0, canvas.width, canvas.height);

            // 设置图像透明度
            ctx.globalAlpha = opacity_factor.value;
            // 绘制前景图片（假设已经加载到 frontImg 变量中）
            ctx.drawImage(frontImg, startX * scale, startY * scale, frontImg.width, frontImg.height);
            // 不影响后面的绘制
            ctx.globalAlpha = 1;
        }

        let originimgwidth = 0;
        let originimgheight = 0;
        const is_processed = ref(false);

        const startMerging = () => {
            const canvas = canvasRef.value;

            backImg.onload = function () {
                canvas.width = backImg.width;
                canvas.height = backImg.height;
                const canvasWindowsWidth = canvas.clientWidth;
                scale = canvas.width / canvasWindowsWidth;
                draw();
            }

            frontImg.onload = function () {
                originimgwidth = frontImg.width;
                originimgheight = frontImg.height;
                canvas.addEventListener('mousedown', handleMouseDown);
                canvas.addEventListener('mousemove', handleMouseMove);
                canvas.addEventListener('mouseup', handleMouseUp);
                canvas.addEventListener('mouseleave', handleMouseUp);
                draw();
                is_processed.value = true;
            }

            // 交换顺序，保证当前img为前景
            if (choose.value === 'no') {
                const temp = new Image();

                temp.onload = function () {
                    img.src = supimg.src;
                    supimg.src = temp.src;
                    backImg.src = supimg.src;
                    frontImg.src = img.src;
                }

                temp.src = img.src;
            }

            else {
                backImg.src = supimg.src;
                frontImg.src = img.src;
            }

            // backImg.onload = () => {
            //     ctx.drawImage(backImg, 0, 0, canvas.width, canvas.height);
            //     ctx.globalCompositeOperation = 'multiply'; // 设置组合模式为 multiply
            //     ctx.drawImage(frontImg, 0, 0, canvas.width, canvas.height);
            // }
        }

        const handleMouseDown = event => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');

            const rect = canvas.getBoundingClientRect();
            console.log("画布大小", canvas.width, canvas.height);
            console.log("鼠标位置", event.clientX, event.clientY);
            console.log("画布偏移", rect.left, rect.top)


            offsetX = event.clientX - rect.left;
            offsetY = event.clientY - rect.top;

            isDragging = true;
        }

        const handleMouseMove = event => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            if (!isDragging) return;
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left - offsetX;
            const y = event.clientY - rect.top - offsetY;

            offsetX += x;
            offsetY += y;

            startX += x
            startY += y

            draw();
        }

        const handleMouseUp = event => {
            isDragging = false;
        }

        const reset_frontImg = () => {
            startX = 0;
            startY = 0;
            shrink_factor.value = 1;
            opacity_factor.value = 1;
            rotationAngle.value = 0;
            draw();
        }

        const handleRoute = () => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(backImg, 0, 0, canvas.width, canvas.height);

            // 保存当前的绘图状态
            ctx.save();

            // 将坐标原点移动到前景图片中心
            const centerX = startX * scale + frontImg.width / 2;
            const centerY = startY * scale + frontImg.height / 2;
            ctx.translate(centerX, centerY);

            // 旋转绘图环境
            const radians = rotationAngle.value * Math.PI / 180; // 将角度转换为弧度
            ctx.rotate(radians);

            // 将坐标原点移动回左上角
            ctx.translate(-centerX, -centerY);

            ctx.globalAlpha = opacity_factor.value;
            // 绘制前景图片
            ctx.drawImage(frontImg, startX * scale, startY * scale, frontImg.width, frontImg.height);
            ctx.globalAlpha = 1;
            // 恢复之前保存的绘图状态
            ctx.restore();
        }

        const is_shared = ref(false);
        const is_saved = ref(false);
        const dlink = ref('');
        const downloadName = ref('');  // 文件名

        const saveCanvasImg = () => {
            const canvas = canvasRef.value;
            let imageDataURL = '';

            imageDataURL = canvas.toDataURL('image/png');
            downloadName.value = 'merge.png'

            store.commit('setsavetool', imageDataURL.split(',')[1]);
            dlink.value = imageDataURL;

            is_saved.value = true;
        }

        const share = () => {
            is_shared.value = true;
        }


        watch(
            () => [shrink_factor.value, opacity_factor.value, rotationAngle.value],  // 多参数监听
            (oldVal, newVal) => {
                frontImg.width = originimgwidth * shrink_factor.value;
                frontImg.height = originimgheight * shrink_factor.value;
                draw();

                if (newVal[2] !== oldVal[2]) handleRoute();
            }
        )


        return {
            choose,
            canvasRef,

            img,
            supimg,
            has_input1,
            has_input2,
            resetImg,
            uploadImage,

            shrink_factor,
            opacity_factor,
            rotationAngle,

            is_saved,
            is_shared,
            dlink,
            downloadName,

            startMerging,
            is_processed,

            reset_frontImg,
            saveCanvasImg,
            share,
        }
    }
}
</script>

<style scoped>
canvas {
    max-width: 100%;
    max-height: auto;
}

.canvas-container {
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
    background-color: gray;
}
</style>