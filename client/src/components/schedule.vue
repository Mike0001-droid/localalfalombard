<template>
    <b-modal 
        v-model="showModal"
        size="lg"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        :title="`Билет №${ticket.ticket}. График начисления процентов`"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content">
            <div
                class="row"
            >
                <div class="ticket__paydata d-flex flex-wrap mb-4">
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4">
                        <div class="ticket__paydata-label m--gray-dark">
                            Сумма займа
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(ticketInfo.loanSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4">
                        <div class="ticket__paydata-label m--gray-dark">
                            Общий долг
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(1 * ticket.loanSum + 1 * ticket.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4">
                        <div class="ticket__paydata-label m--gray-dark">
                            % на сегодня
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.toPrice(ticket.debtSum, { pointer: '.', sign: '₽' }) }}
                        </div>
                    </div>
                    <div class="ticket__paydata-item col-12 col-sm-6 col-xl-4">
                        <div class="ticket__paydata-label m--gray-dark">
                            Крайний срок оплаты
                        </div>
                        <div class="ticket__paydata-value">
                            {{ $helpers.parseDate(ticketInfo.sellDate || ticket.sellDate || '0001-01-01', 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </div>
                    </div>
                </div>
                <div class="ticket__accrual">
                    <b-table 
                        :fields="fields"
                        :items="ticketAccrual"
                        select-mode="single"
                        responsive
                        hover
                        class="table__data b-table-sticky-header"
                        selectable
                    >
                        <template #cell(date)="data">
                            {{ $helpers.parseDate(data.value || '0001-01-01', 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </template>
                    </b-table>
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
        watch: {
            show: {
                immediate: true,
                handler() {
                    this.showModal = this.show;
                    if (this.show) {
                        this.getTicketDebt();
                        this.getTicketAccrual();
                    }
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
                ticketInfo: {},
                ticketAccrual: [],
                fields: [{
                    key: 'num',
                    label: '#'
                }, {
                    key: 'date',
                    label: 'Дата'
                }, {
                    key: 'basePercent',
                    label: 'Базовый процент'
                }, {
                    key: 'baseSum',
                    label: 'Базовая сумма'
                }, {
                    key: 'finePercent',
                    label: 'Процент пени'
                }, {
                    key: 'fineSum',
                    label: 'Сумма пени'
                }],
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
                    //this.form.paySum = this.ticketInfo.debtSum;
                }).catch(err => {
                    this.showLoaderSending = false;
                    this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            getTicketAccrual() {
                let params = {
                    client_id: this.user.client_id,
                    ticket_id: this.ticket.ticketId,
                };
                this.showLoaderSending = true;
                app.getTicketAccrual(params).then(res => {
                    this.showLoaderSending = false;
                    console.log(res);
                    this.ticketAccrual = res.result.accrualList;
                }).catch(err => {
                    this.showLoaderSending = false;
                    this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            hideModal() {
                this.$emit('hideSchedule');
            },
        }
    };
</script>
