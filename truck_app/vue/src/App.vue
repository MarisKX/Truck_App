<template>
  <router-view />
</template>

<style lang="scss">
html,
body {
  height: 100%;
  margin: 0;
}

nav {
  padding: 30px;

  a {
    font-size: 1.5em;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
