<template>
    <template
        v-if="showLoaderTickets"
    >
        <div class="tickets__loader loader">
            <b-spinner variant="primary" class="me-2" /> Загрузка данных
        </div>
    </template>
    <template
        v-else-if="!tickets.length"
    >
        <div
            class="h4"
        >
            По Вашему запросу билетов не найдено
        </div>
    </template>
    <template
        v-else
    >
        <template
            v-for="(status, key) in statuses"
            :key="key"
        >
            <template
                v-if="tickets.filter(item => item.status === key * 1).length"
            >
                <div class="tickets__title text-primary h3 mb-4">{{ status.title }} ({{ tickets.filter(item => item.status === key * 1).length }})</div>
                <div class="tickets__block row mb-4">
                    <ticketItem
                        v-for="ticket in tickets.filter(item => item.status === key * 1)"
                        :key="`ticket-${ticket.ticketId}`"
                        :ticket="ticket"
                        :status="status.status"
                        :bgVariant="status.variant"
                        @showPayment="showPayment"
                    />
                </div>
            </template>
        </template>
    </template>
</template>

<script>
    import { app } from "@/services";
    import ticketItem from "@/components/ticket-item";
    export default {
        name: 'ticketsBlock',
        components: {
            ticketItem
        },
        watch: {
            ticketState: {
                immediate: true,
                handler() {
                    let params = {
                        client_id: this.user.client_id,
                        status: this.ticketState
                    };
                    this.showLoaderTickets = true;
                    app.getTickets(params).then(res => {
                        this.showLoaderTickets = false;
                        let result = res.result;
                        let tickets = result.ticketsList ? result.ticketsList : [];
                        let favorites = res.favorites ? res.favorites : [];
                        tickets.forEach(ticket => {
                            if (favorites.findIndex(item => item.ticket === ticket.ticket) !== -1) {
                                ticket.favorite = true;
                            } else {
                                ticket.favorite = false;
                            }
                        });
                        tickets = tickets.sort((a, b) => {
                            if (a.favorite && !b.favorite)
                                return -1;
                            if (!a.favorite && b.favorite)
                                return 1;
                            return 0;
                        });
                        this.tickets = tickets;
                    }).catch(err => {
                        this.showLoaderTickets = false;
                        //this.$store.dispatch('showError', err);
                        this.formErrors = { 
                            email: 1,
                            password: 1,
                            detail: err.response.data.detail
                        }
                        console.error(err);
                    });
                }
            },
        },
        props: {
            ticketState: {
                type: Number,
                default() { return 0; }
            }
        },
        data() {
            return {
                tickets: [],
                user: this.$store.state.user,
                showLoaderTickets: false,
                statuses: {
                    1: {
                        title: 'Активные билеты',
                        variant: 'warning-light',
                        status: 'active'
                    },
                    2: {
                        title: 'Просроченные билеты',
                        variant: 'danger-light',
                        status: 'overdue'
                    },
                    3: {
                        title: 'Выкупленные билеты',
                        variant: 'success-light',
                        status: 'ransom'
                    },
                    4: {
                        title: 'Билеты на реализации',
                        variant: 'secondary-light',
                        status: 'auction'
                    },
                }
            };
        },
        computed: {
        },
        created() {
        },
        mounted() {
        },
        methods: {
            showPayment(ticket) {
                this.$emit('showPayment', ticket);
            }
        }
    };
</script>
