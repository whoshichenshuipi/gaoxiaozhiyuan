import axios from 'axios'

const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
    timeout: 10000
})

// Request interceptor
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// Response interceptor
request.interceptors.response.use(
    response => {
        const res = response.data
        // Handle error codes from backend
        if (res.code && res.code !== 200) {
            // Toast/Alert handling would go here
            return Promise.reject(new Error(res.msg || 'Error'))
        }
        return res
    },
    error => {
        console.error('API Error:', error)
        if (error.response && error.response.status === 401) {
            // Token expired or invalid
            localStorage.clear()
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default request
