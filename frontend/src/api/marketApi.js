import axios from 'axios'

// -- Swap backend URL here if needed ------------------------------------------
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: BASE_URL, timeout: 60000 })

export const estimateMarket = async ({ ingredients }) => {
  const { data } = await api.post('/api/market/estimate', { ingredients })
  return data
}

export default api
