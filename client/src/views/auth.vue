<template>
    <div class="app__block auth d-flex w-100 flex-column flex-md-row">
        <div class="auth__left d-flex col-12 col-md-5 h-md-100 px-3">
            <div class="auth__logo">
                <router-link
                    tag="a"
                    :to="{ name: 'home' }"
                >
                    <img src="/assets/img/logo-index.svg" alt="">
                </router-link>
            </div>
        </div>
        <div class="auth__right d-flex flex-column col-12 col-md-7 h-md-100 p-3 my-auto my-md-0">
            <template 
                v-if="template == 'authorization'"
            >
                <div class="auth__right-form m-auto py-3">
                    <h1 class="auth__right-title text-center">
                        Войдите в ваш аккаунт
                    </h1>
                    <div class="auth__right-text text-center mb-3">
                        Посмотрите, что происходит с вашей рекламой
                    </div>

                    <b-form
                        class="form"
                        @submit="onSubmit"
                    >
                        <b-form-group
                            id="input-group-email"
                            label="Email"
                            label-for="input-email"
                        >
                            <b-form-input
                                id="input-email"
                                v-model="form.email"
                                type="email"
                                placeholder="name@mail.ru"
                                required
                                size="lg"
                                :state="formErrors[template] && formErrors[template].email ? false : null"
                            ></b-form-input>                
                            <b-form-invalid-feedback id="input-email-feedback">
                                {{ formErrors[template] ? formErrors[template].email : '' }}
                            </b-form-invalid-feedback>
                        </b-form-group>
                        <b-form-group
                            id="input-group-password"
                            label="Пароль"
                            label-for="input-password"
                        >
                            <div class="auth__password">
                                <b-form-input
                                    id="input-password"
                                    v-model="form.password"
                                    :type="showPass ? 'text' : 'password'"
                                    placeholder=""
                                    required
                                    size="lg"
                                    :state="formErrors[template] && formErrors[template].password ? false : null"
                                ></b-form-input>
                                <b-button
                                    variant="link"
                                    class="auth__password-btn"
                                    :class="showPass ? 'm--show' : ''"
                                    @click="showPassword"
                                />
                            </div>
                            <b-form-invalid-feedback id="input-password-feedback">
                                {{ formErrors[template] ? formErrors[template].password : '' }}
                            </b-form-invalid-feedback>
                        </b-form-group>
                        <div class="d-flex mb-4">
                            <b-form-checkbox 
                                v-model="checked" 
                                name="save-user" 
                                switch
                            >
                                Запомнить пароль
                            </b-form-checkbox>
                            <router-link
                                tag="a"
                                class="d-block ms-auto"
                                :to="{ name: 'auth', params: { template: 'recovery' } }"
                            >
                                Забыли пароль?
                            </router-link>
                        </div>
                        <b-button 
                            type="submit" 
                            variant="warning"
                            class="d-block col-12"
                            size="lg"
                        >
                            Войти
                        </b-button>
                    </b-form>
                </div>
                <div class="auth__right-bottom mb-4 text-center">
                    Еще не зарегистрированы? 
                    <router-link
                        tag="a"
                        :to="{ name: 'registration', params: { template: 'registration' } }"
                    >
                        Создать аккаунт
                    </router-link>
                    <div class=" text-center">
                        <a href="#" @click.prevent="showContract">Договор оферты</a>
                    </div>
                </div>
            </template>
            <template 
                v-else-if="template == 'registration'"
            >
                <div class="auth__right-form m-auto py-3">
                    <h1 class="auth__right-title text-center">
                        Создайте ваш аккаунт
                    </h1>
                    <div class="auth__right-text text-center mb-3">
                        Посмотрите, что происходит с вашей рекламой
                    </div>
                    <b-form
                        class="form"
                        @submit="onSubmit"
                    >
                        <b-form-group
                            id="input-group-email"
                            label="Email"
                            label-for="input-email"
                        >
                            <b-form-input
                                id="input-email"
                                v-model="form.email"
                                type="email"
                                placeholder="radio@radio.ru"
                                required
                                size="lg"
                                :state="formErrors[template] && formErrors[template].email ? false : null"
                            ></b-form-input>
                            <b-form-invalid-feedback id="input-email-feedback">
                                {{ formErrors[template] ? formErrors[template].email : '' }}
                            </b-form-invalid-feedback>
                        </b-form-group>
                        <b-form-group
                            id="input-group-password"
                            label="Пароль"
                            label-for="input-password"
                        >
                            <div class="auth__password">
                                <b-form-input
                                    id="input-password"
                                    v-model="form.password"
                                    :type="showPass ? 'text' : 'password'"
                                    placeholder=""
                                    required
                                    size="lg"
                                    :state="formErrors[template] && formErrors[template].password ? false : null"
                                ></b-form-input>
                                <b-button
                                    variant="link"
                                    class="auth__password-btn"
                                    :class="showPass ? 'm--show' : ''"
                                    @click="showPassword"
                                />
                            </div>
                            <b-form-invalid-feedback id="input-password-feedback">
                                {{ formErrors[template] ? formErrors[template].password : '' }}
                            </b-form-invalid-feedback>
                        </b-form-group>
                        <div class="d-flex mb-4">
                            <b-form-checkbox 
                                name="agreement"
                                required 
                            >
                                <small>Я <a href="#" @click.prevent="showPolicy">ознакомлен и согласен</a> с условиями политики обработки персональных данных и конфиденциальности.</small>
                            </b-form-checkbox>
                        </div>
                        <b-button 
                            type="submit" 
                            variant="warning"
                            class="d-block col-12"
                            size="lg"
                        >
                            Зарегистрироваться
                        </b-button>
                    </b-form>
                </div>
                <div class="auth__right-bottom mb-4 text-center">
                    Уже есть учетная запись?
                    <router-link
                        tag="a"
                        :to="{ name: 'auth', params: { template: 'authorization' } }"
                    >
                        Войти в аккаунт
                    </router-link>
                    <div class=" text-center">
                        <a href="#" @click.prevent="showContract">Договор оферты</a>
                    </div>
                </div>
            </template>
            <template 
                v-else-if="template == 'recovery'"
            >
                <div class="auth__right-form m-auto py-3">
                    <h1 class="auth__right-title text-center">
                        Восстановление пароля
                    </h1>
                    <div class="auth__right-text text-center mb-3">
                        
                    </div>
                    <b-form
                        class="form"
                        @submit="onSubmit"
                    >
                        <b-form-group
                            id="input-group-email"
                            label="Email"
                            label-for="input-email"
                        >
                            <b-form-input
                                id="input-email"
                                v-model="form.email"
                                type="email"
                                placeholder="radio@radio.ru"
                                required
                                size="lg"
                                :state="formErrors[template] && formErrors[template].email ? false : null"
                            ></b-form-input>                
                            <b-form-invalid-feedback id="input-email-feedback">
                                {{ formErrors[template] ? formErrors[template].email : '' }}
                            </b-form-invalid-feedback>
                        </b-form-group>
                        <b-alert
                            variant="warning"
                            fade
                            v-model="alertText"
                        >
                            {{ alertText }}
                        </b-alert>
                        <b-button 
                            type="submit" 
                            variant="warning"
                            class="d-block col-12"
                            size="lg"
                        >
                            Восстановить пароль
                        </b-button>
                        <div class="text-center mt-3">
                            <router-link
                                tag="a"
                                :to="{ name: 'auth', params: { template: 'authorization' } }"
                            >
                                Войти в аккаунт
                            </router-link>
                        </div>
                    </b-form>
                </div>
                <div class="auth__right-bottom mb-4 text-center">
                    Еще не зарегистрированы? 
                    <router-link
                        tag="a"
                        :to="{ name: 'registration', params: { template: 'registration' } }"
                    >
                        Создать аккаунт
                    </router-link>
                    <div class=" text-center">
                        <a href="#" @click.prevent="showContract">Договор оферты</a>
                    </div>
                </div>
            </template>
            <b-overlay 
                :show="showLoaderSending"
                no-wrap
                spinner-variant="warning"
            />
        </div>
        <Policy
            :show="showModalPolicy"
            @hidePolicy="hidePolicy"
        />
        <Contract
            :show="showModalContract"
            @hideContract="hideContract"
        />
    </div>
</template>

<script>
    import { app } from "@/services";
    //import Contract from "@/components/contract";
    //import Policy from "@/components/policy";

    export default {
        name: 'index',
        components: {
            //Contract,
            //Policy
        },
        props: {
            template: {
                type: String,
                default() { return 'authorization'; }
            }
        },
        data() {
            //console.log(this.$store.state.rooms);
            return {
                //dismissSecs: 5,
                //dismissCountDown: 0,
                showPass: false,
                alertText: null,
                showLoaderSending: false,
                form: {
                    email: null,
                    password: ''
                },
                formErrors: {},
                showModalContract: false,
                showModalPolicy: false
            };
        },
        computed: {
        },
        created() {
            //this.$store.dispatch('hideError');
        },
        methods: {
            //countDownChange(dismissCountDown) {
            //    this.dismissCountDown = dismissCountDown;
            //},
            showPassword() {
                this.showPass = !this.showPass;
            },
            showContract() {
                this.showModalContract = true;
            },
            hideContract() {
                this.showModalContract = false;
            },
            showPolicy() {
                this.showModalPolicy = true;
            },
            hidePolicy() {
                this.showModalPolicy = false;
            },
            onSubmit() {
                this.showLoaderSending = true;
                this.formErrors[this.template] = {};
                if (this.template === 'authorization') {
                    app.obtainToken(this.form).then(res => {
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
                    }).catch(err => {
                        this.showLoaderSending = false;
                        this.$store.dispatch('showError', err);
                        console.error(err);
                    });
                } else if (this.template === 'registration') {
                    app.createUser({
                        email: this.form.email,
                        password: this.form.password
                    }).then(res => {
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
                            this.$store.dispatch('showError', { detail: 'Ошибка получения токена' });
                        }
                    }).catch(err => {
                        this.showLoaderSending = false;
                        if (err.response.status === 400) {
                            console.log(err.response);
                            this.formErrors[this.template] = err.response.data.error;
                        } else {
                            this.$store.dispatch('showError', err);
                            console.error(err);
                        }
                    });
                } else if (this.template === 'recovery') {
                    this.alertText = null;
                    app.resetUser({
                        email: this.form.email
                    }).then(res => {
                        this.showLoaderSending = false;
                        //this.dismissCountDown = this.dismissSecs;
                        this.alertText = res.detail;
                        this.form.email = null;
                    }).catch(err => {
                        this.showLoaderSending = false;
                        if (err.response.status === 400) {
                            console.log(err.response);
                            this.formErrors[this.template] = err.response.data.error;
                        } else {
                            this.$store.dispatch('showError', err);
                            console.error(err);
                        }
                    });
                }
            },
            next() {
                //this.$router.push({ name: 'home' });
                //this.$router.push({ name: 'campaign' });
            },
        }
    };
</script>
