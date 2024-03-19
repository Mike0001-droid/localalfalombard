import { createStore } from 'vuex';
import VuexPersist from 'vuex-persist'

const vuexPersist = new VuexPersist({
    key: 'omega',
    storage: window.localStorage
});

const store = createStore({
    state: {
        user: null,
        userStats: null,
        error: null,
        loader: null,
        access: null,
        refresh: null,
    },
    plugins: [vuexPersist.plugin],
    mutations: {
        USER(state, user) {
            state.user = user;
        },
        USER_STATS(state, info) {
            state.userStats = info;
        },
        TOKENS(state, tokens) {
            state.access = tokens.access || null;
            state.refresh = tokens.refresh || null;
        },
        ERROR(state, error) {
            state.error = error;
        },
        LOADER(state, loader) {
            state.loader = loader;
        }
    },
    actions: {
        setUser(context, user) {
            context.commit('USER', user);
        },
        clearUser(context) {
            context.commit('USER', null);
        },
        setUserStats(context, info) {
            context.commit('USER_STATS', info);
        },
        clearUserStats(context) {
            context.commit('USER_STATS', null);
        },
        setToken(context, tokens) {
            context.commit('TOKENS', tokens);
        },
        clearToken(context) {
            context.commit('TOKENS', {});
        },
        showError(context, error) {
            if (error.response?.status !== 401) {
                context.commit('ERROR', error);
            }
        },
        hideError(context) {
            context.commit('ERROR', null);
        },
        showLoader(context, loader) {
            context.commit('LOADER', loader);
        },
        hideLoader(context) {
            context.commit('LOADER', null);
        }
    }
});

export default store;