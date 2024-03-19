<template>
    <b-modal 
        v-model="showModal"
        classes="modal__container" 
        content-class="modal__block"
        title="Произошла ошибка"
        centered        
        hide-footer
        @hidden="hideModal"
    >
        <div class="modal__content">
            <p 
                v-for="(message, index) in errorMessages"
                :key="index"
                class="text-danger mb-1"
            >
                {{ message }}
            </p>
        </div>
    </b-modal>
</template>

<script>
    //import { logger } from '@/services';

    export default {
        components: {
        },
        computed: {
            showModal() {
                return this.error ? true : false;
            },
            error() {
                return this.$store.state.error;
            },
            errorMessages() {
                let messages = [];
                //console.log('ERROR', this.error.message);
                if (this.error) {
                    let err = this.error.err || this.error;
                    do {
                        messages.push(err.message);
                        err = err.parent;
                    } while (err);
                    this.$store.dispatch('hideError');
                }
                return messages;
            }
        },
        methods: {
            /*
            reportError() {
                if (this.error) {
                    logger.report(this.error);
                    this.hideError();
                }
            },
            */
            hideModal() {
                this.$store.dispatch('hideError');
                this.$store.dispatch('hideLoader');
            }
        }
    };
</script>
