<template>
  <div>
    <div class="home backdrop">
      <HeaderComponent />
      <div class="main">
        <img alt="Vue logo" src="../assets/logo.png" />
        <h1></h1>
        <input type="text" ref="name" />
        <button @click="handleClick">Click Me!</button>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "HomeView",
  components: {
    HeaderComponent,
  },
  data() {
    return {
      title: "My First Vue app :)",
    };
  },
  methods: {
    handleClick() {
      console.log(this.$refs.name);
      this.$refs.name.classList.add("active");
      this.$refs.name.focus();
    },
  },
};
</script>
