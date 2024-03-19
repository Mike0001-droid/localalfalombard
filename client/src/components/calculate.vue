<template>
    <b-modal 
        v-model="showModal"
        size="lg"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        :title="`Билет №${ticket.ticket}. Расчет долга`"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content">
            <div
                class="form row"
            >
                <div class="ticket__paydata d-flex flex-wrap mb-4">
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4 mb-2">
                        <div class="ticket__paydata-label m--gray-dark">
                            Сумма займа
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(ticketInfo.loanSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4 mb-2">
                        <div class="ticket__paydata-label m--gray-dark">
                            Общий долг
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticketInfo.loanSum + 1 * ticketInfo.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4 mb-2">
                        <div class="ticket__paydata-label m--gray-dark">
                            % на {{ $helpers.parseDate(ticket?.dateToPay || '0001-01-01', 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(ticketInfo.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4 mb-2">
                        <div class="ticket__paydata-label m--gray-dark">
                            Крайний срок оплаты
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.parseDate(ticketInfo.sellDate || '0001-01-01', 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </div>
                    </div>
                </div>
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
        name: 'Calculate',
        components: {
        },
        created() {
            console.log('created');
        },
        mounted() {
        },
        computed: {
            showModal() {
                if (this.show) {
                    this.getTicketDebt();
                }
                return this.show;
            },
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
                user: this.$store.state.user,
                form: {
                    paySum: null,
                },
                formErrors: {},
                ticketInfo: this.ticket,
                showLoaderSending: false,
                showInfoBlock: false
            };
        },
        methods: {
            getTicketDebt() {
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
            hideModal() {
                this.$emit('hideCalculate');
            },
        }
    };
</script>
