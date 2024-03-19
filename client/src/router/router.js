import { createRouter, createWebHistory  } from 'vue-router';
import store from '@/store/store'
import help from '@/views/help.vue';
import home from '@/views/home.vue';
//import legal from '@/views/legal.vue';
import map from '@/views/map.vue';
import page from '@/views/page.vue';
//import policy from '@/views/policy.vue';
import profile from '@/views/profile.vue';
import ticket from '@/views/ticket.vue';
import tickets from '@/views/tickets.vue';
import ticketsBlock from '@/views/tickets-block.vue';
/*
import profile from '@/views/profile.vue';
import alerts from '@/views/alerts.vue';
import offer from '@/views/offer.vue';
import privacy from '@/views/privacy.vue';
*/
const routes = [
    {
        path: '/',
        name: 'home',
        component: home,
        meta: { title: null },
        props: true
    }, {
        path: '/tickets',
        name: 'tickets',
        component: tickets,
        meta: { requiresAuth: true },
        redirect: { name: 'tickets-all' },
        props: true,
        children: [
            {
                path: '/tickets/all',
                name: 'tickets-all',
                component: ticketsBlock,
                meta: { title: 'Каталог залоговых билетов', requiresAuth: true },
                props: { ticketState: 0 },
            }, {
                path: '/tickets/active',
                name: 'tickets-active',
                component: ticketsBlock,
                meta: { title: 'Активные залоговые билеты', requiresAuth: true },
                props: { ticketState: 1 },
            }, {
                path: '/tickets/overdue',
                name: 'tickets-overdue',
                component: ticketsBlock,
                meta: { title: 'Просроченные залоговые билеты', requiresAuth: true },
                props: { ticketState: 2 },
            }, {
                path: '/tickets/ransomed',
                name: 'tickets-ransomed',
                component: ticketsBlock,
                meta: { title: 'Выкупленные залоговые билеты', requiresAuth: true },
                props: { ticketState: 3 },
            }, {
                path: '/tickets/sales',
                name: 'tickets-sales',
                component: ticketsBlock,
                meta: { title: 'Залоговые билеты на реализации', requiresAuth: true },
                props: { ticketState: 4 },
            }
        ]
    }, {
        path: '/ticket/:id',
        name: 'ticket',
        component: ticket,
        meta: { title: 'Залоговый билет', requiresAuth: true },
        props: true
    }, {
        path: '/profile',
        name: 'profile',
        component: profile,
        //meta: { title: 'Настройки', showModal: 'shopProfile', requiresAuth: true },
        meta: { title: 'Настройки', requiresAuth: true },
        props: true
    }, {
        path: '/help',
        name: 'help',
        component: help,
        meta: { title: 'Помощь' },
        props: true
    }, {
        path: '/map',
        name: 'map',
        component: map,
        meta: { title: 'Отделения на карте' },
        props: true
    }, {
        path: '/question',
        name: 'question',
        component: tickets,
        meta: { title: 'Задать вопрос', requiresAuth: true },
        props: true

    }, {
        path: '/requisite',
        name: 'requisite',
        component: page,
        meta: { title: 'Реквизиты' },
        props: {
            slug: 'requisite'
        }
    }, {
        path: '/about',
        name: 'about',
        component: page,
        meta: { title: 'О компании' },
        props: {
            slug: 'about'
        }
    }, {
        path: '/agreement',
        name: 'agreement',
        component: page,
        meta: { title: 'Соглашение об обработке персональных данных' },
        props: {
            slug: 'agreement'
        }
    }, {
        path: '/personal-data',
        name: 'personal-data',
        component: page,
        meta: { title: 'Политика конфиденциальности' },
        props: {
            slug: 'personal-data'
        }
    }, {
        path: '/help',
        name: 'help',
        component: page,
        meta: { title: 'Справка' },
        props: {
            slug: 'help'
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: 'is-subactive',
    linkExactActiveClass: 'is-active',
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    },
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title ? to.meta.title + ' - Личный кабинет Омега Ломбард' : 'Личный кабинет Омега Ломбард';
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (store.state.user && store.state.user.client_id) {
            next();
        } else {
            next({ name: 'home' });
        }
    } else {
        //if (store.state.user && store.state.user.client_id && to.name === 'home') {
        //    next({ name: 'home' });
        //} else {
            next();
        //}
    }
});

export default router;
