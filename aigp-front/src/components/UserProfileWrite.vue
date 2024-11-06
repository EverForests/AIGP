<template>
    <div class="card">
        <div class="card-body">
            <input type="file" accept="image/*" ref="fileInput">
            <label for="imgtitle"></label>
            <input type="text" id="imgtitle" name="imgtitle" placeholder="请输入图片标题～" v-model="title">
            <button @click="postImg">上传图片</button>
            <div>{{ result }}</div>
        </div>
    </div>
</template>


<script>
import { useStore } from 'vuex'
import { ref } from 'vue'
import $ from 'jquery'

export default {
    name: "UserProfileWrite",
    components: {

    },

    setup(props, context) {
        let fileInput = ref(null);
        let result = ref('');
        const store = useStore();
        let title = ref('');

        const postImg = () => {
            const file = fileInput.value.files[0];
            const filename = file.name;

            let imageData = new FormData();
            imageData.append('username', store.state.user.username);
            imageData.append('title', title.value);
            imageData.append('image', file);
            imageData.append('flag', true);

            $.ajax({
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
                        result.value = '已成功上传图片: ' + filename;
                        context.emit('post_a_image', resp);
                    }
                }
            })
        }


        return {
            fileInput,
            result,
            title,
            postImg,
        }
    }
}
</script>


<style scoped>
button {
    margin-top: 10px
}
</style>