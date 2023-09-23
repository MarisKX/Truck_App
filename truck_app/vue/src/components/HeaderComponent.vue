<template>
  <nav class="navbar">
    <div class="navbar-left">
      <span v-if="isAuthenticated">
        <i class="fa-duotone fa-user-tie fa-2xl"> </i>
        <span class="useremail">{{ userEmail }}</span>
      </span>
    </div>
    <div class="navbar-center">
      <router-link to="/">Home</router-link> |
      <router-link to="/trucks">Trucks</router-link> |
      <router-link to="/maintenance">Maintenance</router-link> |
      <router-link to="/planing">Planing</router-link> |
      <router-link to="/parts">Parts</router-link>
    </div>
    <div class="navbar-right">
      <router-link to="/login" @click="logout">
        <i class="fa-duotone fa-person-to-door fa-xl"></i>
      </router-link>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
    userEmail() {
      const originalEmail = this.$store.state.userEmail;
      return originalEmail ? originalEmail.toUpperCase() : "";
    },
  },
  methods: {
    logout() {
      // Code to delete cookies
      this.$store.commit("setIsAuthenticated", false);
      document.cookie =
        "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      console.log("Deleted auth_token");
      document.cookie =
        "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      console.log("Deleted csrftoken");

      window.history.pushState(null, "", "/login");
      const currentPage = window.location.href;
      window.history.replaceState(null, "", currentPage);
    },
  },
};
</script>

<style scoped lang="scss">
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  height: 60px;
}

.navbar-center {
  flex-grow: 1; /* Allows "Home" and "About" to take available space */
}
.navbar-right {
  margin-right: 1%;
  padding-left: 9%;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
  text-decoration: none;
}
.useremail {
  font-size: 1.5em;
}
.fa-user-tie {
  margin: auto 25px;
}
.fa-person-to-door,
.fa-user-tie {
  --fa-primary-color: #bababa;
  --fa-secondary-color: #1c1c1c;
  --fa-secondary-opacity: 0.8;
}
</style>
