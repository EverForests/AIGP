<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link class="navbar-brand" :to="{ name: 'home' }">首页</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText"
                aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarText">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'userlist' }">推荐</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'imgedit' }">图像编辑</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'imggenerate' }">图像生成</router-link>
                    </li>
                </ul>

                <ul class="navbar-nav" v-if="!$store.state.user.is_login">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'login' }">登录</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'register' }">注册</router-link>
                    </li>
                </ul>

                <ul class="navbar-nav" v-else>
                    <li class="nav-item">
                        <router-link class="nav-link"
                            :to="{ name: 'userprofile', params: { userId: $store.state.user.id } }">{{
                $store.state.user.username }}</router-link>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="cursor: pointer" @click="logout">登出</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import { useStore } from 'vuex';
import $ from 'jquery';

export default {
    name: "NavBar",
    components: {

    },

    setup() {
        const store = useStore();

        const logout = () => {
            store.commit('logout');
            localStorage.clear();
        }

        if (localStorage.getItem("access") && localStorage.getItem("refresh")) {
            setInterval(() => {
                $.ajax({
                    url: "/agapi/token/refresh/",
                    type: "POST",
                    data: {
                        refresh: localStorage.getItem("refresh"),
                    },
                    success(resp) {
                        store.commit('updateAccess', resp.access);
                        localStorage.setItem("access", resp.access);
                    }
                })
            }, 4.5 * 60 * 1000)

            // 实现自动登录
            $.ajax({
                url: "/agapi/getinfo/",
                type: "GET",
                data: {
                    user_id: localStorage.getItem("id"),
                },
                headers: {
                    'Authorization': "Bearer " + localStorage.getItem("access"),
                },
                success(resp) {
                    store.commit("updateUser", {
                        ...resp,
                        access: localStorage.getItem("access"),
                        refresh: localStorage.getItem("refresh"),
                        is_login: true,
                    })
                },
            })
        }

        return {
            logout,
        }
    }
}
</script>

<style scoped></style>