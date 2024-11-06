<template>
    <div class="card">
        <div class="card-body">
            <div v-for="post in posts.posts" :key="post.id">
                <div class="card single-post">
                    <div class="card-body">
                        <img :src=post.image alt="post.title">
                        <button v-if="is_me" @click="delete_a_image(post.id)" type="button"
                            class="btn btn-danger btn-sm">删除图片</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { useStore } from 'vuex'
import $ from 'jquery'
export default {
    name: "UserProfilePosts",
    components: {

    },

    props: {
        is_me: {
            type: Boolean,
            required: true
        },

        posts: {
            type: Object,
            required: true
        }
    },

    setup(props, context) {
        const store = useStore();
        const delete_a_image = post_id => {
            $.ajax({
                url: "/agapi/deleteimg/",
                type: "DELETE",
                data: {
                    post_id
                },
                headers: {
                    'Authorization': "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if (resp.result === "success") {
                        context.emit('delete_a_image', post_id);
                    }
                }
            })
        }
        return {
            delete_a_image,
        }
    }
}
</script>


<style scoped>
.single-post {
    margin-bottom: 10px;
}

button {
    float: right;
}

img {
    height: 100%;
    width: 100%;
}
</style>