<template>
    <div v-if="!image && !$store.state.img.image">
        <!-- <h3>上传图片</h3> -->
        <input style="width: 100%;" type="file" accept="image/*" ref="fileInput">
        <a-button @click="uploadImage">上传</a-button>
        <div>{{ upload_result }}</div>
        <!-- <img v-if="$store.state.img.image" :src="$store.state.img.image.src" alt="Uploaded Image"
            style="max-width: 300px;"> -->
    </div>

    <!-- <div v-if="!image && $store.state.img.image">
        <img :src="$store.state.img.image.src" alt="Uploaded Image" style="max-width: 300px;">
    </div> -->

    <div v-if="image">
        <!-- <label for="filename" class="filename">请输入文件名: </label> -->
        <!-- <input v-model="filename" type="text" id="filename"> -->
        请输入文件名
        <a-space>
            <a-input v-model:value="filename" placeholder="文件名" />
        </a-space>
        <a-button @click="uploadImage">上传</a-button>
        <div>{{ upload_result }}</div>
    </div>

    <div v-if="op && is_uploaded">
        <a-button v-if="op.find(item => item.id === 1)" @click="switch_to_baseedit">继续进行基础图像编辑</a-button>
        <a-button v-if="op.find(item => item.id === 2)" @click="switch_to_imgmatting">继续进行图像扣取</a-button>
        <a-button v-if="op.find(item => item.id === 3)" @click="switch_to_imgmerge">继续进行图像融合</a-button>
        <a-button v-if="op.find(item => item.id === 4)" @click="switch_to_imgcompress">继续进行图像压缩</a-button>
        <a-button v-if="op.find(item => item.id === 5)" @click="switch_to_img2img">继续进行图生图</a-button>
        <a-button v-if="op.find(item => item.id === 6)" @click="switch_to_imgbig">继续进行图像放大</a-button>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
import $ from 'jquery'
import { handleImageScale } from '@/helpers/scaleHelpers';
import { watch } from 'vue';
import router from '@/router'

export default {
    name: 'ImgUpload',
    emits: ['uploadImage'],
    props: {
        // rawdata
        image: {
            type: null,
            required: false
        },

        options: {
            type: Array,
            required: false
        },

        shared: {
            type: Boolean,
            required: false
        },

        hide_reset: {
            type: Boolean,
            required: false
        }
    },
    setup(props, context) {
        const store = useStore()

        let fileInput = ref(null);
        let filename = ref('img');

        let upload_result = ref('');
        let url = ref(null);
        const is_uploaded = ref(false);

        const op = props.options;

        const uploadImage = async () => {
            upload_result.value = '请稍候...'
            let file = null;
            let flag = false;

            if (!props.image) {
                file = fileInput.value.files[0];
                filename.value = file.name.substring(0, file.name.lastIndexOf('.'));
            }

            else {
                file = props.image;
                if (typeof props.image[0] === 'string') file = b64topng(props.image);
                flag = props.shared;
            }

            let imageData = new FormData();
            imageData.append('username', store.state.user.username);
            imageData.append('title', filename.value);
            imageData.append('image', file, filename.value + ".png");
            imageData.append('flag', flag);  // 这里上传原始图片

            await $.ajax({
                url: "/agapi/postimg/",
                type: "POST",
                data: imageData,
                processData: false,  // 禁止 jQuery 对 FormData 进行处理
                contentType: false,  // 禁止 jQuery 设置请求头的 Content-Type
                headers: {
                    // 'Content-Type': 'multipart/form-data',
                    'Authorization': "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if (resp.result === "success") {
                        upload_result.value = '图片上传成功: ' + filename.value;
                        store.commit('setImgId', resp.id);

                        url.value = new URL(resp.image, location.origin)
                    }

                    else {
                        upload_result.value = '图片上传失败'
                    }
                }
            })
        };

        // 加载原始图片至展示框
        const loadImage = () => {
            try {
                const img = new Image();
                img.onload = () => {
                    const { height, width, samScale } = handleImageScale(img);
                    img.width = width;
                    img.height = height;
                    store.commit('setImage', img);
                    is_uploaded.value = true;
                    context.emit('uploadImage');
                };
                img.src = url.value.href;
            } catch (error) {
                console.log(1, error);
            }
        }

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
            if (!store.state.img.image) { upload_result.value = "请先为图片命名"; return }
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'baseedit' });
        }

        const switch_to_imgmatting = () => {
            if (!store.state.img.image) { upload_result.value = "请先为图片命名"; return }
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'imgmatting' });
        }

        const switch_to_imgmerge = () => {
            if (!store.state.img.image) { upload_result.value = "请先为图片命名"; return }
            store.commit('setfobImg', store.state.img.image);
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'imgmerge' });
        }

        const switch_to_imgcompress = () => {
            if (!store.state.img.image) { upload_result.value = "请先为图片命名"; return }
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'imgcompress' });
        }

        const switch_to_img2img = () => {
            if (!store.state.img.image) { upload_result.value = "请先为图片命名"; return }
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'img2img' });
        }

        const switch_to_imgbig = () => {
            if (!store.state.img.image) { upload_result.value = "请先为图片命名"; return }
            store.state.img.is_PushNavigation = true;
            router.push({ name: 'imgbig' });
        }

        const resetImg = () => {
            upload_result.value = '';
            store.state.img.image = null;
            store.state.img.fobImg = null;
            store.state.img.originImg = null;
        }

        watch(
            () => store.state.img.id,
            () => {
                loadImage();
            }
        );

        return {
            fileInput,
            filename,
            upload_result,
            op,
            is_uploaded,
            uploadImage,
            switch_to_baseedit,
            switch_to_imgmatting,
            switch_to_imgmerge,
            switch_to_imgcompress,
            switch_to_img2img,
            switch_to_imgbig,
            resetImg,
        };
    }
};
</script>

<style scoped>
img {
    width: 100%;
    border: 1px solid black;
    background-color: gray;
}
</style>
