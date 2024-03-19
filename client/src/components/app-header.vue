<template>
    <div
        class="app__header"
    >
        <div class="app__header-inner">
            <div class="app__header-info">
                <div class="app__header-top">Сеть ломбардов «Альфа»</div>
                <h1 class="app__header-title">Личный кабинет клиента</h1>
                <div class="app__header-desc">
                    <ul>
                        <li>Узнайте свою задолженность по залоговым билетам</li>
                        <li>Запланируйте дату следующего платежа</li>
                        <li>Оплатите проценты онлайн</li>
                    </ul>
                </div>
                <div 
                    v-if="user"
                    class="app__header-buttons"
                >
                    <b-button
                        size="lg"
                        variant="warning"
                        class="mb-3"
                        @click.prevent="$router.push({ name: 'tickets' })"
                    >
                        Вход в кабинет
                    </b-button>
                </div>
                <div 
                    v-else
                    class="app__header-buttons"
                >
                    <b-button
                        size="lg"
                        variant="warning"
                        class="mb-3"
                        @click.prevent="$emit('showAuthorization')"
                    >
                        Вход в кабинет
                    </b-button>
                    <b-button
                        size="lg"
                        variant="outline-primary"
                        class="mb-3"
                        @click.prevent="$emit('showRegistration')"
                    >
                        Регистрация
                    </b-button>
                </div>
            </div>
            <!--div class="app__header-pic"></div-->
        </div>
    </div>
</template>

<script>
    export default {
        name: 'appHeader',
        components: {
        },
        computed: {
            user() {
                return this.$store.state.user;
            }
        },
        props: {
        }
    };
</script>
