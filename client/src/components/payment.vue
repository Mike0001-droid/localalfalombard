<template>
    <b-modal 
        v-model="showModal"
        size="xl"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        :title="`Билет №${ticket.ticket}`"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content">
            <b-form
                class="form row"
                @submit="onSubmit"
            >
                <div class="ticket__paydata d-flex flex-wrap mb-4">
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            Сумма займа
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticketInfo.loanSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            Общий долг
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticket.loanSum + 1 * ticket.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            % на сегодня
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticket.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            Крайний срок оплаты
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.parseDate(ticketInfo.sellDate || ticket.sellDate || '0001-01-01', 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </div>
                    </div>
                </div>
                <b-form-group
                    id="input-group-paysum"
                    label-for="input-paysum"
                    class="col-12 col-sm-6 col-xl-3 pe-4"
                >
                    <div class="ticket__sum">
                        <div class="ticket__sum-label m--gray-dark mb-0">Оплатить сейчас</div>
                        <div class="ticket__sum-data">
                            от <strong>{{ $helpers.toPrice(ticketInfo.debtSum, { pointer: '.', sign: '₽' }) }}</strong> до <strong>{{ $helpers.toPrice(1 * ticketInfo.debtSum + 1 * ticketInfo.maxBodySum, { pointer: '.', sign: '₽' }) }}</strong>
                        </div>
                    </div>
                    <b-form-input
                        id="input-paysum"
                        v-model="form.paySum"
                        v-maska="{ mask: '#*D##', tokens: { 'D': { pattern: /\./ }}}"
                        name="paysum"
                        type="text"
                        placeholder="Сумма к оплате"
                        variant="primary"
                        required
                        :state="formErrors && formErrors.paysum ? false : null"
                        @maska="onMask"
                    ></b-form-input>                
                </b-form-group>
                <b-button 
                    type="submit" 
                    variant="primary"
                    class="col-12 col-sm-6 col-xl-3 mt-auto mb-3"
                    size=""
                    pill
                >
                    Оплатить
                </b-button>
                <div 
                    class="col-12"
                >
                    <b-card
                        v-if="formErrors.detail"
                        bg-variant="danger"
                        text-variant="white"
                        class="text-center mb-4"
                    >
                        <b-card-text>
                            <div class="h4 text-white text-uppercase">
                                {{ formErrors.detail }}
                            </div>
                        </b-card-text>
                    </b-card>
                </div>
                <div
                    v-if="showInfoBlock" 
                    class="ticket__paydata d-flex flex-wrap mb-4">
                    <div class="ticket__paydata-title col-12">К оплате</div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-lg-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            Проценты:
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticketInfo.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-lg-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            Часть тела займа:
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticketInfo.maxBodySum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-lg-3">
                        <div class="ticket__paydata-label m--gray-dark">
                            Итого:
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(ticketInfo.debtSum * 1 + ticketInfo.maxBodySum * 1, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                </div>
                <div class="ticket__help mt-4">
                    <p>После нажатия кнопки «Оплатить» Вы будете перенаправлены на страницу оплаты.</p>
                    <p>В первую очередь оплачиваются проценты по билету, затем - тело займа (до остатка в 100 рублей).</p>
                    <p>Вы получите квитанцию и кассовый чек на указанный Email сразу после оплаты.</p>
                    <p>Банк плательщика может взимать комиссию за перевод денежных средств согласно действующим тарифам банка.</p>
                    <p>ДЛЯ РЕГИСТРАЦИИ ПЛАТЕЖА В СИСТЕМЕ ЛОМБАРДА ПОСЛЕ ОПЛАТЫ НЕОБХОДИМО ОБЯЗАТЕЛЬНО ВЕРНУТЬСЯ НА САЙТ ЛИЧНОГО КАБИНЕТА!</p>
                    <!--p><a href="#" class="text-muted">Полные условия оплаты и инструкция</a></p-->
                </div>
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
        name: 'Payment',
        components: {
        },
        watch: {
            show: {
                immediate: true,
                handler() {
                    this.showModal = this.show;
                    if (this.showModal) this.getTicketDebt();
                }
            }
        },
        props: {
            show: {
                type: Boolean,
                default() { return false; }
            },
            ticket: {
                type: Object,
                default() { return {}; }
            }
        },
        data() {
            return {
                showModal: this.show,
                user: this.$store.state.user,
                form: {
                    paySum: null,
                },
                formErrors: {},
                ticketInfo: {},
                showLoaderSending: false,
                showInfoBlock: false
            };
        },
        methods: {
            getTicketDebt() {
                this.formErrors = {};
                let date = this.ticket.dateToPay || this.$helpers.formatDate(new Date(), 'YYYY-MM-DD');
                console.log('DATE', this.ticket.dateToPay);
                let params = {
                    client_id: this.user.client_id,
                    ticket_id: this.ticket.ticketId,
                    date: date
                };
                this.showLoaderSending = true;
                app.getTicketDebt(params).then(res => {
                    this.showLoaderSending = false;
                    console.log(res);
                    this.ticketInfo = res.result;
                    this.form.paySum = this.ticketInfo.debtSum;
                }).catch(err => {
                    this.showLoaderSending = false;
                    this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            onMask(event) {
                this.form[event.target.name] = event.target.dataset.maskRawValue;
                //this.$emit('input', event.target.dataset.maskRawValue);
                //console.log(event.target.dataset);
            },
            onSubmit() {
                //this.showLoaderSending = true;
                this.formErrors = {};
                let dateToPay = this.ticket.dateToPay ? new Date(this.ticket.dateToPay) : new Date();
                let params = {
                    ticket: this.ticket.ticket,
                    ticket_id: this.ticket.ticketId,
                    amount: this.form.paySum,
                    inn: this.ticketInfo.inn,
                    loan_date: this.ticket.loanDate,
                    date: this.$helpers.formatDate(dateToPay, 'YYYY-MM-DD')
                    //date: dateToPay
                }
                console.log(params);

                this.showLoaderSending = true;
                app.payTicket(params).then(res => {
                    this.showLoaderSending = false;
                    console.log(res);
                    if (res.REF) {
                        //this.$store.dispatch('clearUserStats');
                        window.location.href = res.REF;
                    } else {
                        this.formErrors.detail = 'К сожалению по данными билету оплата не возможна. Не сформирована ссылка на оплату.';
                    }
                }).catch(err => {
                    this.showLoaderSending = false;
                    //this.$store.dispatch('showError', err);
                    console.log(err);
                    this.formErrors.detail = 'Что-то пошло не так';
                });

                //this.formErrors = { login: 1 };
            },
            hideModal() {
                this.$emit('hidePayment');
            },
        }
    };
</script>
