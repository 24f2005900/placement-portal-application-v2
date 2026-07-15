import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    role: localStorage.getItem('role') || '',
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      const res = await api.post('/auth/login', { username, password })
      this.token = res.data.token
      this.role = res.data.role
      localStorage.setItem('token', this.token)
      localStorage.setItem('role', this.role)
      return this.role
    },

    logout() {
      this.token = ''
      this.role = ''
      localStorage.removeItem('token')
      localStorage.removeItem('role')
    },
  },
})
