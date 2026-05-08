// frontend/src/api/client.js
import axios from 'axios'

// In development this hits your local FastAPI server.
// In production (Vercel) this will be your Render URL via env variable.
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
})

export async function askQuestion(question) {
  const response = await api.post('/api/v1/query/ask', { question })
  return response.data
}

export async function getSampleQuestions() {
  const response = await api.get('/api/v1/query/samples')
  return response.data.questions
}

export async function checkHealth() {
  try {
    const response = await api.get('/health')
    return response.data.status === 'ok'
  } catch {
    return false
  }
}