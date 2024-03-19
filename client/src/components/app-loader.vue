<template>
    <loader
        :is-shown="!!loader"
        :label="loaderLabel"
    />
</template>

<script>
    import loader from './loader.vue';

    export default {
        components: {
            loader
        },
        computed: {
            loader() {
                return this.$store.state.loader;
            },
            loaderLabel() {
                return this.loader && this.loader.label;
            }
        }
    };
</script>
