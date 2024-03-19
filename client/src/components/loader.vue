<template>
    <transition name="loader">
        <div
            v-if="isShown"
            class="loader"
        >
            <div class="loader__bg" />
            <div class="loader__container">
                <div class="loader__block">
                    <slot>
                        <div class="loader__spinner spinner" />
                        <div class="loader__label">
                            {{ label }}
                        </div>
                    </slot>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        props: {
            label: {
                type: String,
                default: ''
            },
            isShown: {
                type: Boolean,
                default: true
            }
        }
    };
</script>
