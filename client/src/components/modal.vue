<template>
    <transition name="modal">
        <div
            v-if="isShown"
            class="modal"
        >
            <div
                class="modal__bg"
                @click="hide"
            />
            <div class="modal__container">
                <div class="modal__block">
                    <div class="modal__head">
                        <slot name="header">
                            <div
                                v-if="header"
                                class="modal__header h2"
                            >
                                {{ header }}
                            </div>
                        </slot>
                    </div>
                    <div class="modal__body">
                        <slot name="content">
                            <div
                                v-if="content"
                                class="modal__content text"
                            >
                                {{ content }}
                            </div>
                        </slot>
                    </div>
                    <div
                        class="modal__date"
                    >
                        {{ datetime }}
                    </div>
                    <div class="modal__foot">
                        <slot name="footer">
                            <div
                                v-if="footer"
                                class="modal__footer text"
                            >
                                {{ footer }}
                            </div>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        props: {
            header: {
                type: String,
                default: ''
            },
            content: {
                type: String,
                default: ''
            },
            footer: {
                type: String,
                default: ''
            },
            isShown: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            datetime() {
                let today = new Date();
                return today.toUTCString();
            }
        },
        methods: {
            hide() {
                this.$emit('hide');
            }
        }
    };
</script>
