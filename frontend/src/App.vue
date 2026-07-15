<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-dark bg-dark px-3">
    <span class="navbar-brand">Placement Portal</span>
    <div v-if="auth.isLoggedIn" class="d-flex align-items-center">
      <span class="text-light me-3 text-capitalize">{{ auth.role }}</span>
      <button class="btn btn-sm btn-outline-light" @click="logout">Logout</button>
    </div>
  </nav>

  <div class="container my-4">
    <router-view />
  </div>
</template>
