<template>
    <div class="app__top">
        <router-link
            v-if="user"
            :to="{ name: 'tickets' }"
            class="app__top-logo"
        />
        <router-link
            v-else
            :to="{ name: 'home' }"
            class="app__top-logo"
        />
        <div class="app__top-block">
            <div class="app__top-contacts">
                <a 
                    :href="`tel:${siteInfo.phone}`" 
                    class="app__top-contacts-item m--phone"
                >
                    {{ siteInfo.phone }}
                </a>
                <a 
                    :href="`mailto:${siteInfo.email}`" 
                    class="app__top-contacts-item m--mail"
                >
                    {{ siteInfo.email }}
                </a>
                <!--a href="#" class="app__top-contacts-item m--vk">
                </a-->
            </div>
            <div 
                v-if="user"
                class="app__top-user"
            >
                {{ user.fio || user.email }}
            </div>
            <div 
                v-else
                class="app__top-menu"
            >
                <a 
                    href="#" 
                    class="app__top-menu-item"
                    @click.prevent="$emit('showRegistration')"
                >
                    Регистрация
                </a>
                <a 
                    href="#" 
                    class="app__top-menu-item"
                    @click.prevent="$emit('showAuthorization')"
                >
                    Вход
                </a>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'appTop',
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
        }
    };
</script>
