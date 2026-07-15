<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const form = ref({
  title: '',
  description: '',
  salary: '',
  location: '',
  eligibility: '',
  deadline: '',
})

const error = ref('')

async function createDrive() {
  error.value = ''
  try {
    await api.post('/company/drive', form.value)
    // go back to dashboard, drive will show up as pending approval
    router.push('/company')
  } catch (err) {
    error.value = err.response?.data?.message || 'Could not create drive'
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <button class="btn btn-link px-0 mb-2" @click="router.push('/company')">&larr; Back to dashboard</button>

      <div class="card">
        <div class="card-body">
          <h4 class="mb-3">Create a Drive</h4>

          <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

          <form @submit.prevent="createDrive">
            <div class="mb-3">
              <label class="form-label">Job Title</label>
              <input v-model="form.title" class="form-control" required />
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Location</label>
                <input v-model="form.location" class="form-control" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Salary</label>
                <input v-model="form.salary" type="number" class="form-control" />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Job Description</label>
              <textarea v-model="form.description" class="form-control" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label">Eligibility Criteria</label>
              <input v-model="form.eligibility" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">Application Deadline</label>
              <input v-model="form.deadline" type="date" class="form-control" required />
            </div>
            <button class="btn btn-primary">Save Drive</button>
          </form>
          <small class="text-muted d-block mt-2">Drive will be visible to students after admin approval.</small>
        </div>
      </div>
    </div>
  </div>
</template>
