<template>
    <div class="app__menu menu">
        <template
            v-for="(mitem, index) in menu"
            :key="`menu-${index}`"
        >

            <template
                v-for="item in mitem"
                :key="item.name"
            >
                <template
                    v-if="item.action"
                >
                    <div 
                        class="menu__item"
                    >
                        <a 
                            class="menu__item-link"
                            :class="['m--' + item.icon]"
                            href="#" 
                            @click.prevent="handleClick(item.action)"
                        >
                            {{ item.title }}
                        </a>
                    </div>                
                </template>
                <template
                    v-else
                >
                    <router-link
                        :to="{ name: item.name }"
                        custom
                        v-slot="{ href, navigate, isActive, isExactActive }"
                    >        
                        <div 
                            class="menu__item"
                            :class="[isActive && 'is-active', isExactActive && 'is-subactive']"
                        >
                            <a
                                class="menu__item-link"
                                :class="['m--' + item.icon]"
                                :href="href" 
                                @click="navigate"
                            >
                                {{ item.title }}
                            </a>
                            <b-button
                                v-if="item.subitems"
                                v-b-toggle="`collapse-${item.name}`"
                                class="menu__item-collapse"
                                aria-expanded="true"
                            >
                            </b-button>
                        </div>
                        <b-collapse
                            v-if="item.subitems"
                            :modelValue="true"
                            :id="`collapse-${item.name}`" 
                        >
                            <router-link
                                v-for="sitem in item.subitems"
                                :key="sitem.name"
                                :to="{ name: sitem.name }"
                                custom
                                v-slot="{ href, navigate, isExactActive }"
                            >        
                                <div 
                                    class="menu__item"
                                    :class="[isExactActive && 'is-subactive']"
                                >
                                    <a 
                                        class="menu__item-link"
                                        :href="href" 
                                        @click="navigate"
                                    >
                                        {{ sitem.title }}
                                    </a>
                                </div>
                            </router-link>
                        </b-collapse>
                    </router-link>    
                </template>
            </template>
            <div class="menu__item m--devider"/>
        </template>
        <div class="menu__item">
            <a 
                href="#" 
                class="menu__item-link"
                @click.prevent="logout"
            >
                Выйти
            </a>
        </div>
        <Profile 
            :show="showModalProfile"
            @hideProfile="hideProfile"
        />
        <Question 
            :show="showModalQuestion"
            @hideQuestion="hideQuestion"
        />
    </div>
</template>

<script>
    //import { mainMenu, advancedMenu } from '@/settings';
    import Profile from "@/components/profile";
    import Question from "@/components/question";

    export default {
        name: 'SideBar',
        components: {
            Profile,
            Question
        },
        computed: {
        },
        props: {
        },
        created() {
        },
        data() {
            return {
                menu: [[{
                    name: 'tickets',
                    role: 'all',
                    icon: 'tickets',
                    title: 'Все билеты',
                    subitems: [{
                        name: 'tickets-active',
                        role: 'all',
                        title: 'Активные билеты',
                    }, {
                        name: 'tickets-overdue',
                        role: 'all',
                        title: 'Просроченные билеты',
                    }, {
                        name: 'tickets-ransomed',
                        role: 'all',
                        title: 'Выкупленные билеты',
                    }, {
                        name: 'tickets-sales',
                        role: 'all',
                        title: 'Билеты на реализации',
                    }]
                }, {
                    name: 'profile',
                    role: 'all',
                    icon: 'profile',
                    title: 'Настройки',
                    //action: 'showProfile'
                }], [{
                /*
                    name: 'help',
                    role: 'all',
                    icon: 'help',
                    title: 'Помощь'
                }, {
                */
                    name: 'map',
                    role: 'all',
                    icon: 'map',
                    title: 'Отделения на карте'
                }, {
                    name: 'question',
                    role: 'all',
                    icon: 'question',
                    title: 'Задать вопрос',
                    action: 'showQuestion'
                }]],
                showModalProfile: false,
                showModalQuestion: false,
            };
        },
        methods: {
            handleClick(action) {
                if (action === 'showProfile') {
                    this.showProfile(action);
                }
                if (action === 'showQuestion') {
                    this.showQuestion(action);
                }
            },
            showProfile() {
                this.showModalProfile = true;
                console.log('Show Modal Profile', this.showModalProfile);
            },
            hideProfile() {
                this.showModalProfile = false;
                console.log('Show Modal Profile', this.showModalProfile);
            },
            showQuestion() {
                this.showModalQuestion = true;
                console.log('Show Modal Question', this.showModalQuestion);
            },
            hideQuestion() {
                this.showModalQuestion = false;
                console.log('Show Modal Question', this.showModalQuestion);
            },
            logout() {
                this.$store.dispatch('clearUser');
                this.$store.dispatch('clearToken');
                this.$router.push({ name: 'home' });
            }
        },
    };
</script>
