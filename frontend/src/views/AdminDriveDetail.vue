<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const router = useRouter()

const driveId = Number(route.params.id)
const drive = ref(null)
const message = ref('')

async function load() {
  const res = await api.get('/admin/drives')
  drive.value = res.data.find((d) => d.id === driveId) || null
}

async function approve() {
  message.value = ''
  try {
    await api.put('/admin/drive/' + driveId + '/approve')
    message.value = 'Drive approved.'
    await load()
  } catch (err) {
    message.value = err.response?.data?.message || 'Could not approve'
  }
}

onMounted(load)
</script>

<template>
  <div>
    <button class="btn btn-link px-0 mb-2" @click="router.push('/admin')">&larr; Back to dashboard</button>

    <div v-if="message" class="alert alert-info py-2">{{ message }}</div>

    <div v-if="drive" class="card">
      <div class="card-body">
        <h3>{{ drive.title }}</h3>
        <h6 class="text-muted mb-3">{{ drive.company_name }}</h6>

        <p>
          <span :class="drive.approved ? 'badge bg-success' : 'badge bg-secondary'">
            {{ drive.approved ? 'Approved' : 'Pending Approval' }}
          </span>
          <span class="badge bg-info ms-1">{{ drive.status }}</span>
        </p>
        <p><strong>Location:</strong> {{ drive.location || '-' }}</p>
        <p><strong>Salary:</strong> {{ drive.salary || '-' }}</p>
        <p><strong>Deadline:</strong> {{ drive.deadline || '-' }}</p>
        <p><strong>Eligibility:</strong> {{ drive.eligibility || '-' }}</p>
        <p><strong>Description:</strong></p>
        <p>{{ drive.description || '-' }}</p>

        <button v-if="!drive.approved" class="btn btn-success" @click="approve">Approve Drive</button>
      </div>
    </div>

    <p v-else class="text-muted">Drive not found.</p>
  </div>
</template>
