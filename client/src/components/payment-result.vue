<template>
    <b-modal 
        v-model="showModal"
        size="lg"
        classes="modal__container" 
        header-class="pb-2 mb-2"
        body-class="pt-0"
        content-class="modal__block"
        :title="`Проверка платежа по билету №${ticket.ticket}`"
        centered
        hide-footer
        scrollable
        @hidden="hideModal"
    >
        <div class="modal__content my-4">
            <div 
                class="ticket__payresult py-4"
                :class="showLoaderSending ? 'py-4' : ''"
            >
                <template
                    v-if="!showLoaderSending"
                >
                    <b-card
                        v-if="payResult.status !== 0"
                        bg-variant="danger"
                        text-variant="white"
                        class="text-center mb-4"
                    >
                        <b-card-text>
                            <div class="h4 text-white text-uppercase">
                                {{ payResult.detail }}
                            </div>
                        </b-card-text>
                    </b-card>
                    <template
                        v-else
                    >
                        <b-card
                            bg-variant="success"
                            text-variant="white"
                            class="text-center mb-4"
                        >
                            <b-card-text>
                                <div class="h4 text-white text-uppercase">
                                    {{ payResult.detail }}
                                </div>
                            </b-card-text>
                        </b-card>
                        <b-button 
                            variant="outline-success"
                            class="d-block col-6 col-sm-6 col-xl-3 mx-auto"
                            size=""
                            pill
                            @click.stop="hideModal()"
                        >
                            Закрыть
                        </b-button>
                    </template>                    
                </template>
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
        name: 'PaymentResult',
        components: {
        },
        watch: {
            show: {
                immediate: true,
                handler() {
                    this.showModal = this.show;
                    if (this.show) {
                        this.payTicketResult(this.query);
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
            },
            query: {
                type: Object,
                default() { return {}; }
            }
        },
        data() {
            return {
                showModal: this.show,
                user: this.$store.state.user,
                payResult: {},
                showLoaderSending: false,
            };
        },
        methods: {
            payTicketResult(params) {
                this.showLoaderSending = true;
                app.payTicketResult(params).then(res => {
                    //this.showLoaderSending = false;
                    console.log(res);
                    this.payResult = res;
                    this.getStatsInfo();
                }).catch(err => {
                    this.showLoaderSending = false;
                    this.payResult = {
                        status: 99,
                        detail: err.message
                    };
                    //this.payResult = err.response;
                    //this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            // дубль из /components/user-stats.bue для получение актуальной статистики по билетам.
            getStatsInfo() {
                let params = {
                    client_id: this.user.client_id
                };
                this.showLoaderSending = true;
                app.getTickets(params).then(res => {
                    this.showLoaderSending = false;
                    let result = res.result;
                    let tickets = result.ticketsList ? result.ticketsList : [];
                    let loanSum = 0;
                    let debtSum = 0;
                    let totalSum = 0;
                    tickets.forEach(ticket => {
                        if (ticket.status === 1 || ticket.status === 2) {
                            loanSum += 1 * ticket.loanSum;
                            debtSum += 1 * ticket.debtSum;
                            totalSum += 1 * ticket.totalSum;
                        }
                    });
                    this.userStats = {
                        loanSum: loanSum,
                        debtSum: debtSum,
                        totalSum: totalSum,
                        date: Date.now()
                    }
                    this.$store.dispatch('setUserStats', this.userStats);
                }).catch(err => {
                    this.showLoaderSending = false;
                    //this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            hideModal() {
                this.$emit('hidePaymentResult');
            },
        }
    };
</script>
