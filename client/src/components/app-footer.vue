<template>
    <div 
        :class="footerClass"
        class="app__footer"
    >
        <div class="app__footer-left">
            <div 
                v-if="!user"
                class="app__footer-menu"
            >
                <router-link
                    v-for="(item, index) in menuFooter"
                    :key="`footer-menu-${index}`"
                    :to="{ name: item.name }"
                    class="app__footer-menu-item"
                    :class="!user && item.role === 'user' ? 'd-none' : ''"
                >
                    {{ item.title }}
                </router-link>
                <a 
                    v-if="user"
                    href="#" 
                    class="app__footer-menu-item"
                    @click.prevent="logout"
                >
                    Выйти
                </a>
                <a
                    v-else 
                    href="#" 
                    class="app__footer-menu-item"
                    @click.prevent="$emit('showAuthorization')"
                >
                    Войти в кабинет
                </a>
            </div>
            <div class="app__footer-copyright">
                © 2023 ООО Ломбард «Омега». Все права защищены

            </div>
            <div class="app__footer-menu m--small">
                <router-link
                    v-for="(item, index) in menuBottom"
                    :key="`bottom-menu-${index}`"
                    :to="{ name: item.name }"
                    class="app__footer-menu-item"
                >
                    {{ item.title }}
                </router-link>
            </div>
        </div>
        <div 
            class="app__footer-info content"
            v-html="siteInfo.footer_text"
        />
        <div class="app__footer-right">
            <a href="//flexites.org" target="_blank" class="app__footer-developer">сайт разработан</a>
        </div>
    </div>
</template>

<script>
    //import { footerMenu, bottomMenu } from '@/settings';
    export default {
        name: 'appFooter',
        components: {
        },
        computed: {
            user() {
                return this.$store.state.user;
            }
        },
        props: {
            siteInfo: {
                type: Object,
                default() { return {}; }
            },
            footerClass: {
                type: String,
                default() { return ''; }
            },
        },
        data() {
            return {
                menuFooter: [{
                /*
                    name: 'help',
                    role: 'user',
                    title: 'Помощь'
                }, {
                */
                    name: 'map',
                    role: 'all',
                    title: 'Отделения на карте'
                }],
                menuBottom: [{
                    name: 'about',
                    role: 'all',
                    title: 'О компании'
                }, {
                    name: 'help',
                    role: 'all',
                    title: 'Справка'
                }, {
                    name: 'personal-data',
                    role: 'all',
                    title: 'Положение об обработке персональных данных потребителя'
                }],
            };
        },
        methods: {
            logout() {
                this.$store.dispatch('clearUser');
                this.$store.dispatch('clearToken');
                this.$router.push({ name: 'home' });
            }
        }
    };
</script>
