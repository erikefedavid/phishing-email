import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export async function detectEmail(subject, body, headers) {
  const { data } = await api.post('/detect', { subject, body, headers })
  return data
}

export async function healthCheck() {
  const { data } = await api.get('/health')
  return data
}
