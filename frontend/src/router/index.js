import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LoginView from '../views/LoginView.vue'
import StudentRegister from '../views/StudentRegister.vue'
import CompanyRegister from '../views/CompanyRegister.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import StudentDriveDetail from '../views/StudentDriveDetail.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import CreateDrive from '../views/CreateDrive.vue'
import CompanyDriveDetail from '../views/CompanyDriveDetail.vue'
import ApplicantDetail from '../views/ApplicantDetail.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminDriveDetail from '../views/AdminDriveDetail.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register/student', name: 'student-register', component: StudentRegister },
  { path: '/register/company', name: 'company-register', component: CompanyRegister },
  {
    path: '/student',
    name: 'student-dashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' },
  },
  {
    path: '/student/drive/:id',
    name: 'student-drive-detail',
    component: StudentDriveDetail,
    meta: { requiresAuth: true, role: 'student' },
  },
  {
    path: '/company',
    name: 'company-dashboard',
    component: CompanyDashboard,
    meta: { requiresAuth: true, role: 'company' },
  },
  {
    path: '/company/create-drive',
    name: 'create-drive',
    component: CreateDrive,
    meta: { requiresAuth: true, role: 'company' },
  },
  {
    path: '/company/drive/:id',
    name: 'company-drive-detail',
    component: CompanyDriveDetail,
    meta: { requiresAuth: true, role: 'company' },
  },
  {
    path: '/company/applicant/:id',
    name: 'applicant-detail',
    component: ApplicantDetail,
    meta: { requiresAuth: true, role: 'company' },
  },
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' },
  },
  {
    path: '/admin/drive/:id',
    name: 'admin-drive-detail',
    component: AdminDriveDetail,
    meta: { requiresAuth: true, role: 'admin' },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// simple auth + role guard
router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'login' }
  }

  // don't let a student open the company/admin page etc
  if (to.meta.role && auth.role !== to.meta.role) {
    return { name: 'login' }
  }

  return true
})

export default router
