<template>
    <b-modal 
        v-model="showModal"
        size="xl"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        title="Задайте нам вопрос"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content">
            <div class="question">
                <b-form
                    class="form row"
                    @submit="onSubmit"
                >
                    <div class="col-12 col-lg-4 mb-0">
                        <b-form-group
                            id="input-group-person"
                            label="Имя*"
                            label-for="input-person"
                            class=""
                        >
                            <b-form-input
                                id="input-person"
                                v-model="form.person"
                                type="text"
                                placeholder="Ваше имя"
                                variant="primary"
                                required
                                :state="formErrors && formErrors.person ? false : null"
                            ></b-form-input>                
                        </b-form-group>
                        <b-form-group
                            id="input-group-email"
                            label="Email*"
                            label-for="input-email"
                            class=""
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
                        <b-form-group
                            id="input-group-phone"
                            label="Телефон*"
                            label-for="input-phone"
                            class=""
                        >
                            <b-form-input
                                id="input-phone"
                                v-model="form.phone"
                                type="text"
                                placeholder="Телефон"
                                variant="primary"
                                required
                                :state="formErrors && formErrors.phone ? false : null"
                            ></b-form-input>                
                        </b-form-group>
                    </div>

                    <div class="col-12 col-lg-8">                    
                        <b-form-group
                            id="input-group-question"
                            label="Комментарий*"
                            label-for="input-question"
                            class="h-100"
                        >
                            <b-form-textarea
                                id="input-question"
                                v-model="form.question"
                                placeholder="Напишите здесь, что вас интересует."
                                variant="primary"
                                required
                                :state="formErrors && formErrors.question ? false : null"
                            ></b-form-textarea>                
                        </b-form-group>
                    </div>
                    <div class="text-muted small mb-3">*Данные обязательные для заполнения</div>
                    <div class="d-flex col-12 col-lg-7 mb-3">
                        <b-form-checkbox 
                            name="agreement"
                            variant="primary"
                            required 
                        >
                            Я ознакомлен и согласен на <a href="/agreement" target="_blank">обработку персональных данных</a> и с <a href="/personal-data" target="_blank">политикой конфиденциальности</a>
                        </b-form-checkbox>
                    </div>
                    <div 
                        v-if="formSend"
                        class="col-12"
                    >
                        <b-card
                            bg-variant="success"
                            text-variant="white"
                            class="text-center mb-4"
                        >
                            <b-card-text>
                                <div class="h4 text-white text-uppercase">
                                    Ваш вопрос успешно отправлен!
                                </div>
                            </b-card-text>
                        </b-card>
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
                    <div class="text-end col-12 col-lg ms-auto mb-3">
                        <b-button 
                            type="submit" 
                            variant="primary"
                            class="profile__button mx-auto"
                            size="lg"
                            pill
                        >
                            Отправить сообщение
                        </b-button>
                    </div>
                </b-form>
            </div>
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
        name: 'Question',
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
                user: this.$store.state.user,
                form: {},
                formErrors: {},
                formSend: false,
                showLoaderSending: false,
            };
        },
        mounted() {
            this.formSend = false;
            this.form = {
                phone: this.user.phone,
                email: this.user.email
            };
        },
        methods: {
            onSubmit() {
                this.showLoaderSending = true;
                this.formErrors = {};
                app.askQuestion(this.form).then(res => {
                    this.showLoaderSending = false;
                    console.log(res);
                    this.formSend = true;
                    this.form = {};
                }).catch(err => {
                    this.showLoaderSending = false;
                    this.formErrors = err.response.data;
                    this.formErrors.detail = err.message;
                    //this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            hideModal() {
                this.$emit('hideQuestion');
            },
        }
    };
</script>
