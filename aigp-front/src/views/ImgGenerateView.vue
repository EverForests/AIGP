<template>
    <div class="card-list">
        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">文生图</h5>
                <!-- <p class="card-text">文生图是一款图像编辑工具，它可以帮助您轻松编辑图像，添加各种滤镜、调整色调、裁剪图像等。</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'text2img' }">Go there</router-link>
            </div>
        </div>

        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">图生图</h5>
                <!-- <p class="card-text">图生图是一款方便易用的批量处理工具，它可以让您处理图像，节省您的时间和精力。</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'img2img' }">Go there</router-link>
            </div>
        </div>

        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">图像无损放大</h5>
                <!-- <p class="card-text">图像无损放大</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'imgbig' }">Go there</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import Text2ImgView from './ImgGenerate/Text2ImgView.vue';
import Img2ImgView from './ImgGenerate/Img2ImgView.vue';
import ImgBigView from './ImgGenerate/ImgBigView.vue';

export default {
    name: "ImgGenerateView",
    components: {
        Text2ImgView,
        Img2ImgView,
        ImgBigView,
    }
}
</script>

<style scoped>
.card-list {
    display: flex;
    justify-content: center;
    align-items: stretch;
}

.card {
    margin: 30px;
}

.card-img-top {
    height: 100%;
}
</style>