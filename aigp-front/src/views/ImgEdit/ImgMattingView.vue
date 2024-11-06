<template>
    <div class="show-stage">
        <Stage />
    </div>
</template>

<script>
import Stage from '@/components/Stage.vue'
import ImgUpload from '@/components/ImgUpload.vue'
import ContentBase from '@/components/ContentBase.vue';

export default {
    name: "ImgMattingView",
    components: {
        ImgUpload,
        Stage,
        ContentBase,
    },
    setup() {
    }


}
</script>

<style scoped>
.show-stage {
    margin-top: 20px;
}
</style>