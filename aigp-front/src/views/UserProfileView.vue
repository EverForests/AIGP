<template>
    <ContentBase>
        <div class="row">
            <div class="col-3">
                <UserProfileInfo :user="user" @follow="follow" @unfollow="unfollow" />
                <UserProfileWrite v-if="is_me" @post_a_image="post_a_image" />
            </div>
            <div class="col-9">
                <UserProfilePosts :is_me="is_me" :posts="posts" @delete_a_image="delete_a_image" />
            </div>
        </div>
    </ContentBase>
</template>

<script>
import ContentBase from '../components/ContentBase'
import UserProfileInfo from '@/components/UserProfileInfo.vue';
import UserProfilePosts from '@/components/UserProfilePosts.vue';
import UserProfileWrite from '@/components/UserProfileWrite.vue';
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import $ from 'jquery'
import { computed, reactive } from 'vue'

export default {
    name: "UserProfileView",

    components: {
        ContentBase,
        UserProfileInfo,
        UserProfilePosts,
        UserProfileWrite,
    },

    setup() {
        const route = useRoute();
        const store = useStore();

        const userId = parseInt(route.params.userId);

        const user = reactive({});
        const posts = reactive({});

        // 更新user和posts
        $.ajax({
            url: "/agapi/getinfo/",
            type: "GET",
            data: {
                user_id: userId,
            },
            headers: {
                'Authorization': "Bearer " + store.state.user.access,
            },

            success(resp) {
                user.id = resp.id;
                user.username = resp.username;
                user.photo = resp.photo;
                user.followerCount = resp.followerCount;
                user.is_followed = resp.is_followed;
                console.log(user.is_followed);
            }
        })

        $.ajax({
            url: "/agapi/getimglist/",
            type: "GET",
            data: {
                user_id: userId,
            },
            headers: {
                'Authorization': "Bearer " + store.state.user.access,
            },
            success(resp) {
                posts.count = resp.length;
                posts.posts = resp.slice().reverse();  // 新图片优先
            }
        });

        const follow = () => {
            if (user.is_followed) return;
            user.is_followed = true;
            user.followerCount++;
        }

        const unfollow = () => {
            if (!user.is_followed) return;
            user.is_followed = false;
            user.followerCount--;
        }

        const post_a_image = data => {
            posts.count++;
            posts.posts.unshift({
                id: data.id,
                title: data.title,
                image: data.image,
                create_date: data.create_date,
                flag: data.flag,
                username: data.username
            })
        }

        const delete_a_image = post_id => {
            posts.posts = posts.posts.filter(post => post.id != post_id);
            posts.count = posts.posts.length;
        }

        const is_me = computed(() => user.id === store.state.user.id);


        return {
            user,
            posts,
            follow,
            unfollow,
            post_a_image,
            delete_a_image,
            is_me,
        }
    }
}
</script>

<style scoped></style>