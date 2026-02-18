import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import AnalysisDashboard from "../views/AnalysisDashboard.vue";
import Analyses from "../views/AnalysesListView.vue";
import UploadWizard from "../views/UploadWizard.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/dashboard",
    component: AnalysisDashboard,
    meta: { title: "Dashboard" },
  },
  {
    path: "/analyses",
    component: Analyses,
    meta: { title: "My Analyses" },
  },
  {
    path: "/upload",
    component: UploadWizard,
    meta: { title: "Upload Data" },
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

  if (to.path !== '/login' && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router;
