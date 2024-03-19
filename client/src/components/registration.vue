<template>
    <b-modal 
        v-model="showModal"
        size="xl"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        title="Регистрация доступна только для клиентов ломбарда"
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
                    id="input-group-spasport"
                    label="Серия паспорта*"
                    label-for="input-spasport"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-spasport"
                        v-maska="'####'"
                        name="series"
                        type="text"
                        placeholder="Серия паспорта"
                        variant="primary"
                        required
                        :readonly="this.pasportChecked"
                        :state="formErrors && formErrors.series ? false : null"
                        @maska="onMask"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-npasport"
                    label="Номер паспорта*"
                    label-for="input-npasport"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-npasport"
                        v-maska="'######'"
                        name="number"
                        type="text"
                        placeholder="Номер паспорта"
                        variant="primary"
                        required
                        :readonly="this.pasportChecked"
                        :state="formErrors && formErrors.number ? false : null"
                        @maska="onMask"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-phone"
                    label="Номер телефона*"
                    label-for="input-phone"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-phone"
                        v-maska="'+7(###) ###-##-##'"
                        name="phone"
                        type="text"
                        placeholder="Телефон"
                        variant="primary"
                        required
                        :readonly="this.pasportChecked"
                        :state="formErrors && formErrors.phone ? false : null"
                        @paste.stop="onPastePhone"
                        @maska="onMask"
                    ></b-form-input>                
                </b-form-group>
                <template
                    v-if="!pasportChecked"
                >
                    <div class="small mb-3">*Данные обязательные для заполнения</div>
                    <div class="mb-3"><span class="icon m--info me-1"/>Мы проверим, есть ли Ваши данные в базе наших клиентов. Затем можно будет продолжить регистрацию</div>
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
                        class="mx-auto col-11 col-lg-4 mt-3"
                        size="lg"
                        pill
                    >
                        Проверить данные
                    </b-button>
                </template>
                <template
                    v-else
                >
                    <div class="col-12">
                        <hr
                            class="bg-primary opacity-100"
                        >
                    </div>
                    <input
                        id="input-clientid"
                        v-model="form.client_id"
                        type="hidden"
                    />
                    <input
                        id="input-fio"
                        v-model="form.fio"
                        type="hidden"
                    />
                    <b-form-group
                        id="input-group-email"
                        label="Email*"
                        label-for="input-email"
                        class="col-12 col-lg-4 mb-0"
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
                        id="input-group-password"
                        label="Введите пароль*"
                        label-for="input-password"
                        class="col-12 col-lg-4 mb-0"
                    >
                        <b-form-input
                            id="input-password"
                            v-model="form.password"
                            type="password"
                            placeholder="Введите пароль"
                            variant="primary"
                            required
                            :state="formErrors && formErrors.password ? false : null"
                        ></b-form-input>                
                    </b-form-group>
                    <b-form-group
                        id="input-group-password_re"
                        label="Повторите пароль*"
                        label-for="input-password_re"
                        class="col-12 col-lg-4 mb-0"
                    >
                        <b-form-input
                            id="input-password_re"
                            v-model="form.password_confirm"
                            type="password"
                            placeholder="Повторите пароль"
                            variant="primary"
                            required
                            :state="formErrors && formErrors.password_confirm ? false : null"
                        ></b-form-input>                
                    </b-form-group>
                    <div class="small mb-0">*Данные обязательные для заполнения</div>
                    <div class="small mb-3">Адрес электронной почты (Email) должен быть действительным для прихода ваших кассовых чеков</div>
                    <div class="mb-3"><span class="icon m--info"/>Мы проверим, есть ли Ваши данные в базе наших клиентов. Затем можно будет продолжить регистрацию</div>
                    <div class="d-flex mb-1">
                        <b-form-checkbox 
                            name="agreement"
                            variant="primary"
                            required 
                        >
                            Я ознакомлен и согласен с <router-link :to="{name: 'personal-data'}" target="_blank">условиями политики обработки персональных данных</router-link> и <router-link :to="{name: 'personal-data'}" target="_blank">политикой конфиденциальности</router-link>
                        </b-form-checkbox>
                    </div>
                    <div class="d-flex mb-3">
                        <b-form-checkbox 
                            name="notify"
                            variant="primary"
                        >
                            Я хочу получать уведомления о ближайших платежах по залогам
                        </b-form-checkbox>
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
                        class="mx-auto col-11 col-lg-4 mt-3"
                        size="lg"
                        pill
                    >
                        Зарегистрироваться
                    </b-button>
                </template>
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
                form: {},
                formErrors: {},
                pasportChecked: false,
                showLoaderSending: false,
            };
        },
        methods: {
            onPastePhone(event) {
                let clipboardData = event.clipboardData || window.clipboardData;
                let pastedData = clipboardData.getData('Text');
                pastedData = pastedData.replace(/[^\d]/g, '');
                if (pastedData.length > 10 && (pastedData[0] === '7' || pastedData[0] === '8')) {
                    pastedData = pastedData.slice(1);
                }
                event.target.value = pastedData;
                this.form[event.target.name] = pastedData;
            },
            onMask(event) {
                this.form[event.target.name] = event.target.dataset.maskRawValue;
                //this.$emit('input', event.target.dataset.maskRawValue);
                //console.log(event.target.dataset);
            },
            onSubmit() {
                this.formErrors = {};
                if (!this.pasportChecked) {
                    this.showLoaderSending = true;
                    /* Костыль для приведение телефона к формату в 1С */
                    if (this.form.phone[0] !== '8') {
                        this.form.phone = '8' + this.form.phone;
                    }
                    app.checkUser(this.form).then(res => {
                        this.showLoaderSending = false;
                        let result = res.result;
                        if (result.clientId && result.error.status === 0) {
                            this.pasportChecked = true;
                            this.form.client_id = result.clientId;
                            this.form.fio = result.fio;
                        } else {
                            this.formErrors = { 
                                detail: 'Что-то пошло не так!'
                            }
                        }
                    }).catch(err => {
                        this.showLoaderSending = false;
                        this.formErrors = { 
                            series: 1,
                            number: 1,
                            phone: 1,
                            detail: err.response.data.error ? err.response.data.error.detail : err.detail
                        }
                        console.error(err);
                    });
                } else {
                    if (this.form.password !== this.form.password_confirm) {
                        this.formErrors = { 
                            password: 1,
                            password_confirm: 1,
                            detail: 'Пароли не совпадают!'
                        }
                    } else {
                        this.showLoaderSending = true;
                        this.formErrors = {};
                        app.createUser(this.form).then(res => {
                            if (res.access && res.refresh) {
                                this.$store.dispatch('setToken', res);
                                app.getProfile().then(res => {
                                    this.showLoaderSending = false;
                                    this.$store.dispatch('setUser', res);
                                    this.$emit('hideRegistration');
                                    this.next();
                                }).catch(err => {
                                    this.showLoaderSending = false;
                                    this.formErrors = { 
                                        detail: 'Что-то пошло не так!'
                                    }
                                    console.error(err);
                                });
                            } else {
                                this.showLoaderSending = false;
                                this.formErrors = { 
                                    detail: 'Ошибка получения токена'
                                }
                            }
                        }).catch(err => {
                            this.showLoaderSending = false;
                            this.formErrors = { 
                                email: err.response.data.email ? err.response.data.email : null,
                                detail: err.response.data.client_id ? err.response.data.client_id[0] : null
                            }
                            console.error(err);
                        });
                    }
                }
            },
            hideModal() {
                this.$emit('hideRegistration');
            },
            next() {
                this.$router.push({ name: 'tickets' });
            }
        }
    };
</script>
