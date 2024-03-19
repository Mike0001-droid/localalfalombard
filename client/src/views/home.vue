<template>
    <div class="app__main home d-flex flex-column py-5">
        <b-card
            bg-variant="danger-light"
            border-variant="danger"
            class="home__block p-1 mb-5"
            bodyClass="mt-3"
        >
            <b-card-text>
                <h4 class="text-danger pb-2"><strong>Уважаемые залогодатели!</strong></h4>
                <p>В связи с началом работы нашего Личного кабинета возможно появление технических неисправностей. Убедительная просьба отнестись к этому с пониманием! Мы постоянно работаем над их устранением!</p>
                <p>Спасибо!</p>
                <p><strong class="text-muted">Администрация Личного кабинета</strong></p>
            </b-card-text>
        </b-card>
        <b-card
            bg-variant="primary-light"
            border-variant="primary"
            class="home__block p-1 mb-5"
            bodyClass="mt-3"
        >
            <b-card-text>
                <h4 class="text-primary pb-2"><strong>Зачем мне личный кабинет?</strong></h4>
                <p>В ЛИЧНОМ КАБИНЕТЕ Вы можете оплатить % и сумму займа, даже если под рукой нет номера залогового билета, а также узнать ВСЮ информацию о своих залоговых билетах (действующих и погашенных):</p>
                <ul>
                    <li>№ залогового билета</li>
                    <li>Сумма займа</li>
                    <li>Дата оформления</li>
                    <li>Дата возврата займа (после этой даты у Вас есть не менее 30-ти дней льготного месячного срока, который предоставлен любому клиенту ломбарда Законом о ломбардах)</li>
                    <li>Срок хранения имущества в ломбарде</li>
                    <li>Дата последней оплаты %</li>
                    <li>Статус залогового имущества (в ломбарде, выкуплено, отправлено на реализацию)</li>
                    <li>Предмет залога (описание)</li>
                    <li>Рассчитать % за нужный период</li>
                    <li>График начисления % на каждый день займа (дата, сумма, процентная ставка)</li>
                    <li>Возможность написать в службу поддержки</li>
                </ul>
            </b-card-text>
        </b-card>
        <b-card
            bg-variant="success-light"
            border-variant="success"
            class="home__block p-1 mb-5"
            bodyClass="mt-3"
        >
            <b-card-text>
                <h4 class="text-success pb-2"><strong>Как зарегистрироваться?</strong></h4>
                <p>Зарегистрироваться может тот, кто хотя бы раз пользовался нашими услугами и указал свой телефонный номер в одном из отделений нашей сети. Важно, чтобы телефон был актуальный!</p>
                <ul>
                    <li>Нажмите «Зарегистрироваться»</li>
                    <li>Укажите серию/номер паспорта и номер телефона, который Вы сообщали товароведу в ломбарде!</li>
                    <li>Введите и сохраните свой пароль</li>
                    <li>Поздравляем! Возможности Личного кабинета – в Вашем распоряжении.</li>
                </ul>
            </b-card-text>
        </b-card>
        <b-card
            bg-variant="warning-light"
            border-variant="warning"
            class="home__block p-1 mb-5"
            bodyClass="mt-3"
        >
            <b-card-text>
                <h4 class="text-warning pb-2"><strong>Если не удается зарегистрироваться или войти</strong></h4>
                <p><strong>Не вводятся цифры или другие символы при регистрации. </strong><br>
                Попробуйте зайти на страницу с другого браузера, либо перезагрузите страницу, нажав на клавиатуре персонального компьютера клавишу «F5» или одновременно клавиши «Ctrl» и «F5».</p>

                <p>Кроме телефонного номера неверными могут быть также и серия и номер паспорта. Поэтому, текст данного абзаца будет, скорее всего, таким:<br>
                <strong>Вы ввели паспортные данные и номер телефона, но на экране появилась надпись: «Клиент не найден по переданным параметрам».</strong><br>
                Убедитесь, что Вы ввели именно те паспортные данные и тот номер телефона, который Вы сообщили товароведу в ломбарде.</p>

                <p>Проверьте пароль - он должен состоять как минимум из 4-х и максимум до 16 символов (букв и/или цифр).<br>
                Не используйте спецсимволы (знаки препинания, символы = +, @, %, $ и т.д.) при создании пароля.</p>

                <p><strong>Если Вы забыли пароль.</strong><br>
                Не беспокойтесь: чтобы завести новый пароль, просто пройдите заново регистрацию (введите серию и номер паспорта, номер телефона).</p>
            </b-card-text>
        </b-card>
    </div>
</template>

<script>
    export default {
        name: 'home',
        components: {
        },
        props: {
        },
        data() {
            return {
                showModalAuthorization: false,
                showModalRecovery: false,
                showModalRegistration: false
            };
        },
        computed: {
        },
        created() {
        },
        methods: {
            showAuthorization() {
                this.showModalAuthorization = true;
                console.log('Show Modal Authorization', this.showModalAuthorization);
            },
            hideAuthorization(props={}) {
                this.showModalAuthorization = false;
                if (props.show == 'recovery') {
                    this.showRecovery();    
                }
            },
            showRecovery() {
                this.showModalRecovery = true;
                console.log('Show Modal Recovery', this.showModalRecovery);
            },
            hideRecovery() {
                this.showModalRecovery = false;
            },
            showRegistration() {
                this.showModalRegistration = true;
                console.log('Show Modal Recovery', this.showModalRegistration);
            },
            hideRegistration() {
                this.showModalRegistration = false;
            },
        }
    };
</script>
