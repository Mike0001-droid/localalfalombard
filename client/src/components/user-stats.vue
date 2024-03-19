<template>
    <div 
        class="stats mb-4 row flex-wrap"
        :class="mClass"
    >
        <div class="col mb-4">
            <b-card
                class="stats__item m--red"
            >
                <div class="stats__item-title">
                    {{ new Date().toLocaleDateString('ru') }}
                </div>
                <div class="stats__item-info">
                    {{ new Date().toLocaleDateString('ru', {weekday: 'long'}) }}
                </div>
            </b-card>
        </div>
        <div class="col mb-4">
            <b-card
                class="stats__item m--blue"
            >
                <div class="stats__item-title">
                    <template
                        v-if="showLoaderTickets"
                    >
                        <div class="stats__loader loader">
                            <b-spinner variant="light" class="me-2" />
                        </div>
                    </template>
                    <template
                        v-else-if="userStats"
                    >
                        {{ $helpers.toPrice(userStats.loanSum, { pointer: '.', sign: '₽' }) }}
                    </template>
                </div>
                <div class="stats__item-info">сумма займов</div>
            </b-card>
        </div>
        <div class="col mb-4">
            <b-card
                class="stats__item m--green"
            >
                <div class="stats__item-title">
                    <template
                        v-if="showLoaderTickets"
                    >
                        <div class="stats__loader loader">
                            <b-spinner variant="light" class="me-2" />
                        </div>
                    </template>
                    <template
                        v-else-if="userStats"
                    >
                        {{ $helpers.toPrice(userStats.debtSum, { pointer: '.', sign: '₽' }) }}
                    </template>
                </div>
                <div class="stats__item-info">% на сегодня</div>
            </b-card>
        </div>
        <div class="col mb-4">
            <b-card
                class="stats__item m--purple"
            >
                <div class="stats__item-title">
                    <template
                        v-if="showLoaderTickets"
                    >
                        <div class="stats__loader loader">
                            <b-spinner variant="light" class="me-2" />
                        </div>
                    </template>
                    <template
                        v-else-if="userStats"
                    >
                        {{ $helpers.toPrice(userStats.totalSum, { pointer: '.', sign: '₽' }) }}
                    </template>
                </div>
                <div class="stats__item-info">общий долг</div>
            </b-card>
        </div>
    </div>
</template>

<script>
    import { app } from "@/services";
    export default {
        name: 'UserStats',
        components: {
        },
        computed: {
            userStats() {
                return this.$store.state.userStats;
            }
        },
        props: {
            mClass: {
                type: String,
                default() { return null; }
            },
            getData: {
                type: Boolean,
                default() { return false; }
            }
        },
        created() {
        },
        mounted() {
            let getData = this.getData;
            let useStatsDate = this.userStats ? this.userStats.date * 1 : 0;
            if (Date.now() - useStatsDate > 300 * 1000) {
                getData = true;    
            }
            if (this.user && getData) {
                this.getStatsInfo();
            }
        },
        data() {
            return {
                user: this.$store.state.user,
                //userStats: this.$store.state.userStats,
                showLoaderTickets: false
            };
        },
        methods: {
            getStatsInfo() {
                let params = {
                    client_id: this.user.client_id
                };
                this.showLoaderTickets = true;
                app.getTickets(params).then(res => {
                    this.showLoaderTickets = false;
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
                    let userStats = {
                        loanSum: loanSum,
                        debtSum: debtSum,
                        totalSum: totalSum,
                        date: Date.now()
                    }
                    this.$store.dispatch('setUserStats', userStats);
                }).catch(err => {
                    this.showLoaderTickets = false;
                    //this.$store.dispatch('showError', err);
                    console.error(err);
                });
            }
        },
    };
</script>
