<template>
    <div 
        class="app__main ticket d-flex flex-row"
    >
        <SideBar />
        <div class="app__block py-5">
            <UserStats
                mClass="ticket__stats"
            />
            <template
                v-if="showLoaderTicket"
            >
                <div class="ticket__loader loader">
                    <b-spinner variant="primary" class="me-2" /> Загрузка данных
                </div>
            </template>
            <template
                v-else
            >
                <div class="ticket__title text-uppercase text-primary h3 mb-2">
                    Билет №{{ ticket.ticket }}
                </div>
                <div class="ticket__status text-uppercase h5 mb-4">
                    <template
                        v-if="ticket.status === 3"
                    >
                        Выкуплено: 
                        <span class="text-success">
                            {{ $helpers.parseDate(ticket.ransomDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </span>
                    </template>
                    <template
                        v-else-if="ticket.status === 4"
                    >
                        Ушло на реализацию:    
                        <span class="text-danger">
                            {{ $helpers.parseDate(ticket.sellDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </span>
                    </template>
                    <template
                        v-else
                    >
                        Хранится в ломбарде: 
                        <span class="text-danger">
                            до {{ $helpers.parseDate(ticket.sellDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                        </span>
                    </template>
                </div>
                <div 
                    v-if="ticket.DateBN && ticket.paymentEnabled"
                    class="ticket__status text-uppercase h5 mb-4"
                >
                    Оплата по безналичному расчету возможна с {{ $helpers.parseDate(ticket.DateBN, 'YYYY-MM-DD').toLocaleDateString('ru') }} (см.*)
                </div>
                <div class="row mb-5">
                    <div class="col-12 col-xl-6 col-xxl-3 mb-5">
                        <b-card
                            class="ticket__subject h-100"
                        >
                            <div class="ticket__subject-title">Предмет залога:</div>
                            <ul>
                                <li
                                    v-for="(item, index) in ticket.items"
                                    :key="`item-${index}`"
                                >
                                    {{ item.name }}
                                </li>
                            </ul>
                        </b-card>
                    </div>
                    <div class="col-12 col-xxl-9 mb-5">
                        <b-card
                            class="ticket__info h-100"
                        >
                            <div class="row">
                                <div class="ticket__sum col-12 col-lg-6 col-xxl-4 mb-4">
                                    <div class="ticket__sum-value m--blue">
                                        {{ $helpers.toPrice(ticket.loanSum, { pointer: '.', sign: '₽' }) }}
                                    </div>
                                    <div class="ticket__sum-label">
                                        Сумма займа (без %)
                                    </div>
                                    <div class="ticket__sum-date">
                                        оформлен {{ $helpers.parseDate(ticket.loanDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div 
                                    v-if="ticket.status !== 4"
                                    class="ticket__sum col-12 col-lg-6 col-xxl-4 mb-4"
                                >
                                    <div class="ticket__sum-value m--green">
                                        {{ $helpers.toPrice(ticket.debtSum, { pointer: '.', sign: '₽' }) }}
                                    </div>
                                    <div class="ticket__sum-label">
                                        Процент к погашению
                                    </div>
                                    <div class="ticket__sum-date">
                                        на {{ new Date().toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div 
                                    v-if="ticket.status !== 4"
                                    class="ticket__sum col-12 col-lg-6 col-xxl-4 mb-4"
                                >
                                    <div class="ticket__sum-value m--blue">
                                        {{ $helpers.toPrice((ticket.status !== 3) ? 1 * ticket.loanSum + 1 * ticket.debtSum : 0, { pointer: '.', sign: '₽' }) }}
                                    </div>
                                    <div class="ticket__sum-label">
                                        Задолженность
                                    </div>
                                    <div 
                                        v-if="ticket.status !== 3"
                                        class="ticket__sum-date"
                                    >
                                        оплатить до {{ $helpers.parseDate(ticket.Date, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div 
                                    v-if="ticket.status === 4"
                                    class="ticket__sum col-12 col-lg-6 col-xxl-4 mb-4"
                                >
                                    <div class="ticket__sum-label">
                                        Дата последнего платежа
                                    </div>
                                    <div 
                                        v-if="ticket.paymentDate === '0001-01-01'"
                                        class="ticket__sum-date"
                                    >
                                        —
                                    </div>
                                    <div 
                                        v-else
                                        class="ticket__sum-date"
                                    >
                                        {{ $helpers.parseDate(ticket.paymentDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                            </div>
                            <div class="row flex-row-reverse">
                                <div 
                                    v-if="ticket.status !== 4"
                                    class="ticket__sum col-12 col-lg-6 col-xxl-4 mb-4"
                                >
                                    <div class="ticket__sum-label">
                                        Дата последнего платежа
                                    </div>
                                    <div 
                                        v-if="ticket.paymentDate === '0001-01-01'"
                                        class="ticket__sum-date"
                                    >
                                        —
                                    </div>
                                    <div 
                                        v-else
                                        class="ticket__sum-date"
                                    >
                                        {{ $helpers.parseDate(ticket.paymentDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div 
                                    v-if="ticket.paymentEnabled"
                                    class="ticket__sum col-12 col-lg-6 col-xxl-8 mb-4"
                                >
                                    <div class="ticket__sum-label">
                                        Выберите желаемую дату платежа
                                    </div>
                                    <div class="ticket__sum-date">
                                        Процент к погашению и Задолженность пересчитаются согласно выбранной дате
                                    </div>
                                </div>
                            </div>
                            <b-form 
                                v-if="ticket.paymentEnabled"
                                class="row"
                            >
                                <b-form-group
                                    id="calculate-date"
                                    label=""
                                    class="ticket__calendar col-12 col-md-6 col-xl-4"
                                >
                                    <DatePicker
                                        v-model="dateToPay"
                                        :model-config="calendarConfig"
                                        :masks="masks"
                                        :min-date="this.$helpers.formatDate(new Date(), 'YYYY-MM-DD')"
                                        is-required
                                        mode="date"
                                        color="blue"
                                    >
                                        <template v-slot="{ inputValue, inputEvents }">
                                            <b-form-input
                                                name="date"
                                                placeholder="дд.мм.гггг"
                                                readonly
                                                required
                                                size="lg"
                                                :value="inputValue"
                                                v-on="inputEvents"
                                                :state="null"
                                            ></b-form-input>
                                        </template>
                                    </DatePicker>
                                </b-form-group>
                                <div
                                    class="d-flex flex-wrap col-12 col-md-6 col-xl-8 justify-content-end"
                                >
                                    <b-button
                                        class="ticket__button mb-3"
                                        variant="outline-primary"
                                        size="lg"
                                        pill
                                        @click.prevent="showCalculate(ticket)"
                                    >
                                        Рассчитать платеж
                                    </b-button>
                                    <b-button
                                        class="ticket__button ms-3 mb-3"
                                        variant="primary"
                                        size="lg"
                                        pill
                                        @click.prevent="showPayment(ticket)"
                                    >
                                        Оплатить сейчас
                                    </b-button>
                                    <b-button
                                        class="ticket__button ms-3 mb-3"
                                        variant="outline-primary"
                                        size="lg"
                                        pill
                                        @click.prevent="showSchedule(ticket)"
                                    >
                                        Начисление процентов
                                    </b-button>
                                </div>
                            </b-form>
                        </b-card>                
                    </div>
                    <div class="col-12">
                        <b-card
                            class="ticket__dates col-12"
                        >
                            <div class="row">
                                <div class="ticket__date col-12 col-lg-6 col-xxl-4">
                                    <div class="ticket__date-label">
                                        Дата оформления займа
                                    </div>
                                    <div class="ticket__date-value">
                                        {{ $helpers.parseDate(ticket.loanDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div class="ticket__date col-12 col-lg-6 col-xxl-4">
                                    <div class="ticket__date-label">
                                        Дата окончания договора
                                    </div>
                                    <div class="ticket__date-value">
                                        {{ $helpers.parseDate(ticket.Date, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div class="ticket__date col-12 col-lg-6 col-xxl-4">
                                    <div class="ticket__date-label">
                                        Число дней до окончания договора
                                    </div>
                                    <div class="ticket__date-value">
                                        {{ $helpers.stringForNumber(ticket.deltaDate, ['день', 'дня', 'дней']) }}
                                    </div>
                                </div>

                                <div class="ticket__date col-12 col-lg-6 col-xxl-4">
                                    <div class="ticket__date-label">
                                        Адрес оформления займа
                                    </div>
                                    <div class="ticket__date-value">
                                        {{ ticket.lombardName }}
                                    </div>
                                </div>
                                <div class="ticket__date col-12 col-lg-6 col-xxl-4">
                                    <div class="ticket__date-label">
                                        Дата окончания льготного периода
                                    </div>
                                    <div class="ticket__date-value">
                                        {{ $helpers.parseDate(ticket.graceDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                                    </div>
                                </div>
                                <div class="ticket__date col-12 col-lg-6 col-xxl-4">
                                    <div class="ticket__date-label">
                                        Число дней до окончания льготного периода
                                    </div>
                                    <div class="ticket__date-value">
                                        {{ $helpers.stringForNumber(ticket.deltaGraceDate, ['день', 'дня', 'дней']) }}
                                    </div>
                                </div>
                            </div>
                        </b-card>                
                    </div>
                </div>
                <div 
                    v-if="ticket.DateBN && ticket.paymentEnabled"
                    class="text-muted small"
                >
                    * Заемщик исполняет обязательства путем внесения наличных денежных средств, либо по безналичному расчету. В случае оплаты по безналичному расчету оплата возможна только при достижении суммой начисленных процентов значения не менее 3% от суммы займа.
                </div>
            </template>
            <TicketsBlock
                v-if="showTicketsBlock"
                ticketState="other"
                @showPayment="showPayment"
            />
        </div>
        <Payment 
            :show="showModalPayment"
            :ticket="ticket"
            @hidePayment="hidePayment"
        />
        <PaymentResult 
            :show="showModalPaymentResult"
            :ticket="ticket"
            :query="query"
            @hidePaymentResult="hidePaymentResult"
        />
        <Calculate 
            :show="showModalCalculate"
            :ticket="ticket"
            @hideCalculate="hideCalculate"
        />
        <Schedule 
            :show="showModalSchedule"
            :ticket="ticket"
            @hideSchedule="hideSchedule"
        />
    </div>
</template>

<script>
    import { app } from "@/services";
    import TicketsBlock from "@/views/tickets-block";
    import SideBar from '@/components/side-bar';
    import UserStats from '@/components/user-stats';
    import Payment from "@/components/payment";
    import PaymentResult from "@/components/payment-result";
    import Calculate from "@/components/calculate";
    import Schedule from "@/components/schedule";
    import { DatePicker } from 'v-calendar';
    import 'v-calendar/dist/style.css';

    export default {
        name: 'ticket',
        components: {
            SideBar,
            UserStats,
            TicketsBlock,
            Payment,
            PaymentResult,
            Calculate,
            Schedule,
            DatePicker,
        },
        props: {
            id: {
                type: String,
                default() { return null; }
            },
        },
        data() {
            return {
                masks: {
                    input: 'DD.MM.YYYY',
                },
                calendarConfig: {
                    type: 'string',
                    mask: 'YYYY-MM-DD'
                },
                user: this.$store.state.user,
                dateToPay: this.$helpers.formatDate(new Date(), 'YYYY-MM-DD'),
                showLoaderTicket: false,
                showModalPayment: false,
                showModalPaymentResult: false,
                showModalCalculate: false,
                showModalSchedule: false,
                showTicketsBlock: false,
                ticket: {},
                query: {}
            };
        },
        computed: {
        },
        created() {
            this.getTicket();
        },
        mounted() {
        },
        methods: {
            getTicket(checkResult = true) {
                let params = {
                    client_id: this.user.client_id,
                    ticket_id: this.id || null
                };
                this.showLoaderTicket = true;
                app.getTicket(params).then(res => {
                    this.showLoaderTicket = false;
                    console.log(res.result);
                    this.ticket = res.result || {};
                    let deltaDate = Math.ceil((this.$helpers.parseDate(this.ticket.Date, 'YYYY-MM-DD') - new Date()) / (1000 * 60 * 60 * 24));
                    if (deltaDate < 0) { deltaDate = 0; }
                    this.ticket.deltaDate = deltaDate;
                    let deltaGraceDate = Math.ceil((this.$helpers.parseDate(this.ticket.graceDate, 'YYYY-MM-DD') - new Date()) / (1000 * 60 * 60 * 24));
                    if (deltaGraceDate < 0) { deltaGraceDate = 0; }
                    this.ticket.deltaGraceDate = deltaGraceDate;
                    // Небольшие костыли пока. В ответе нет ticketId
                    if (!this.ticket.ticketId) {
                        this.ticket.ticketId = this.id;
                    }
                    let query = this.$router.currentRoute.value.query;
                    console.log(query);
                    if (query.ticket_id === this.id && query.ticket === this.ticket.ticket && checkResult) {
                        console.log('Проверка платежа!');
                        this.query = {
                            ticket: query.ticket,
                            ticket_id: query.ticket_id,
                            order: query.order,
                            amount: query.amount
                        };
                        this.showPaymentResult();
                    }
                }).catch(err => {
                    this.showLoaderTicket = false;
                    this.$store.dispatch('showError', err);
                    console.error(err);
                });
            },
            showPayment() {
                this.showModalPayment = true;
                this.ticket.dateToPay = this.dateToPay;
                console.log('Show Modal Payment', this.showModalPayment, this.ticket);
            },
            hidePayment() {
                this.showModalPayment = false;
            },
            showPaymentResult() {
                this.showModalPaymentResult = true;
                console.log('Show Modal Payment', this.showModalPaymentResult, this.ticket);
            },
            hidePaymentResult() {
                this.showModalPaymentResult = false;
                this.getTicket(false);
            },
            showCalculate() {
                this.showModalCalculate = true;
                this.ticket.dateToPay = this.dateToPay;
                console.log('Show Modal Calculate', this.showModalCalculate, this.ticket);
            },
            hideCalculate() {
                this.showModalCalculate = false;
            },
            showSchedule() {
                this.showModalSchedule = true;
                this.ticket.dateToPay = this.dateToPay;
                console.log('Show Modal Schedule', this.showModalSchedule, this.ticket);
            },
            hideSchedule() {
                this.showModalSchedule = false;
            },
        }
    };
</script>
