<template>
    <div 
        class="app__main map d-flex"
        :class="user ? 'flex-row' : 'flex-column'"
    >
        <SideBar
            v-if="user"
        />

        <div 
            class="app__block py-5"
            :class="user ? '' : 'm--width-100'"
        >
            <h1 class="h3 text-primary text-uppercase mb-4">Отделения на карте</h1>
            <div class="map__block">
                <div style="position:relative;overflow:hidden;"><a href="https://yandex.ru/maps/50/perm/search/%D0%B0%D0%BB%D1%8C%D1%84%D0%B0%20%D0%BB%D0%BE%D0%BC%D0%B1%D0%B0%D1%80%D0%B4%20%D0%BF%D0%B5%D1%80%D0%BC%D1%8C/?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:0px;">альфа ломбард пермь в Перми</a><a href="https://yandex.ru/maps/50/perm/?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:14px;">Пермь</a><iframe src="https://yandex.ru/map-widget/v1/-/CCUREJSlgA" width="100%" height="100%" frameborder="1" allowfullscreen="true" style="position:relative;"></iframe></div>
            </div>
        </div>
    </div>
</template>

<script>
    import SideBar from '@/components/side-bar';
    export default {
        name: 'map',
        components: {
            SideBar
        },
        props: {
        },
        data() {
            return {
                user: this.$store.state.user
            };
        },
        computed: {
        },
        created() {
        },
        methods: {
        }
    };
</script>
