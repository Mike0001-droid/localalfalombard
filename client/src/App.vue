<template>
    <div 
        class="app"
        :class="($route.name === 'home') ? 'm--white' : ''"
    >
        <appTop 
            :siteInfo="siteInfo"
            @showAuthorization="showAuthorization"
            @hideAuthorization="hideAuthorization"
            @showRegistration="showRegistration"
            @hideRegistration="hideRegistration"
        />
        <appHeader
            v-if="$route.name === 'home'"
            @showAuthorization="showAuthorization"
            @hideAuthorization="hideAuthorization"
            @showRegistration="showRegistration"
            @hideRegistration="hideRegistration"
        />
        <routerView v-slot="{ Component }">
            <transition name="fade">
                <component :is="Component" />
            </transition>
        </routerView>
        <appFooter
            :footer-class="($route.name !== 'home') ? 'm--white' : ''"
            :siteInfo="siteInfo"
            @showAuthorization="showAuthorization"
            @hideAuthorization="hideAuthorization"
        />
        <appError />
        <appLoader />
        <Authorization 
            :show="showModalAuthorization"
            @hideAuthorization="hideAuthorization"
        />
        <Recovery 
            :show="showModalRecovery"
            @hideRecovery="hideRecovery"
        />
        <Registration 
            :show="showModalRegistration"
            @hideRegistration="hideRegistration"
        />
    </div>
</template>

<script>
    import { app } from "@/services";

    import appTop from "@/components/app-top";
    import appHeader from "@/components/app-header";
    import appFooter from "@/components/app-footer";
    import appError from '@/components/app-error.vue';
    import appLoader from '@/components/app-loader.vue';

    import Authorization from "@/components/authorization";
    import Recovery from "@/components/recovery";
    import Registration from "@/components/registration";

    export default {
        components: {
            appTop,
            appHeader,
            appFooter,
            appError,
            appLoader,
            Authorization,
            Recovery,
            Registration
        },
        computed: {
            user() {
                return this.$store.state.user;
            }
        },
        created() {
            window.onerror = (message, source, lineno, colno, err) => {
                console.error('Window error', err.message);
                this.$store.dispatch('showError', { err });
            };
        },
        errorCaptured(err, vm, info) {
            console.error('Local error', err.message, vm, info);
            this.$store.dispatch('showError', { err });
            return false;
        },
        data() {
            return {
                siteInfo: {},
                showModalAuthorization: false,
                showModalRecovery: false,
                showModalRegistration: false
            };
        },
        mounted() {
            this.showLoaderPage = true;
            app.getSiteInfo().then(res => {
                this.showLoaderPage = false;
                this.siteInfo = res;
                console.log(res);
            }).catch(err => {
                this.showLoaderPage = false;
                this.errorPage = err.response.status;
                console.log(err.response);
                //this.$store.dispatch('showError', err);
            });
        },
        methods: {
            showAuthorization() {
                this.showModalAuthorization = true;
                console.log('Show Modal Authorization', this.showModalAuthorization);
            },
            hideAuthorization(props={}) {
                this.showModalAuthorization = false;
                if (props.show == 'recovery') {
                    this.showRecovery();    
                }
            },
            showRecovery() {
                this.showModalRecovery = true;
                console.log('Show Modal Recovery', this.showModalRecovery);
            },
            hideRecovery() {
                this.showModalRecovery = false;
            },
            showRegistration() {
                this.showModalRegistration = true;
                console.log('Show Modal Recovery', this.showModalRegistration);
            },
            hideRegistration() {
                this.showModalRegistration = false;
            },
        }
    };
</script>
<style lang="sass">
    @import './assets/css/main.scss'
</style>