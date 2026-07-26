import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async () => {
    try {
      const res = await api.post('/auth/login', form)
      login(res.data.access_token)
      navigate('/dashboard')
    } catch (e) {
      setError(e.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold text-white">Welcome back</h1>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <input name="email" placeholder="Email" onChange={handle}
          className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none" />
        <input name="password" type="password" placeholder="Password" onChange={handle}
          className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none" />
        <button onClick={submit}
          className="w-full bg-violet-600 hover:bg-violet-700 text-white py-3 rounded-lg font-semibold">
          Login
        </button>
        <p className="text-gray-400 text-sm text-center">
          No account? <Link to="/register" className="text-violet-400">Register</Link>
        </p>
      </div>
    </div>
  )
}