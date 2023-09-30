import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import store from "./store";
import router from "./router";
import axios from "axios";
import "./assets/css/global.css";

axios.defaults.withCredentials = true;

// Check authentication and create the app
store.dispatch("checkAuthentication").then(() => {
  createApp(App).use(store).use(router).mount("#app");
});
