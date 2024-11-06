<template>
    <ImgUpload v-if="is_processed" :imginfo="imginfo" />

    <button v-if="op.find(item => item.id === 1) !== undefined" @click="switch_to_baseedit">继续进行基础图像编辑</button>
    <button v-if="op.find(item => item.id === 3) !== undefined" @click="switch_to_imgmatting">继续进行图像扣除</button>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import ImgUpload from '@/components/ImgUpload.vue'
import router from '@/router'

export default {
    name: "FunctionSwitch",
    components: {
        ImgUpload,
    },
    props: {
        // image data
        image: {
            type: null,
            required: true,
        },

        // object array {id, name}
        options: {
            type: Array,
            required: true,
        }
    },
    setup(props) {
        let imginfo = reactive({});
        const op = props.options;
        const is_processed = ref(false);

        const b64topng = (str) => {
            const byteCharacters = atob(str);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            // 创建 Blob 对象，表示二进制数据
            const blob = new Blob([byteArray], { type: 'image/png' });

            return blob;
        }

        const switch_to_baseedit = () => {
            router.push({ name: 'baseedit' });
        }

        const switch_to_imgmatting = () => {
            router.push({ name: 'imgmatting' });
        }

        watch(
            () => props.image,
            () => {
                let image = props.image;
                if (typeof props.image === 'string') {
                    image = b64topng(props.image);
                }
                imginfo.image = image;
                imginfo.flag = true;
                is_processed.value = true
            }
        )

        return {
            imginfo,
            op,
            is_processed,
            switch_to_baseedit,
            switch_to_imgmatting
        }
    }
}
</script>

<style></style>