import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import AnalysisDashboard from "../views/AnalysisDashboard.vue";
import Analyses from "../views/AnalysesListView.vue";
import UploadWizard from "../views/UploadWizard.vue";
import Register from "../views/Register.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/login",
    component: Login,
    meta: { title: "Login", guestOnly: true },
  },
  {
    path: "/dashboard",
    component: AnalysisDashboard,
    meta: { title: "Dashboard", requiresAuth: true },
  },
  {
    path: "/analyses",
    component: Analyses,
    meta: { title: "My Analyses", requiresAuth: true },
  },
  {
    path: "/upload",
    component: UploadWizard,
    meta: { title: "Upload Data", requiresAuth: true },
  },
  {
    path: "/register",
    component: Register,
    meta: { title: "Register", guestOnly: true },

  },

  // временни празни страници
  {
    path: "/billing",
    component: { template: "<div>Billing (coming soon)</div>" },
  },
  {
    path: "/settings",
    component: { template: "<div>Settings (coming soon)</div>" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('bi_saas_token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.guestOnly && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router;
