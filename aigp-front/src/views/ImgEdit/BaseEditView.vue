<template>
    <a-layout class="layout">
        <a-layout-sider :style="siderStyle">

            <div v-if="has_input">
                当前处理图片：
                <img :src="img.src" alt="" style="width: 100%;">
                <a-button @click="resetImg">重新上传图片</a-button>
            </div>

            <ImgUpload v-if="!has_input" style="width: 100%;" @uploadImage="uploadImage" />
            <hr>

            <a-button type="primary" @click="startEditing">开始编辑</a-button>
            <a-button type="primary" shape="circle" @click="showModal"
                style="background-color: gray; margin-left: 20px;">?</a-button>

            <div>
                <a-modal v-model:open="open" title="参数说明" @ok="handleOk">
                    伸缩系数: 调整图像大小 <br>
                    旋转角度: 调整图像方位 <br>
                    透明度: 调整图像清晰度 <br>
                    <br>
                    注：在使用文本添加、图像擦除或图像裁剪时，同一时间仅能打开一个功能
                </a-modal>
            </div>

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
                    <router-link class="nav-link" :to="{ name: 'baseedit' }">基础编辑</router-link>
                </a-breadcrumb-item>
            </a-breadcrumb>

            <div :style="{ background: '#fff', padding: '24px', height: '70vh' }">
                <div class="canvas-container">
                    <canvas ref="canvasRef"></canvas>
                </div>
            </div>

            <div v-if="has_input">
                <a-button @click="saveCanvasImg">保存图像</a-button>
                <a v-if="is_saved" :href="dlink" download="baseedit.png">baseedit.png</a>
                <a-button @click="share" v-if="is_saved">
                    分享图像
                </a-button>
                <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                    :options="[{ id: 2, name: 'imgmatting' }, { id: 3, name: 'imgmerge' }, { id: 4, name: 'imgcompress' }, { id: 5, name: 'img2img' }, { id: 6, name: 'imgbig' }]"
                    :hide_reset="true" />
            </div>

        </a-layout-content>

        <a-layout-sider :style="siderStyle">
            <div class="tools">
                <div>
                    伸缩系数
                    <!-- <label for="shrink_factor" class="range-label">伸缩系数: {{ shrink_factor }}</label>
                    <input v-model="shrink_factor" type="range" id="shrink_factor" min="0" max="5" step="0.1"> -->
                    <a-slider v-model:value="shrink_factor" :min="0" :max="5" :step="0.1"
                        style="margin: 0 16px 0 16px" />
                    <a-input-number v-model:value="shrink_factor" :min="1" :max="20" :step="0.1" />
                </div>

                <hr>

                <div>
                    旋转调整
                    <!-- <label for="rotationAngle" class="range-label">旋转角度: {{ rotationAngle }}</label>
                    <input v-model="rotationAngle" type="range" id="rotationAngle" min="0" max="360" step="1"> -->
                    <a-slider v-model:value="rotationAngle" :min="0" :max="360" :step="1"
                        style="margin: 0 16px 0 16px" />
                    <a-input-number v-model:value="rotationAngle" :min="0" :max="360" :step="1" />
                </div>

                <hr>

                <div>
                    调节透明度
                    <!-- <label for="opacity_factor" class="range-label">不透明度: {{ opacity_factor }}</label>
                    <input v-model="opacity_factor" type="range" id="opacity_factor" min="0" max="1" step="0.1"> -->
                    <a-slider v-model:value="opacity_factor" :min="0" :max="1" :step="0.1"
                        style="margin: 0 16px 0 16px" />
                    <a-input-number v-model:value="opacity_factor" :min="0" :max="1" :step="0.1" />
                </div>

                <hr>

                <div>
                    <a-button @click="addText">文本添加: {{ is_addText ? "开" : "关" }}</a-button>
                    <a-button @click="reset_text">重置文本</a-button>
                    <div v-if="show_textBox">
                        <!-- <label for="textBox" class="textBox"></label>
                        <textarea ref="textBox" v-model="text_content" name="textBox" id="textBox" cols="30" rows="1"
                            class="textBox"></textarea> -->
                        <a-space>
                            <a-input v-model:value="text_content" placeholder="编辑文本"></a-input>
                        </a-space>
                    </div>
                </div>

                <hr>

                <div>
                    <a-button @click="erase">图像擦除: {{ is_erase ? "开" : "关" }}</a-button>
                    <a-button @click="reset_erase">重置擦除</a-button>
                </div>

                <hr>

                <div>
                    <a-button @click="crop">图像裁剪: {{ is_crop ? "开" : "关" }}</a-button>
                    <a-button @click="reset_crop">重置裁剪</a-button>
                </div>
            </div>
        </a-layout-sider>
    </a-layout>

    <!-- <div class="container-fluid">
    <div class="show-stage row">
        <h1>基础工具</h1>
        <div class="col-2 first-col">
            <ImgUpload />
            <hr>
            <a-button @click="startEditing">开始编辑</a-button>
        </div>

        <div class="col-8 second-col">
            <div class="canvas-container">
                <canvas ref="canvasRef"></canvas>
            </div>
        </div>

        <div class="col-2 third-col">
            <div class="tools">
                <div>
                    调节图像大小
                    <label for="shrink_factor" class="range-label">伸缩系数: {{ shrink_factor }}</label>
                    <input v-model="shrink_factor" type="range" id="shrink_factor" min="0" max="5" step="0.1">
                </div>

                <div>
                    旋转调整
                    <label for="rotationAngle" class="range-label">旋转角度: {{ rotationAngle }}</label>
                    <input v-model="rotationAngle" type="range" id="rotationAngle" min="0" max="360" step="1">
                </div>

                <div>
                    调节透明度
                    <label for="opacity_factor" class="range-label">不透明度: {{ opacity_factor }}</label>
                    <input v-model="opacity_factor" type="range" id="opacity_factor" min="0" max="1" step="0.1">
                </div>

                <div>
                    <a-button @click="addText">文本添加: {{ is_addText ? "开" : "关" }}</a-button>
                    <a-button @click="reset_text">重置文本内容</a-button>
                    <div v-if="show_textBox">
                        <label for="textBox" class="textBox"></label>
                        <textarea ref="textBox" v-model="text_content" name="textBox" id="textBox" cols="30" rows="1"
                            class="textBox"></textarea>
                    </div>
                </div>

                <div>
                    <a-button @click="erase">橡皮擦: {{ is_erase ? "开" : "关" }}</a-button>
                    <a-button @click="reset_erase">重置擦除</a-button>
                </div>

                <div>
                    <a-button @click="crop">图像裁剪: {{ is_crop ? "开" : "关" }}</a-button>
                    <a-button @click="reset_crop">重置裁剪</a-button>
                </div>
            </div>

            <div>
                <a-button @click="saveCanvasImg">保存图像</a-button>
                <a v-if="is_saved" :href="dlink" download="baseedit.png">baseedit.png</a>
                <a-button @click="share" v-if="is_saved">
                    分享图像
                    <ImgUpload v-if="is_shared" :image="$store.state.img.savetool" :shared=true
                        :options="[{ id: 3, name: 'imgmatting' }, { id: 4, name: 'imgmerge' }, { id: 6, name: 'img2img' }]"
                        :hide_reset="true" />
                </a-button>
            </div>
        </div>
    </div>
    </div> -->


</template>

<script>
import ImgUpload from '@/components/ImgUpload.vue';
import ContentBase from '@/components/ContentBase.vue';
import { ref, onMounted, watch, reactive } from 'vue';
import { useStore } from 'vuex';
export default {
    name: "BaseEditView",
    components: {
        ImgUpload,
        ContentBase
    },
    setup() {
        const store = useStore();
        const canvasRef = ref(null);

        const img = new Image();  // 组件图片接收变量
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

        // 开始编辑
        let scale = 1;  // 渲染伸缩比
        const startEditing = () => {
            const canvas = canvasRef.value;

            canvas.width = img.width;
            canvas.height = img.height;

            draw();

            const canvasWindowsWidth = canvas.clientWidth;
            scale = canvas.width / canvasWindowsWidth;
        }

        const draw = () => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;

            ctx.save();

            ctx.translate(centerX, centerY);
            const radians = rotationAngle.value * Math.PI / 180; // 将角度转换为弧度
            ctx.rotate(radians);
            ctx.translate(-centerX, -centerY);

            ctx.globalAlpha = opacity_factor.value;

            ctx.drawImage(img, centerX - img.width / 2, centerY - img.height / 2, img.width, img.height);

            ctx.globalAlpha = 1;

            ctx.restore();

            if (text_content.value) {
                ctx.fillStyle = "red";
                ctx.strokeStyle = "blue";
                ctx.lineWidth = 5;
                ctx.save();
                ctx.beginPath();
                ctx.font = `${50 * scale}px orbitron`;
                ctx.fillText(text_content.value, textPX * scale, textPY * scale);
                ctx.restore();
                ctx.closePath();
            }

            if (erase_list.length !== 0) {
                erase_list.forEach(pos => {
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(pos.x * scale, pos.y * scale, 10 * scale, 0, Math.PI * 2);
                    ctx.clip();
                    // ctx.fillStyle = 'gray';
                    // ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.restore();
                    ctx.closePath();
                })
            }

            if (is_crop.value && is_move) {
                ctx.beginPath();
                ctx.rect(cropStartPX * scale, cropStartPY * scale, cropEndPX * scale - cropStartPX * scale, cropEndPY * scale - cropStartPY * scale);
                // 设置边框样式
                ctx.lineWidth = 2; // 边框宽度
                ctx.strokeStyle = 'red'; // 边框颜色
                // 绘制边框
                ctx.stroke();
                ctx.closePath();
            }

            if (crop_completed.value) {
                ctx.save();
                ctx.beginPath();
                // 绘制掩膜
                ctx.globalCompositeOperation = 'destination-in'; // 设置合成操作为"destination-in"，将绘制限制在原始图像上
                ctx.rect(cropStartPX * scale, cropStartPY * scale, cropEndPX * scale - cropStartPX * scale, cropEndPY * scale - cropStartPY * scale);
                ctx.fill(); // 填充区域
                ctx.restore();
                ctx.closePath();
            }
        }

        const shrink_factor = ref(1);
        const rotationAngle = ref(0);
        const opacity_factor = ref(1);

        // 控制文本添加
        const is_addText = ref(false);
        const show_textBox = ref(false);
        const text_content = ref('');

        let textPX = 0;
        let textPY = 0;

        const addText = () => {
            if (is_erase.value || is_crop.value) return;
            const canvas = canvasRef.value;
            if (!is_addText.value) {
                canvas.addEventListener('mousedown', handleMouseDown_Text);
                is_addText.value = true;
            }

            else {
                show_textBox.value = false;
                canvas.removeEventListener('mousedown', handleMouseDown_Text);
                is_addText.value = false;
            }
        }

        const reset_text = () => {
            text_content.value = '';
        }

        const handleMouseDown_Text = event => {
            if (show_textBox.value) {
                show_textBox.value = false;
                draw();
            }

            else {
                const canvas = canvasRef.value;
                const rect = canvas.getBoundingClientRect();

                // 更新文本位置
                textPX = event.clientX - rect.left;
                textPY = event.clientY - rect.top;

                show_textBox.value = true;
            }
        }

        // 橡皮擦
        const is_erase = ref(false);
        const erase_list = reactive([]);
        let erasePX = 0;
        let erasePY = 0;
        let is_move = false;  // 图像裁剪共用

        const erase = () => {
            if (is_addText.value || is_crop.value) return;
            const canvas = canvasRef.value;
            if (!is_erase.value) {
                canvas.addEventListener('mousedown', handleMouseDown_Erase);
                canvas.addEventListener('mousemove', handleMouseMove_Erase);
                canvas.addEventListener('mouseup', handleMouseUp_Erase);
                is_erase.value = true;
            }

            else {
                is_erase.value = false;
                canvas.removeEventListener('mousedown', handleMouseDown_Erase);
                canvas.removeEventListener('mousemove', handleMouseMove_Erase);
                canvas.removeEventListener('mouseup', handleMouseUp_Erase);
            }
        }

        const reset_erase = () => {
            erase_list.splice(0, erase_list.length);
            console.log(erase_list);
        }

        const handleMouseDown_Erase = event => {
            is_move = true;

            const canvas = canvasRef.value;
            const rect = canvas.getBoundingClientRect();

            erasePX = event.clientX - rect.left;
            erasePY = event.clientY - rect.top;

            erase_list.push({ x: erasePX, y: erasePY });
        }

        const handleMouseMove_Erase = event => {
            if (!is_move) return;

            const canvas = canvasRef.value;
            const rect = canvas.getBoundingClientRect();

            erasePX = event.clientX - rect.left;
            erasePY = event.clientY - rect.top;

            erase_list.push({ x: erasePX, y: erasePY });
        }

        const handleMouseUp_Erase = event => {
            is_move = false;
        }

        // 图像裁剪
        const is_crop = ref(false);
        const crop_completed = ref(false);
        let cropStartPX = 0;
        let cropStartPY = 0;
        let cropEndPX = 0;
        let cropEndPY = 0;

        const crop = () => {
            if (is_addText.value || is_erase.value) return;
            const canvas = canvasRef.value;
            if (!is_crop.value) {
                canvas.addEventListener('mousedown', handleMouseDown_Crop);
                canvas.addEventListener('mousemove', handleMouseMove_Crop);
                canvas.addEventListener('mouseup', handleMouseUp_Crop);
                is_crop.value = true;
            }

            else {
                is_crop.value = false;
                canvas.removeEventListener('mousedown', handleMouseDown_Crop);
                canvas.removeEventListener('mousemove', handleMouseMove_Crop);
                canvas.removeEventListener('mouseup', handleMouseUp_Crop);
            }
        }

        const reset_crop = () => {
            const canvas = canvasRef.value;
            crop_completed.value = false;
            canvas.addEventListener('mousedown', handleMouseDown_Crop);
            canvas.addEventListener('mousemove', handleMouseMove_Crop);
            canvas.addEventListener('mouseup', handleMouseUp_Crop);
            draw();
        }

        const handleMouseDown_Crop = event => {
            const canvas = canvasRef.value;
            const rect = canvas.getBoundingClientRect();

            cropStartPX = event.clientX - rect.left;
            cropStartPY = event.clientY - rect.top;

            cropEndPX = cropStartPX;
            cropEndPY = cropStartPY;

            is_move = true;
        }

        const handleMouseMove_Crop = event => {
            if (!is_move) return;

            const canvas = canvasRef.value;
            const rect = canvas.getBoundingClientRect();

            // 更新终点
            cropEndPX = event.clientX - rect.left;
            cropEndPY = event.clientY - rect.top;

            draw();
        }

        const handleMouseUp_Crop = event => {
            is_move = false;
            const canvas = canvasRef.value;
            crop_completed.value = true;
            draw();
            canvas.removeEventListener('mousedown', handleMouseDown_Crop);
            canvas.removeEventListener('mousemove', handleMouseMove_Crop);
            canvas.removeEventListener('mouseup', handleMouseUp_Crop);
        }

        // 保存图像
        const is_shared = ref(false);
        const is_saved = ref(false);
        const dlink = ref('');

        const saveCanvasImg = () => {
            const canvas = canvasRef.value;
            // ctx.transform(cropStartPX * scale, cropStartPY * scale);
            // canvas.width = cropEndPX * scale - cropStartPX * scale;
            // canvas.height = cropEndPY * scale - cropStartPY * scale;
            const imageDataURL = canvas.toDataURL(); // 将画布内容转换为数据 URL

            store.commit('setsavetool', imageDataURL.split(',')[1]);

            dlink.value = imageDataURL;

            is_saved.value = true;
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
            () => [shrink_factor.value, rotationAngle.value, opacity_factor.value, text_content.value, erase_list.length],  // 多参数监听
            (oldVal, newVal) => {
                img.width = store.state.img.image.width * shrink_factor.value;
                img.height = store.state.img.image.height * shrink_factor.value;
                draw();
            }
        )

        return {
            canvasRef,

            has_input,
            img,
            uploadImage,
            resetImg,

            startEditing,

            shrink_factor,
            rotationAngle,
            opacity_factor,

            show_textBox,
            is_addText,
            text_content,
            addText,
            reset_text,

            is_erase,
            erase,
            reset_erase,

            is_crop,
            crop,
            reset_crop,

            is_saved,
            is_shared,
            dlink,
            saveCanvasImg,
            share,

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
    background-color: gray;
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
    /* 水平和垂直居中 */
}

canvas {
    max-width: 100%;
    max-height: auto;
}

/* .textBox {
    font: 28px orbitron;
    word-break: break-all;
    background-color: transparent;
    resize: none;
}

.show-stage {
    margin-top: 20px;
}

.show-stage>div {
    border-left: 1px solid;
}

.first-col {
    border-left: none;
    margin-left: -1px;
}

.third-col {
    border-left: none;
    margin-right: -1px;
} */

.layout {
    height: 100vh;
}
</style>