<template>
    <b-modal 
        v-model="showModal"
        size="lg"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        title="Вход в личный кабинет"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content">
            <p>Если у Вас был хотя бы один займ в наших ломбардах, вы успешно войдете в систему</p>
            <b-form
                class="form row"
                @submit="onSubmit"
            >
                <b-form-group
                    id="input-group-login"
                    label="Номер телефона или email"
                    label-for="input-login"
                    class="col-12 col-lg-6 mb-0"
                >
                    <b-form-input
                        id="input-login"
                        v-model="form.email"
                        type="text"
                        placeholder="Номер телефона или email"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.email ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-password"
                    label="Пароль"
                    label-for="input-password"
                    class="col-12 col-lg-6 mb-0"
                >
                    <div class="auth__password">
                        <b-form-input
                            id="input-password"
                            v-model="form.password"
                            type="password"
                            placeholder="Пароль"
                            required
                            :state="formErrors && formErrors.password ? false : null"
                        ></b-form-input>
                    </div>
                </b-form-group>
                <div class="d-flex mb-3">
                    <a
                        href="#"
                        @click.prevent="showRecovery"
                    >
                        Забыли пароль?
                    </a>
                </div>
                <div 
                    v-if="formErrors.detail"
                    class="col-12"
                >
                    <b-card
                        bg-variant="danger"
                        text-variant="white"
                        class="text-center mb-4"
                    >
                        <b-card-text>
                            <div class="h4 text-white text-uppercase">
                                {{ formErrors.detail }}
                            </div>
                            <p>Пожалуйста, проверьте правильность ввода и попробуйте еще раз</p>
                        </b-card-text>
                    </b-card>
                </div>
                <b-button 
                    type="submit" 
                    variant="outline-primary"
                    class="mx-auto col-12 col-sm-4 mt-3"
                    size="lg"
                    pill
                >
                    Войти
                </b-button>
            </b-form>
        </div>
        <b-overlay 
            :show="showLoaderSending"
            no-wrap
            spinner-variant="primary"
        />
    </b-modal>
</template>

<script>
    import { app } from "@/services";
    export default {
        name: 'Authorization',
        components: {
        },
        watch: {
            show: {
                immediate: true,
                handler() {
                    this.showModal = this.show;
                }
            }
        },
        props: {
            show: {
                type: Boolean,
                default() { return false; }
            }
        },
        data() {
            return {
                showModal: this.show,
                form: {
                    email: null,
                    password: null
                },
                formErrors: {},
                showLoaderSending: false,
            };
        },
        methods: {
            onSubmit() {
                this.showLoaderSending = true;
                this.formErrors = {};
                app.obtainToken(this.form).then(res => {
                    if (res.access && res.refresh) {
                        this.$store.dispatch('setToken', res);
                        app.getProfile().then(res => {
                            this.showLoaderSending = false;
                            this.$store.dispatch('setUser', res);
                            this.$store.dispatch('clearUserStats');
                            this.$emit('hideAuthorization');
                            this.next();
                        }).catch(err => {
                            this.showLoaderSending = false;
                            //this.$store.dispatch('showError', err);
                            console.error(err);
                        });
                    } else {
                        this.showLoaderSending = false;
                        this.$store.dispatch('showError', 'Ошибка получения токена');
                    }
                }).catch(err => {
                    this.showLoaderSending = false;
                    //this.$store.dispatch('showError', err);
                    this.formErrors = { 
                        email: 1,
                        password: 1,
                        detail: err.response.data.detail
                    }
                    console.error(err);
                });
            },
            hideModal() {
                this.$emit('hideAuthorization');
            },
            showRecovery() {
                this.$emit('hideAuthorization', { show: 'recovery' });
            },
            next() {
                this.$router.push({ name: 'tickets' });
            }
        }
    };
</script>
