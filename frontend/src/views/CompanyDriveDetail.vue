<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const router = useRouter()

const driveId = Number(route.params.id)
const drive = ref(null)
const applicants = ref([])

async function load() {
  const res = await api.get('/company/drives')
  drive.value = res.data.find((d) => d.id === driveId) || null

  // show who applied to this particular drive
  const apps = await api.get('/company/applications')
  applicants.value = apps.data.filter((a) => a.drive.id === driveId)
}

onMounted(load)
</script>

<template>
  <div>
    <button class="btn btn-link px-0 mb-2" @click="router.push('/company')">&larr; Back to dashboard</button>

    <div v-if="drive" class="card mb-4">
      <div class="card-body">
        <h3>{{ drive.title }}</h3>
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
      </div>
    </div>

    <p v-else class="text-muted">Drive not found.</p>

    <h5>Applicants for this drive</h5>
    <table class="table table-striped">
      <thead>
        <tr><th>Name</th><th>Department</th><th>Status</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-if="applicants.length === 0">
          <td colspan="4" class="text-muted">No applicants yet.</td>
        </tr>
        <tr v-for="app in applicants" :key="app.application_id">
          <td>{{ app.student.full_name }}</td>
          <td>{{ app.student.department || '-' }}</td>
          <td>{{ app.status }}</td>
          <td>
            <button class="btn btn-sm btn-outline-secondary" @click="router.push('/company/applicant/' + app.application_id)">
              View Student
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
