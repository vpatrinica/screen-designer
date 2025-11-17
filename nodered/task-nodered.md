
Example of template to generate:

<template>
    <div>
        <h2>Counter</h2>
        <!-- Conditional Styling using Attribute Binding (":") -->
        <!-- and rendering content inside <tags></tags> with {{ }} -->
        <p :style="{'color' : (count > 5 ? 'red' : 'green' )}">Current Count: {{ count }}</p>
        <!-- Computed Rendering using Vue Computed Variables -->
        <p class="my-class">Formatted Count: {{ formattedCount }}</p>
        <!-- Conditional Rendering with "v-if" -->
        <b v-if="count > 5">Too many!</b>
        <v-btn @click="increase()">Increment</v-btn>
    </div>
</template>

<script>
    export default {
        data() {
            // define variables available component-wide
            // (in <template> and component functions)
            return {
                count: 0
            }
        },
        watch: {
            // watch for any changes of "count"
            count: function () {
                if (this.count % 5 === 0) {
                    this.send({payload: 'Multiple of 5'})
                }
            }
        },
        computed: {
            // automatically compute this variable
            // whenever VueJS deems appropriate
            formattedCount: function () {
                return this.count + ' Apples'
            }
        },
        methods: {
            // expose a method to our <template> and Vue Application
            increase: function () {
                this.count++
            }
        },
        mounted() {
            // code here when the component is first loaded
        },
        unmounted() {
            // code here when the component is removed from the Dashboard
            // i.e. when the user navigates away from the page
        }
    }
</script>
<style>
    /* define any styles here - supports raw CSS */
    .my-class {
        color: red;
    }
</style>