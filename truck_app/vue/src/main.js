import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import store from "./store";
import router from "./router";
import axios from "axios";
import Cookies from "js-cookie"; // Import js-cookie library

axios.defaults.withCredentials = true;

// Set up Axios interceptor to include the token in headers
axios.interceptors.request.use((config) => {
  const token = Cookies.get("auth_token"); // Get the token from cookies
  //const token = "e716e7653c612808bd0de5a590d2a13fbb4707f6";
  console.log(token);
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Check authentication and create the app
store.dispatch("checkAuthentication").then(() => {
  createApp(App).use(store).use(router).mount("#app");
});
