<template>
    <div class="card-list">
        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">基础工具</h5>
                <!-- <p class="card-text">基础工具</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'baseedit' }">Go there</router-link>
            </div>
        </div>

        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">图像抠取</h5>
                <!-- <p class="card-text">图像抠取</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'imgmatting' }">Go there</router-link>
            </div>
        </div>

        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">图像融合</h5>
                <!-- <p class="card-text">图像融合</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'imgmerge' }">Go there</router-link>
            </div>
        </div>

        <div class="card" style="width: 18rem;">
            <img src="/imggenerate/img2img.png" class="card-img-top" alt="123">
            <div class="card-body">
                <h5 class="card-title">图像压缩</h5>
                <!-- <p class="card-text">图像压缩</p> -->
                <router-link class="link btn btn-primary" :to="{ name: 'imgcompress' }">Go there</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import BaseEditView from './ImgEdit/BaseEditView.vue';
import ImgMattingView from './ImgEdit/ImgMattingView.vue';
import ImgMergeView from './ImgEdit/ImgMergeView.vue';
import ImgCompressView from './ImgEdit/ImgCompressView.vue';

export default {
    name: "ImgEditView",
    components: {
        BaseEditView,
        ImgMattingView,
        ImgMergeView,
        ImgCompressView,
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