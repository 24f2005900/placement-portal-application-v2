<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const router = useRouter()

const appId = Number(route.params.id)
const app = ref(null)
const message = ref('')

const statuses = ['Applied', 'Shortlisted', 'Interview', 'Selected', 'Rejected']

async function load() {
  const res = await api.get('/company/applications')
  app.value = res.data.find((a) => a.application_id === appId) || null
}

async function save() {
  message.value = ''
  try {
    await api.put('/company/applications/' + appId, {
      status: app.value.status,
      remarks: app.value.remarks || '',
    })
    message.value = 'Application updated.'
  } catch (err) {
    message.value = err.response?.data?.message || 'Update failed'
  }
}

onMounted(load)
</script>

<template>
  <div>
    <button class="btn btn-link px-0 mb-2" @click="router.back()">&larr; Back</button>

    <div v-if="message" class="alert alert-info py-2">{{ message }}</div>

    <div v-if="app" class="card">
      <div class="card-body">
        <h3>{{ app.student.full_name }}</h3>
        <h6 class="text-muted mb-3">Applied for: {{ app.drive.title }}</h6>

        <p><strong>Email:</strong> {{ app.student.email }}</p>
        <p><strong>Phone:</strong> {{ app.student.phone || '-' }}</p>
        <p><strong>Department:</strong> {{ app.student.department || '-' }}</p>
        <p><strong>CGPA:</strong> {{ app.student.cgpa ?? '-' }}</p>
        <p><strong>Graduation Year:</strong> {{ app.student.graduation_year || '-' }}</p>
        <p><strong>Skills:</strong> {{ app.student.skills || '-' }}</p>
        <p><strong>Resume:</strong> {{ app.student.resume || 'Not uploaded' }}</p>
        <p><strong>Applied At:</strong> {{ app.applied_at }}</p>

        <hr />
        <h5>Update Application</h5>
        <div class="row g-2 align-items-end">
          <div class="col-md-4">
            <label class="form-label">Status</label>
            <select v-model="app.status" class="form-select">
              <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="col-md-5">
            <label class="form-label">Remarks</label>
            <input v-model="app.remarks" class="form-control" placeholder="remarks" />
          </div>
          <div class="col-md-3">
            <button class="btn btn-primary w-100" @click="save">Save</button>
          </div>
        </div>
      </div>
    </div>

    <p v-else class="text-muted">Applicant not found.</p>
  </div>
</template>
