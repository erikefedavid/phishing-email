import axios from 'axios'

let baseUrl = import.meta.env.VITE_API_URL || '/api';

// If VITE_API_URL is provided, ensure it ends with /api
if (import.meta.env.VITE_API_URL) {
  const trimmedUrl = import.meta.env.VITE_API_URL.replace(/\/+$/, ''); // Remove trailing slashes
  baseUrl = trimmedUrl.endsWith('/api') ? trimmedUrl : `${trimmedUrl}/api`;
}

const api = axios.create({
  baseURL: baseUrl,
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
