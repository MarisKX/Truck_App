import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    isAuthenticated: false,
    userEmail: null,
  },
  getters: {},
  mutations: {
    setIsAuthenticated(state, value) {
      state.isAuthenticated = value;
    },
    setUserEmail(state, value) {
      state.userEmail = value;
    },
  },
  actions: {
    async checkAuthentication({ commit }) {
      try {
        const response = await axios.get(
          "http://dev.maris.com:8090/api/user/check-auth/",
          {
            withCredentials: true,
          }
        );

        if (response.data.authenticated) {
          // If authenticated, set isAuthenticated to true and set the userEmail
          commit("setIsAuthenticated", true);
          commit("setUserEmail", response.data.username); // Assuming the response contains 'username'
          console.log("setIsAuthenticated");
        } else {
          // Handle the case where authentication failed
          commit("setIsAuthenticated", false);
          console.log("setIsAuthenticated - false");
          document.cookie =
            "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
          console.log("Deleted auth_token");
          document.cookie =
            "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
          console.log("Deleted csrftoken");
        }
      } catch (err) {
        // Handle any other errors that might occur during the request
        console.error("Error:", err);
      }
    },
  },
  modules: {},
});
