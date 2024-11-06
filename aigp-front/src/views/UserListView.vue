<template>
    <ContentBase>
        <div class="image-container">
            <img v-for="img in showlist" :key="img.id" @click="open_img_profile(img)" :src="img.image" :alt="img.title"
                data-bs-toggle="modal" data-bs-target="#exampleModal">
        </div>

        <!-- 模态框 -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">图片信息</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="container-fluid">
                            <div class="row">
                                <img class="col-8 ms-auto" :src="currentImgSrc" alt="currentImg">
                                <div class="col-4 ms-auto img-info">
                                    <div>编号： {{ currentImgId }}</div>
                                    <div>标题：{{ currentImgTitle }}</div>
                                    <div>创建时间： {{ currentImgDate }}</div>
                                    <div @click="open_user_profile" data-bs-dismiss="modal" aria-label="Close">作者：{{
                                        currentImgUser }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                        <button type="button" class="btn btn-primary">跳转处理</button>
                    </div>
                </div>
            </div>
        </div>

    </ContentBase>
</template>

<script>
import { useStore } from 'vuex';
import ContentBase from '../components/ContentBase'
import { ref, reactive } from 'vue'
import $ from 'jquery'
import router from '@/router';

export default {
    name: "UserListView",
    components: {
        ContentBase
    },
    setup() {
        const showlist = ref({});
        const store = useStore();
        $.ajax({
            url: "/agapi/socialimg/",
            type: "GET",
            success(resp) {
                showlist.value = resp;
            }
        });


        const currentImgSrc = ref('');
        const currentImgId = ref('');
        const currentImgTitle = ref('');
        const currentImgDate = ref('');
        const currentImgUser = ref('');

        const open_img_profile = img => {
            currentImgSrc.value = img.image;
            currentImgId.value = img.id;
            currentImgTitle.value = img.title;
            currentImgDate.value = img.create_date;
            currentImgUser.value = img.username;
        }

        const open_user_profile = async () => [
            await $.ajax({
                url: "/agapi/searchuserid/",
                type: "GET",
                data: {
                    "username": currentImgUser.value
                },
                success(resp) {
                    router.push({ name: 'userprofile', params: { userId: resp.id } })
                }
            })
        ]

        return {
            showlist,

            currentImgSrc,
            currentImgId,
            currentImgTitle,
            currentImgDate,
            currentImgUser,

            open_img_profile,
            open_user_profile,
        }
    }
}
</script>

<style scoped>
.image-container {
    display: flex;
    flex-wrap: wrap;
}

.image-container img {
    width: calc(33.333% - 10px);
    /* 假设你想要每行三张图片，并且图片之间有10px的间距 */
    margin-right: 10px;
    /* 图片右边距 */
    margin-bottom: 10px;
    /* 图片下边距 */
    /* 根据需要设置图片的宽度和高度 */
    /* 例如，如果你想让图片高度自适应宽度，可以设置 object-fit 属性 */
    object-fit: cover;
    cursor: pointer;
}
</style>