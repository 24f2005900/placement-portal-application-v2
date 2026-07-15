<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

async function doLogin() {
  error.value = ''
  try {
    const role = await auth.login(username.value, password.value)
    // send each role to its own dashboard
    if (role === 'admin') {
      router.push('/admin')
    } else if (role === 'company') {
      router.push('/company')
    } else {
      router.push('/student')
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed'
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-5">
      <div class="card shadow-sm">
        <div class="card-body">
          <h4 class="card-title mb-3">Login</h4>

          <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

          <form @submit.prevent="doLogin">
            <div class="mb-3">
              <label class="form-label">Username / Email</label>
              <input v-model="username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </form>

          <hr />
          <p class="mb-1">
            New student? <router-link to="/register/student">Register here</router-link>
          </p>
          <p class="mb-0">
            Company? <router-link to="/register/company">Register your company</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
