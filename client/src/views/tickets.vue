<template>
    <div class="app__main tickets d-flex flex-row">
        <sideBar />

        <div class="app__block py-5">
            <userStats
                mClass="tickets__stats"
                :getData="false"
            />
            <routerView
                @showPayment="showPayment"
            />
        </div>
        <Payment 
            :show="showModalPayment"
            :ticket="ticket"
            @hidePayment="hidePayment"
        />
    </div>
</template>

<script>
    import sideBar from '@/components/side-bar';
    import userStats from '@/components/user-stats';
    import Payment from "@/components/payment";

    export default {
        name: 'tickets',
        components: {
            sideBar,
            userStats,
            Payment,
        },
        props: {
        },
        data() {
            return {
                user: this.$store.state.user,
                showModalPayment: false,
                ticket: {},
            };
        },
        computed: {
        },
        created() {
        },
        methods: {
            showPayment(ticket) {
                this.ticket = ticket;
                this.showModalPayment = true;
                console.log('Show Modal Payment', this.showModalPayment, ticket);
            },
            hidePayment() {
                this.showModalPayment = false;
            },
        }
    };
</script>
