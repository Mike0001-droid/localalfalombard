<template>
    <div 
        class="app__main profile d-flex flex-row"
    >
        <SideBar />
        <div class="app__block py-5">
            <div class="h4 text-uppercase">Личные данные</div>
            <b-form
                class="profile__form form row"
                @submit="onSubmitProfile"
            >
                <b-form-group
                    id="input-group-phone"
                    label="Номер телефона*"
                    label-for="input-phone"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-phone"
                        v-model="formProfile.phone"
                        type="text"
                        placeholder="Телефон"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.phone ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-spasport"
                    label="Серия паспорта*"
                    label-for="input-spasport"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-spasport"
                        v-model="formProfile.series"
                        type="text"
                        placeholder="Серия паспорта"
                        variant="primary"
                        disabled
                        required
                        :state="formErrors && formErrors.series ? false : null"
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
                        v-model="formProfile.number"
                        type="text"
                        placeholder="Номер паспорта"
                        variant="primary"
                        disabled
                        required
                        :state="formErrors && formErrors.number ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-email"
                    label="Email*"
                    label-for="input-email"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-email"
                        v-model="formProfile.email"
                        type="text"
                        placeholder="Email"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.email ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <div class="h4 text-uppercase">Уведомления</div>
                <div class="profile__info mb-2">
                    <span class="icon m--info"></span> Вам будут приходить уведомления на Email за 7 дней и за 3 дня до окончания льготного периода
                </div>
                <b-form-group
                    id="input-group-notify"
                    label-for="input-notify"
                    class="col-12 mb-0"
                >
                    <b-form-checkbox
                        id="input-notify"
                        v-model="formProfile.notify"
                    >
                        Включить уведомления
                    </b-form-checkbox>
                </b-form-group>
                <div 
                    v-if="formErrors.detail_profile"
                    class="col-12"
                >
                    <b-card
                        bg-variant="danger"
                        text-variant="white"
                        class="text-center mb-4"
                    >
                        <b-card-text>
                            <div class="h4 text-white text-uppercase">
                                {{ formErrors.detail_profile }}
                            </div>
                            <p>Пожалуйста, проверьте правильность ввода и попробуйте еще раз</p>
                        </b-card-text>
                    </b-card>
                </div>
                <div class="text-center col-12 mb-2 pt-2">
                    <b-button 
                        type="submit" 
                        variant="primary"
                        class="profile__button mx-auto"
                        size="lg"
                        pill
                    >
                        Сохранить изменения
                    </b-button>
                </div>
                <div class="col-12">
                    <hr
                        class="bg-primary opacity-100"
                    >
                </div>
            </b-form>
            <div class="h4 text-uppercase">Смена пароля</div>
            <b-form
                class="profile__form form row"
                @submit="onSubmitPassword"
            >
                <b-form-group
                    id="input-group-password"
                    label="Введите текущий пароль"
                    label-for="input-password"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-password"
                        v-model="formPassword.password"
                        type="password"
                        placeholder="Пароль"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.password ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-password-new"
                    label="Введите новый пароль"
                    label-for="input-password-new"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-password-new"
                        v-model="formPassword.password_new"
                        type="password"
                        placeholder="Пароль"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.password_new ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <b-form-group
                    id="input-group-password-rep"
                    label="Повторите новый пароль"
                    label-for="input-password-rep"
                    class="col-12 col-lg-4 mb-0"
                >
                    <b-form-input
                        id="input-password-rep"
                        v-model="formPassword.password_confirm"
                        type="password"
                        placeholder="Пароль"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.password_confirm ? false : null"
                    ></b-form-input>                
                </b-form-group>
                <div 
                    v-if="formErrors.detail_password"
                    class="col-12"
                >
                    <b-card
                        bg-variant="danger"
                        text-variant="white"
                        class="text-center mb-4"
                    >
                        <b-card-text>
                            <div class="h4 text-white text-uppercase">
                                {{ formErrors.detail_password }}
                            </div>
                            <p>Пожалуйста, проверьте правильность ввода и попробуйте еще раз</p>
                        </b-card-text>
                    </b-card>
                </div>
                <div class="text-center col-12 mb-2 pt-2">
                    <b-button 
                        type="submit" 
                        variant="primary"
                        class="profile__button mx-auto"
                        size="lg"
                        pill
                    >
                        Изменить пароль
                    </b-button>
                </div>
            </b-form>
            <b-overlay 
                :show="showLoaderSending"
                no-wrap
                spinner-variant="primary"
            />
        </div>
    </div>
</template>

<script>
    import { app } from "@/services";
    //import TicketsBlock from "@/views/tickets-block";
    import SideBar from '@/components/side-bar';
    //import UserStats from '@/components/user-stats';
    //import Payment from "@/components/payment";
    //import { DatePicker } from 'v-calendar';
    //import 'v-calendar/dist/style.css';

    export default {
        name: 'Profile',
        components: {
            SideBar
        },
        computed: {
            showModal() {
                return this.show;
            },
        },
        props: {
            show: {
                type: Boolean,
                default() { return false; }
            }
        },
        data() {
            return {
                formProfile: {},
                formPassword: {},
                formErrors: {},
                showLoaderSending: false,
            };
        },
        created() {
        },
        mounted() {
            this.formProfile = Object.assign({}, this.$store.state.user);
        },
        methods: {
            onSubmitProfile() {
                this.formErrors = {};
                this.showLoaderSending = true;
                let params = {
                    phone: this.formProfile.phone,
                    email: this.formProfile.email,
                    notify: this.formProfile.notify,
                }
                app.updateUser(params).then(res => {
                    //this.showLoaderSending = false;
                    console.log(res);
                    app.getProfile().then(res => {
                        this.showLoaderSending = false;
                        this.$store.dispatch('setUser', res);
                        this.$store.dispatch('clearUserStats');
                    }).catch(err => {
                        this.showLoaderSending = false;
                        //this.$store.dispatch('showError', err);
                        console.error(err);
                    });
                }).catch(err => {
                    this.showLoaderSending = false;
                    if (err.detail) {
                        this.formErrors.detail_profile = err.detail;
                    } else {
                        this.formErrors.detail_profile = 'Что-то пошло не так!';
                    }
                    //this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            onSubmitPassword() {
                this.formErrors = {};
                if (this.formPassword.password_new !== this.formPassword.password_confirm) {
                    this.formErrors = { 
                        password_new: 1,
                        password_confirm: 1,
                        detail_password: 'Пароли не совпадают!'
                    }
                } else {
                    this.showLoaderSending = true;
                    app.updatePassword(this.formPassword).then(res => {
                        this.showLoaderSending = false;
                        console.log(res);
                        this.formPassword = {};
                    }).catch(err => {
                        this.showLoaderSending = false;
                        if (err.detail && err.response.data) {
                            this.formErrors = (err.response && err.response.data) ? err.response.data.error : {};
                            this.formErrors.detail_password = err.detail;
                        } else {
                            this.formErrors.detail_password = 'Что-то пошло не так!';
                        }
                        //this.$store.dispatch('showError', err);
                        console.error(err);
                    });
                }
            },
            hideModal() {
                this.$emit('hideProfile');
            },
        }
    };
</script>
