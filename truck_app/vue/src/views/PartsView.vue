<template>
  <div>
    <div class="parts backdrop">
      <HeaderComponent />
      <div class="main">
        <h1>This is a parts page</h1>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "PartsView",
  components: {
    HeaderComponent,
  },
};
</script>
