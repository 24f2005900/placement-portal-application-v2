<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const company = ref(null)
const drives = ref([])
const applicants = ref([])

async function loadDashboard() {
  const res = await api.get('/company/dashboard')
  company.value = res.data.company
  drives.value = res.data.drives
}

async function loadApplicants() {
  const res = await api.get('/company/applications')
  applicants.value = res.data
}

onMounted(async () => {
  await loadDashboard()
  await loadApplicants()
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center">
      <h3 v-if="company">{{ company.company_name }}</h3>
      <router-link to="/company/create-drive" class="btn btn-primary">+ Create Drive</router-link>
    </div>

    <!-- my drives -->
    <h5 class="mt-4">My Drives</h5>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Title</th>
          <th>Location</th>
          <th>Deadline</th>
          <th>Approved?</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="drives.length === 0">
          <td colspan="5" class="text-muted">No drives yet.</td>
        </tr>
        <tr v-for="d in drives" :key="d.id">
          <td>{{ d.title }}</td>
          <td>{{ d.location || '-' }}</td>
          <td>{{ d.deadline || '-' }}</td>
          <td>
            <span :class="d.approved ? 'badge bg-success' : 'badge bg-secondary'">
              {{ d.approved ? 'Approved' : 'Pending' }}
            </span>
          </td>
          <td>
            <button class="btn btn-sm btn-outline-primary" @click="router.push('/company/drive/' + d.id)">
              View Details
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- applicants -->
    <h5 class="mt-4">Applicants</h5>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Student</th>
          <th>Department</th>
          <th>Drive</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="applicants.length === 0">
          <td colspan="5" class="text-muted">No applications yet.</td>
        </tr>
        <tr v-for="app in applicants" :key="app.application_id">
          <td>{{ app.student.full_name }}</td>
          <td>{{ app.student.department || '-' }}</td>
          <td>{{ app.drive.title }}</td>
          <td>{{ app.status }}</td>
          <td>
            <button class="btn btn-sm btn-outline-primary" @click="router.push('/company/applicant/' + app.application_id)">
              View Details
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
