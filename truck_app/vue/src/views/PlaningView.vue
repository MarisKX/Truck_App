<template>
  <div>
    <div class="planning backdrop">
      <HeaderComponent />
      <div class="main">
        <h1>This is a planning page</h1>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "PlanningView",
  components: {
    HeaderComponent,
  },
};
</script>
