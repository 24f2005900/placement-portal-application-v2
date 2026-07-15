<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const stats = ref({})
const companies = ref([])
const drives = ref([])
const students = ref([])
const message = ref('')

async function loadAll() {
  const [s, c, d, st] = await Promise.all([
    api.get('/admin/dashboard'),
    api.get('/admin/companies'),
    api.get('/admin/drives'),
    api.get('/admin/students'),
  ])
  stats.value = s.data
  companies.value = c.data
  drives.value = d.data
  students.value = st.data
}

async function approveCompany(id) {
  await api.put('/admin/company/' + id + '/approve')
  message.value = 'Company approved'
  await loadAll()
}

async function blacklistCompany(id) {
  await api.put('/admin/company/' + id + '/blacklist')
  message.value = 'Company blacklisted'
  await loadAll()
}

async function whitelistCompany(id) {
  await api.put('/admin/company/' + id + '/whitelist')
  message.value = 'Company removed from blacklist'
  await loadAll()
}

async function deactivateStudent(id) {
  await api.put('/admin/student/' + id + '/deactivate')
  message.value = 'Student deactivated'
  await loadAll()
}

async function activateStudent(id) {
  await api.put('/admin/student/' + id + '/activate')
  message.value = 'Student activated'
  await loadAll()
}

onMounted(loadAll)
</script>

<template>
  <div>
    <h3>Admin Dashboard</h3>

    <div v-if="message" class="alert alert-info py-2">{{ message }}</div>

    <!-- quick counts -->
    <div class="row mb-4">
      <div class="col">
        <div class="card text-center"><div class="card-body"><h4>{{ stats.students }}</h4><small>Students</small></div></div>
      </div>
      <div class="col">
        <div class="card text-center"><div class="card-body"><h4>{{ stats.companies }}</h4><small>Companies</small></div></div>
      </div>
      <div class="col">
        <div class="card text-center"><div class="card-body"><h4>{{ stats.drives }}</h4><small>Drives</small></div></div>
      </div>
      <div class="col">
        <div class="card text-center"><div class="card-body"><h4>{{ stats.applications }}</h4><small>Applications</small></div></div>
      </div>
    </div>

    <!-- companies -->
    <h5>Companies</h5>
    <table class="table table-bordered">
      <thead>
        <tr><th>Name</th><th>HR Email</th><th>Status</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="c in companies" :key="c.id">
          <td>{{ c.company_name }}</td>
          <td>{{ c.hr_email }}</td>
          <td>
            <span :class="c.approved ? 'badge bg-success' : 'badge bg-secondary'">
              {{ c.approved ? 'Approved' : 'Not approved' }}
            </span>
            <span v-if="c.blacklisted" class="badge bg-danger ms-1">Blacklisted</span>
          </td>
          <td>
            <button v-if="!c.approved" class="btn btn-sm btn-success me-1" @click="approveCompany(c.id)">Approve</button>
            <button v-if="!c.blacklisted" class="btn btn-sm btn-danger" @click="blacklistCompany(c.id)">Blacklist</button>
            <button v-else class="btn btn-sm btn-warning" @click="whitelistCompany(c.id)">Whitelist</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- drives -->
    <h5 class="mt-4">Drives</h5>
    <table class="table table-bordered">
      <thead>
        <tr><th>Title</th><th>Company</th><th>Approved</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="d in drives" :key="d.id">
          <td>{{ d.title }}</td>
          <td>{{ d.company_name }}</td>
          <td>
            <span :class="d.approved ? 'badge bg-success' : 'badge bg-secondary'">
              {{ d.approved ? 'Yes' : 'No' }}
            </span>
          </td>
          <td>
            <button class="btn btn-sm btn-outline-primary" @click="router.push('/admin/drive/' + d.id)">
              View Details
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- students -->
    <h5 class="mt-4">Students</h5>
    <table class="table table-bordered">
      <thead>
        <tr><th>Name</th><th>Email</th><th>Department</th><th>Status</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="s in students" :key="s.id">
          <td>{{ s.full_name }}</td>
          <td>{{ s.email }}</td>
          <td>{{ s.department || '-' }}</td>
          <td>
            <span :class="s.is_active ? 'badge bg-success' : 'badge bg-secondary'">
              {{ s.is_active ? 'Active' : 'Deactivated' }}
            </span>
          </td>
          <td>
            <button v-if="s.is_active" class="btn btn-sm btn-outline-danger" @click="deactivateStudent(s.id)">Deactivate</button>
            <button v-else class="btn btn-sm btn-outline-success" @click="activateStudent(s.id)">Activate</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
