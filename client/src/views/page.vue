<template>
    <div 
        class="app__main map d-flex"
        :class="user ? 'flex-row' : 'flex-column'"
    >
        <SideBar
            v-if="user"
        />

        <div 
            class="app__block py-5"
            :class="user ? '' : 'm--width-100'"
        >
            <template
                v-if="showLoaderPage"
            >
                <div class="ticket__loader loader">
                    <b-spinner variant="primary" class="me-2" /> Загрузка страницы
                </div>
            </template>
            <template
                v-else
            >
                <template
                    v-if="errorPage"
                >
                    <h1 class="h3 text-primary text-uppercase mb-4">
                        Ошибка {{ errorPage }}
                    </h1>
                    <div class="content text">
                        <p>Что то не так... :(</p>
                    </div>
                </template>
                <template
                    v-else-if="page"
                >
                    <h1 class="h3 text-primary text-uppercase mb-4">
                        {{ page.title }}
                    </h1>
                    <div 
                        class="content text"
                        v-html="page.body"
                    />
                </template>
            </template>
        </div>
    </div>
</template>

<script>
    import { app } from "@/services";
    import SideBar from '@/components/side-bar';

    export default {
        name: 'map',
        components: {
            SideBar
        },
        watch: {
            slug: {
                immediate: true,
                handler() {
                    this.showLoaderPage = true;
                    this.errorPage = null;
                    this.page = null;
                    app.getPage(this.slug).then(res => {
                        this.showLoaderPage = false;
                        this.page = res;
                    }).catch(err => {
                        this.showLoaderPage = false;
                        this.errorPage = err.response.status;
                        console.log(err.response);
                        //this.$store.dispatch('showError', err);
                    });
                }
            }
        },
        props: {
            slug: {
                type: String,
                default() { return null; }
            },
        },
        data() {
            return {
                user: this.$store.state.user,
                page: null,
                showLoaderPage: false,
                errorPage: null
            };
        },
        computed: {
        },
        created() {
        },
        methods: {
        }
    };
</script>
