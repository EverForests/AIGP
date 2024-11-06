<template>
    <div class="card">
        <div class="card-body">
            <div class="row">
                <div class="col-3 img-field">
                    <img class="fluid" :src="user.photo" alt="">
                </div>
                <div class="col-9">
                    <div class="username">{{ user.username }}</div>
                    <div class="fans">粉丝数：{{ user.followerCount }}</div>
                    <button @click="follow" v-if="!user.is_followed" type="button"
                        class="btn btn-secondary btn-sm">加关注</button>
                    <button @click="unfollow" v-if="user.is_followed" type="button"
                        class="btn btn-secondary btn-sm">取消关注</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import $ from 'jquery'
import router from '@/router';
import { useStore } from 'vuex'

export default {
    name: "UserProfileInfo",
    components: {

    },

    props: {
        user: {
            type: Object,
            required: true
        }
    },

    setup(props, context) {
        const store = useStore();
        const is_login = store.state.user.is_login;

        // 先改数据库再改本地
        const follow = () => {
            if (!is_login) router.push({ name: 'login' });
            $.ajax({
                url: "/agapi/follow/",
                type: "POST",
                data: {
                    target_id: props.user.id,
                },
                headers: {
                    'Authorization': "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if (resp.result === "success") {
                        context.emit('follow');
                    }
                }
            })
        }

        const unfollow = () => {
            if (!is_login) { router.push({ name: 'login' }); return; }
            $.ajax({
                url: "/agapi/follow/",
                type: "POST",
                data: {
                    target_id: props.user.id,
                },
                headers: {
                    'Authorization': "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if (resp.result === "success") {
                        context.emit('unfollow');
                    }
                }
            });
        };

        return {
            follow,
            unfollow,
        }

    }
}
</script>


<style scoped>
img {
    border-radius: 50%;
}

.username {
    font-weight: bold;
}

.fans {
    font-size: 12px;
    color: gray;
}

button {
    padding: 2px 4px;
    font-size: 12px;
}

.img-field {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
</style>