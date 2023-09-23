import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/trucks",
    name: "trucks",
    component: () =>
      import(/* webpackChunkName: "trucks" */ "../views/TrucksView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/truck-details/:id",
    name: "truck-details",
    component: () =>
      import(/* webpackChunkName: "trucks" */ "../views/TruckDetailsView.vue"),
    meta: { requiresAuth: true },
    props: true, // This line is important
  },
  {
    path: "/maintenance",
    name: "maintenance",
    component: () =>
      import(
        /* webpackChunkName: "maintenance" */ "../views/MaintenanceView.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/planing",
    name: "planing",
    component: () =>
      import(/* webpackChunkName: "planning" */ "../views/PlaningView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/parts",
    name: "parts",
    component: () =>
      import(/* webpackChunkName: "parts" */ "../views/PartsView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/LoginView.vue"),
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.isAuthenticated;
  console.log(isAuthenticated);
  if (!isAuthenticated) {
    document.cookie =
      "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }

  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !isAuthenticated
  ) {
    next({ name: "login" });
  } else {
    next();
  }
});

export default router;
