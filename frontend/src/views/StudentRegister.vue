<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const form = ref({
  full_name: '',
  email: '',
  password: '',
  department: '',
  cgpa: '',
  skills: '',
  phone: '',
  graduation_year: '',
})

const error = ref('')
const success = ref('')

async function register() {
  error.value = ''
  success.value = ''
  try {
    await api.post('/auth/register/student', form.value)
    success.value = 'Registered! You can login now.'
    setTimeout(() => router.push('/login'), 1200)
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
          <h4 class="mb-3">Student Registration</h4>

          <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2">{{ success }}</div>

          <form @submit.prevent="register">
            <div class="mb-3">
              <label class="form-label">Full Name</label>
              <input v-model="form.full_name" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Department</label>
                <input v-model="form.department" class="form-control" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">CGPA</label>
                <input v-model="form.cgpa" type="number" step="0.01" class="form-control" />
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Phone</label>
                <input v-model="form.phone" class="form-control" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Graduation Year</label>
                <input v-model="form.graduation_year" type="number" class="form-control" />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Skills</label>
              <textarea v-model="form.skills" class="form-control" rows="2"></textarea>
            </div>
            <button class="btn btn-primary">Register</button>
            <router-link to="/login" class="btn btn-link">Back to login</router-link>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
