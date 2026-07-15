<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const router = useRouter()

const driveId = Number(route.params.id)
const drive = ref(null)
const applied = ref(false)
const message = ref('')

async function load() {
  // reuse the dashboard endpoint and pick this drive out of the list
  const res = await api.get('/student/dashboard')
  drive.value = res.data.drives.find((d) => d.id === driveId) || null

  const apps = await api.get('/student/applications')
  applied.value = apps.data.some((a) => a.drive_id === driveId)
}

async function apply() {
  message.value = ''
  try {
    const res = await api.post('/student/apply/' + driveId)
    message.value = res.data.message
    applied.value = true
  } catch (err) {
    message.value = err.response?.data?.message || 'Could not apply'
  }
}

onMounted(load)
</script>

<template>
  <div>
    <button class="btn btn-link px-0 mb-2" @click="router.push('/student')">&larr; Back to dashboard</button>

    <div v-if="message" class="alert alert-info py-2">{{ message }}</div>

    <div v-if="drive" class="card">
      <div class="card-body">
        <h3>{{ drive.title }}</h3>
        <h6 class="text-muted mb-3">{{ drive.company_name }}</h6>

        <p><strong>Location:</strong> {{ drive.location || '-' }}</p>
        <p><strong>Salary:</strong> {{ drive.salary || '-' }}</p>
        <p><strong>Deadline:</strong> {{ drive.deadline || '-' }}</p>
        <p><strong>Eligibility:</strong> {{ drive.eligibility || '-' }}</p>
        <p><strong>Description:</strong></p>
        <p>{{ drive.description || '-' }}</p>

        <button v-if="!applied" class="btn btn-primary" @click="apply">Apply</button>
        <span v-else class="badge bg-success fs-6">Already Applied</span>
      </div>
    </div>

    <p v-else class="text-muted">Drive not found.</p>
  </div>
</template>
