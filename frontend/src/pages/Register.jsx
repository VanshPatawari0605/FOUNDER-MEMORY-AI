import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function Register() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ company_name: '', name: '', email: '', password: '' })
  const [error, setError] = useState('')

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async () => {
    try {
      const res = await api.post('/auth/register', form)
      const token = res.data.access_token
      localStorage.setItem('token', token)
      login(token)
      navigate('/onboard')
    } catch (e) {
      setError(e.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold text-white">Create your company</h1>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <input name="company_name" placeholder="Company Name" onChange={handle}
          className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none" />
        <input name="name" placeholder="Your Name" onChange={handle}
          className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none" />
        <input name="email" placeholder="Email" onChange={handle}
          className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none" />
        <input name="password" type="password" placeholder="Password" onChange={handle}
          className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none" />
        <button onClick={submit}
          className="w-full bg-violet-600 hover:bg-violet-700 text-white py-3 rounded-lg font-semibold">
          Register
        </button>
        <p className="text-gray-400 text-sm text-center">
          Already have an account? <Link to="/login" className="text-violet-400">Login</Link>
        </p>
      </div>
    </div>
  )
}