<template>
    <div 
        class="tickets__item d-flex"
        :class="[tClass, `m--${status}`]"
    >
        <b-card
            class="tickets__item-inner"
            bodyClass="d-flex flex-column"
            :bg-variant="bgVariant"
        >
            <div class="tickets__item-top d-flex justify-content-center mb-4">
                <!--b-form-checkbox
                    v-visible="status === 'active'"
                    name="number"
                    variant="primary"
                /-->
                <div class="tickets__item-number">Билет №{{ ticket.ticket }}</div>
                <b-button
                    variant="outline-warning"
                    class="tickets__item-label"
                    :class="selected ? 'm--selected' : ''"
                    @click.prevent="changeSelected(ticket.ticket)"
                />
            </div>
            <div class="tickets__item-time mb-4">
                <template
                    v-if="status === 'active'"
                >
                    Осталось {{ $helpers.stringForNumber(deltaGraceDate, ['день', 'дня', 'дней']) }}
                </template>
                <template
                    v-else-if="status === 'ransom'"
                >
                    Выкуплен {{ $helpers.parseDate(ticket.ransomDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                </template>
                <template
                    v-else-if="status === 'overdue'"
                >
                    Просрочено на {{ $helpers.stringForNumber(deltaDate, ['день', 'дня', 'дней']) }}
                </template>
                <template
                    v-else-if="status === 'auction'"
                >
                    {{ ticket.sellDate ? $helpers.parseDate(ticket.sellDate, 'YYYY-MM-DD').toLocaleDateString('ru') : '\xa0' }}
                </template>
            </div>
            <div class="tickets__item-params">
                <div class="tickets__item-param">
                    <div class="tickets__item-param-name">Сумма займа (без %):</div>
                    <div class="tickets__item-param-value">{{ $helpers.toPrice(ticket.loanSum, { pointer: '.', sign: '₽' }) }}</div>
                </div>
                <div 
                    v-if="status !== 'auction'"
                    class="tickets__item-param"
                >
                    <div class="tickets__item-param-name">% на сегодня:</div>
                    <div class="tickets__item-param-value">{{ $helpers.toPrice(ticket.debtSum, { pointer: '.', sign: '₽' }) }}</div>
                </div>
                <div 
                    v-if="status !== 'auction'"
                    class="tickets__item-param"
                >
                    <div class="tickets__item-param-name">Общий долг (с %):</div>
                    <div class="tickets__item-param-value">{{ $helpers.toPrice(1 * ticket.totalSum, { pointer: '.', sign: '₽' }) }}</div>
                </div>
                <div class="tickets__item-param-devider"/>
                <div class="tickets__item-param">
                    <div class="tickets__item-param-name">
                        Дата оформления:
                    </div>
                    <div class="tickets__item-param-value">
                        {{ $helpers.parseDate(ticket.loanDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                    </div>
                </div>
                <div class="tickets__item-param">
                    <div class="tickets__item-param-name">
                        Окончание договора:
                    </div>
                    <div class="tickets__item-param-value">
                        {{ $helpers.parseDate(ticket.Date, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                    </div>
                </div>
                <div class="tickets__item-param">
                    <div class="tickets__item-param-name">
                        Льготный период:
                    </div>
                    <div class="tickets__item-param-value">
                        до {{ $helpers.parseDate(ticket.graceDate, 'YYYY-MM-DD').toLocaleDateString('ru') }}
                    </div>
                </div>
                <div class="tickets__item-param-devider"/>
                <div class="tickets__item-subject">
                    Предмет залога:
                    <ul>
                        <li
                            v-for="(item, index) in ticket.items"
                            :key="`t-${ticket.ticketId}-item-${index}`"
                        >
                            {{ item.name }}
                        </li>
                    </ul>
                </div>
            </div>
            <div class="tickets__item-buttons d-flex mb-2 mt-auto">
                <b-button
                    variant="outline-primary"
                    size=""
                    class="px-3"
                    :class="ticket.paymentEnabled ? 'ms-auto me-1' : 'mx-auto'"
                    pill
                    @click.prevent="ticketInfo(ticket.ticketId)"
                >
                    Подробнее
                </b-button>
                <b-button
                    v-if="ticket.paymentEnabled"
                    variant="primary"
                    size=""
                    class="px-3 ms-1 me-auto"
                    pill
                    @click.prevent="$emit('showPayment', ticket)"
                >
                    Оплатить
                </b-button>
            </div>
        </b-card>
    </div>
</template>

<script>
    import { app } from "@/services";

    export default {
        name: 'TicketItem',
        components: {
        },
        created() {

        },
        computed: {
            deltaGraceDate() {
                let deltaGraceDate = Math.ceil((this.$helpers.parseDate(this.ticket.graceDate, 'YYYY-MM-DD') - new Date()) / (1000 * 60 * 60 * 24));
                deltaGraceDate = Math.abs(deltaGraceDate);
                return deltaGraceDate;
            },
            deltaDate() {
                let deltaDate = Math.ceil((this.$helpers.parseDate(this.ticket.Date, 'YYYY-MM-DD') - new Date()) / (1000 * 60 * 60 * 24));
                deltaDate = Math.abs(deltaDate);
                return deltaDate;
            }
        },
        props: {
            ticket: {
                type: Object,
                default() { return {}; }
            },
            tClass: {
                type: String,
                default() { return 'col-12 col-lg-6 col-xl-4 col-xxl-3 mb-4'; }
            },
            bgVariant: {
                type: String,
                default() { return ''; }
            },
            status: {
                type: String,
                default() { return ''; }
            }
        },
        data() {
            return {
                selected: this.ticket.favorite,
            };
        },
        methods: {
            changeSelected(ticket) {
                let params = {
                    ticket: ticket
                };
                if (!this.selected) {
                    app.setTicketFavorite(params).then(res => {
                        console.log(res);
                        this.selected = true;
                    }).catch(err => {
                        this.$store.dispatch('showError', err);
                        console.error(err);
                    });
                } else {
                    app.unsetTicketFavorite(params).then(res => {
                        console.log(res);
                        this.selected = false;
                    }).catch(err => {
                        this.$store.dispatch('showError', err);
                        console.error(err);
                    });
                }
                console.log(this.selected);
            },
            ticketInfo(ticketId) {
                this.$router.push({ name: 'ticket', params: { id: ticketId } });
            },
        }
    };
</script>
