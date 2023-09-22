<template>
  <LoginDialog />
</template>

<script>
import LoginDialog from "../components/LoginDialog.vue";
export default {
  components: {
    LoginDialog,
  },
};
</script>

<style>
.login {
  width: 50%;
  padding: 20px;
  margin: 10% auto;
  background: white;
  opacity: 0.6;
  border-radius: 12px;
}
.backdrop {
  top: 0;
  position: fixed;
  background: rgba(0, 0, 0, 0.6);
  width: 100%;
  height: 100%;
}
</style>
