import $ from 'jquery'
import { jwtDecode } from 'jwt-decode'

const ModuleUser={
    state: {
        id: "",
        username: "",
        photo: "",
        followerCount: 0,
        access: "",
        refresh: "",
        is_login: false,
    },

    getters: {
        
    },

    mutations: {
        updateUser(state, user) {
            state.id = user.id;
            state.username = user.username;
            state.photo = user.photo;
            state.followerCount = user.followerCount;
            state.access = user.access;
            state.refresh = user.refresh;
            state.is_login = user.is_login;
        },

        updateAccess(state, access) {
            state.access = access;
        },

        logout(state) {
            state.id = "";
            state.username = "";
            state.photo = "";
            state.followerCount = 0;
            state.access = "";
            state.refresh = "";
            state.is_login = false;
        }
    },

    actions: {
        login(context, data) {
            $.ajax({
                url: '/agapi/token/',
                type: "POST",
                data: {
                    username: data.username,
                    password: data.password
                },
                success(resp) {
                    const {access, refresh} = resp;
                    const access_obj = jwtDecode(access);

                    localStorage.setItem("access", access);
                    localStorage.setItem("refresh", refresh);

                    setInterval(() => {
                        $.ajax({
                            url: "/agapi/token/refresh/",
                            type: "POST",
                            data: {
                                refresh,
                            },
                            success(resp) {
                                context.commit('updateAccess', resp.access);
                                localStorage.setItem("access", resp.access);
                            }
                        })
                    }, 4.5*60*1000)

                    // 初始化用户数据
                    $.ajax({
                        url: "/agapi/getinfo/",
                        type: "GET",
                        data: {
                            user_id: access_obj.user_id,
                        },
                        headers: {
                            'Authorization': "Bearer " + access,
                        },
                        success(resp) {
                            context.commit("updateUser", {
                                ...resp,
                                access: access,
                                refresh: refresh,
                                is_login: true,
                            })

                            localStorage.setItem("id", resp.id);
                            console.log(resp);

                            data.success();
                        },
                    })
                },

                error() {
                    console.log("404");
                    data.error();
                }
            })
        }
    },

    modules: {
        
    }
}

export default ModuleUser;