<template>
    <b-modal 
        v-model="showModal"
        size="lg"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        title="Восстановление пароля"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content">
            <template
                v-if="showSuccessSending"
            >
                <div class="h4 text-uppercase"><span class="icon m--info me-1"/>Ссылка для восстановления пароля успешно отправлена</div>
                <p>Она будет действительна в течение 24 часов. Пожалуйста, проверьте свою почту.</p>
            </template>
            <template
                v-else
            >
                <div class="h4 text-uppercase"><span class="icon m--info me-1"/>Введите email, указанный при регистрации</div>
                <p>Мы отправим Вам ссылку. Пройдите по ней, чтобы ввести новый пароль</p>
                <b-form
                    class="form row"
                    @submit="onSubmit"
                >
                    <b-form-group
                        id="input-group-email"
                        label="Email"
                        label-for="input-email"
                        class="col-12 mb-0"
                    >
                        <b-form-input
                            id="input-email"
                            v-model="form.email"
                            type="text"
                            placeholder="Email"
                            variant="primary"
                            required
                            :state="formErrors && formErrors.email ? false : null"
                        ></b-form-input>                
                    </b-form-group>
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
                        Отправить ссылку
                    </b-button>
                </b-form>
            </template>
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
        name: 'Recovery',
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
                },
                formErrors: {},
                showLoaderSending: false,
                showSuccessSending: false,
            };
        },
        methods: {
            onSubmit() {
                this.showLoaderSending = true;
                this.formErrors = {};
                app.resetPassword(this.form).then(res => {
                    this.showLoaderSending = false;
                    console.log(res);
                    /*
                    if (res.access && res.refresh) {
                        this.$store.dispatch('setToken', res);
                        app.getUser().then(res => {
                            this.showLoaderSending = false;
                            this.$store.dispatch('setUser', res);
                            this.next();
                        }).catch(err => {
                            this.showLoaderSending = false;
                            this.$store.dispatch('showError', err);
                            console.error(err);
                        });
                    } else {
                        this.showLoaderSending = false;
                        this.$store.dispatch('showError', 'Ошибка получения токена');
                    }
                    */
                    this.showSuccessSending = true;
                }).catch(err => {
                    this.showLoaderSending = false;
                    //this.$store.dispatch('showError', err);
                    this.formErrors = { 
                        email: 1,
                        detail: err.response.data.detail
                    }
                    console.error(err);
                });
            },
            hideModal() {
                this.$emit('hideRecovery');
            },
        }
    };
</script>
