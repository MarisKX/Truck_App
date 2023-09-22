import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    isAuthenticated: false,
  },
  getters: {},
  mutations: {
    setIsAuthenticated(state, value) {
      state.isAuthenticated = value;
    },
  },
  actions: {
    async checkAuthentication({ commit }) {
      try {
        await axios.get("http://dev.maris.com:8090/api/user/check-auth/", {
          withCredentials: true,
        });
        commit("setIsAuthenticated", true);
        console.log("setIsAuthenticated");
      } catch (err) {
        commit("setIsAuthenticated", false);
      }
    },
  },
  modules: {},
});
