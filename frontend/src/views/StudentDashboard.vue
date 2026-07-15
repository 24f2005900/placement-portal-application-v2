<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const student = ref(null)
const drives = ref([])
const appliedDriveIds = ref([])
const message = ref('')

async function loadDashboard() {
  const res = await api.get('/student/dashboard')
  student.value = res.data.student
  drives.value = res.data.drives
}

async function loadApplications() {
  const res = await api.get('/student/applications')
  appliedDriveIds.value = res.data.map((a) => a.drive_id)
}

function alreadyApplied(driveId) {
  return appliedDriveIds.value.includes(driveId)
}

async function apply(driveId) {
  message.value = ''
  try {
    const res = await api.post('/student/apply/' + driveId)
    message.value = res.data.message
    await loadApplications()
  } catch (err) {
    message.value = err.response?.data?.message || 'Could not apply'
  }
}

onMounted(async () => {
  await loadDashboard()
  await loadApplications()
})
</script>

<template>
  <div>
    <h3 v-if="student">Welcome, {{ student.full_name }}</h3>

    <div v-if="message" class="alert alert-info py-2">{{ message }}</div>

    <h5 class="mt-4">Available Drives</h5>
    <p v-if="drives.length === 0" class="text-muted">No approved drives right now.</p>

    <div class="row">
      <div v-for="drive in drives" :key="drive.id" class="col-md-6 mb-3">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ drive.title }}</h5>
            <h6 class="text-muted">{{ drive.company_name }}</h6>
            <p class="mb-1"><strong>Location:</strong> {{ drive.location || '-' }}</p>
            <p class="mb-1"><strong>Salary:</strong> {{ drive.salary || '-' }}</p>
            <p class="mb-2"><strong>Deadline:</strong> {{ drive.deadline || '-' }}</p>

            <button class="btn btn-sm btn-outline-primary me-1" @click="router.push('/student/drive/' + drive.id)">
              View Details
            </button>
            <button
              v-if="!alreadyApplied(drive.id)"
              class="btn btn-sm btn-primary"
              @click="apply(drive.id)"
            >
              Apply
            </button>
            <span v-else class="badge bg-success">Applied</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
