import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import UploadWizard from '../components/UploadWizard.vue'
import Dashboard from '../views/Dashboard.vue'
import Register from '../views/Register.vue'
import AnalysisDashboard from '../views/AnalysisDashboard.vue'


const routes = [
  { path: '/', component: Login },
  { path: '/upload', component: UploadWizard },
  { path: '/dashboard', component: AnalysisDashboard },
  { path: '/register', component: Register}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
