<template>
  <div class="about">
    <HeaderComponent />
    <h1>This is an about page</h1>
  </div>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "AboutView",
  components: {
    HeaderComponent,
  },
};
</script>
