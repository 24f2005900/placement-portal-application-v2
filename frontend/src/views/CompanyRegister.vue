<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const form = ref({
  company_name: '',
  hr_email: '',
  password: '',
  website: '',
  description: '',
})

const error = ref('')
const success = ref('')

async function register() {
  error.value = ''
  success.value = ''
  try {
    const res = await api.post('/auth/register/company', form.value)
    success.value = res.data.message || 'Registered. Awaiting admin approval.'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed'
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div class="card shadow-sm">
        <div class="card-body">
          <h4 class="mb-3">Company Registration</h4>

          <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2">{{ success }}</div>

          <form @submit.prevent="register">
            <div class="mb-3">
              <label class="form-label">Company Name</label>
              <input v-model="form.company_name" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">HR Email</label>
              <input v-model="form.hr_email" type="email" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Website</label>
              <input v-model="form.website" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">Description</label>
              <textarea v-model="form.description" class="form-control" rows="3"></textarea>
            </div>
            <button class="btn btn-primary">Register</button>
            <router-link to="/login" class="btn btn-link">Back to login</router-link>
          </form>
          <small class="text-muted">Note: company accounts need admin approval before login.</small>
        </div>
      </div>
    </div>
  </div>
</template>
