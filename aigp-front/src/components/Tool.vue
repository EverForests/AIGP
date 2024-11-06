<!-- <template>
    <div class="image-container">
        <img v-if="$store.state.img.image" @mousemove="handleMouseMove"
            @mouseout="() => underall.defer(() => $store.commit('setmaskImg', null))" @touchstart="handleMouseMove"
            :src="$store.state.img.image.src" class="image" />
        <img v-if="$store.state.img.maskImg" :src="$store.state.img.maskImg.src" class="mask-image" />
        <div v-if="$store.state.img.maskImg" class="mask-layer"></div>
    </div>
</template> -->

<template>
    <div class="image-container">
        <img v-if="img.src" @mouseleave="() => underall.defer(() => $store.commit('setmaskImg', null))"
            @mousemove="handleMouseMove" @touchstart="handleMouseMove" @click="handleClick" :src="img.src"
            class="image" />
        <img v-if="$store.state.img.maskImg" :src="$store.state.img.maskImg.src" class="mask-image" />
        <canvas ref="canvasRef"></canvas>
    </div>

    <div class="controler" v-if="$store.state.img.id">
        <a-button @click="getmaskImg">开启图像信息捕捉</a-button>
        <div>{{ caputure_status }}</div>
        <a-button @click="mattingSelect">展示扣除图像</a-button>
        <a-button @click="resetMattingSelect">重置</a-button>
    </div>
</template>


<script>
import ImgUpload from './ImgUpload.vue'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useStore } from 'vuex'
import * as underall from 'underscore'

export default {
    name: "Tool",
    emits: ['handleMouseMove', 'handleClick', 'mattingSelect', 'resetMattingSelect'],
    components: {
    },
    props: {
        caputure_status: {
            type: String,
            required: false
        },

        img: {
            type: Image,
            required: true
        }
    },
    setup(props, context) {
        const store = useStore();
        const canvasRef = ref(null);
        const redPoints = ref([]); // 保存红点坐标的数组

        // Determine if we should shrink or grow the images to match the
        // width or the height of the page and setup a ResizeObserver to
        // monitor changes in the size of the page

        // const shouldFitToWidth = ref(false);
        // const bodyEl = document.body;

        // const fitToPage = () => {
        //     const img = store.state.img;
        //     if (!img.image) return;
        //     const imageAspectRatio =
        //         img.width / img.height;
        //     const screenAspectRatio = window.innerWidth / window.innerHeight;
        //     shouldFitToWidth.value = imageAspectRatio > screenAspectRatio;
        // };

        // const resizeObserver = new ResizeObserver((entries) => {
        //     for (const entry of entries) {
        //         if (entry.target === bodyEl) {
        //             fitToPage();
        //         }
        //     }
        // });

        const getClick = (x, y) => {
            const clickType = 1;
            return { x, y, clickType };
        };

        const getMousePosition = e => {
            let el = e.target;
            const rect = el.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;

            const imageScale = props.img
                ? props.img.width / el.offsetWidth
                : 1;
            x *= imageScale;
            y *= imageScale;
            return getClick(x, y);
        }

        const handleMouseMove = e => {
            const p = getMousePosition(e);
            context.emit('handleMouseMove', p);
        }

        let scale = 1;
        const handleClick = e => {
            const p = getMousePosition(e);
            context.emit('handleClick', p);

            redPoints.value.push({ x: p.x, y: p.y });
            const canvas = canvasRef.value;
            console.log(canvas);
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            canvas.width = props.img.width;
            canvas.height = props.img.height;

            scale = canvas.width / canvas.clientWidth;

            ctx.fillStyle = 'red';
            for (const p of redPoints.value) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, 5 * scale, 0, 2 * Math.PI);
                ctx.fill();
            }
        }

        const mattingSelect = e => {
            context.emit('mattingSelect');
        }

        const clearRedPoint = e => {
            redPoints.value = [];
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        const resetMattingSelect = () => {
            clearRedPoint();
            context.emit('resetMattingSelect');
        }

        const getmaskImg = () => {
            context.emit('getmaskImg');
        }

        // onMounted(async () => {
        //     fitToPage();
        //     resizeObserver.observe(bodyEl);
        // });

        // onUnmounted(async () => {
        //     resizeObserver.unobserve(bodyEl);
        // });

        // watch(
        //     () => store.state.img.click_list,
        //     () => {
        //         fitToPage();
        //         resizeObserver.observe(bodyEl);
        //     }
        // );

        return {
            // imageClass,
            // maskImageClasses,
            // shouldFitToWidth,
            canvasRef,
            handleMouseMove,
            handleClick,
            mattingSelect,
            resetMattingSelect,
            getmaskImg,
            underall,
        }
    },
}
</script>

<style scoped>
.image-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: gray;
}

.image {
    max-width: 100%;
    /* 图片的最大宽度为父容器的宽度 */
    max-height: 100%;
    /* 图片的最大高度为父容器的高度 */

}

.mask-image {
    position: absolute;
    opacity: 0.4;
    pointer-events: none;
    max-width: 100%;
    /* 图片的最大宽度为父容器的宽度 */
    max-height: 100%;
    /* 图片的最大高度为父容器的高度 */
}

canvas {
    position: absolute;
    pointer-events: none;
    max-width: 100%;
    /* 图片的最大宽度为父容器的宽度 */
    max-height: 100%;
    /* 图片的最大高度为父容器的高度 */
}
</style>