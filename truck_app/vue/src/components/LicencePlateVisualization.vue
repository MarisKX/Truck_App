<template>
  <div class="licence-plate-bg">
    <div v-for="(char, index) in splitChars" :key="index" class="custom-font">
      {{ char }}
    </div>
  </div>
</template>

<script>
export default {
  props: ["splitChars"],
};
</script>

<style>
.licence-plate-bg {
  background: url("@/assets/Wisconsin licence plate template.png") no-repeat
    center center;
  background-size: cover;
  padding-top: 17px;
  padding-left: 2px;
  padding-right: 2px;
  width: 230px;
  height: 100px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 3.4em;
  text-shadow: -2px -2px 0 #aaa, 2px -2px 0 #aaa, -2px 2px 0 #aaa,
    2px 2px 0 #aaa;
  display: flex;
  justify-content: center;
  align-items: center;
}
.custom-font {
  font-family: "Modulario", sans-serif;
  transform: scaleX(0.5);
  letter-spacing: -10px;
}
</style>
