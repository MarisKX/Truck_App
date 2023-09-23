<template>
  <div>
    <div class="maintenance backdrop">
      <HeaderComponent />
      <div class="main">
        <h1>This is a maintenance page</h1>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "MaintenanceView",
  components: {
    HeaderComponent,
  },
};
</script>
