import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Navbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 bg-violet-500 rounded-full"></div>
        <h1 className="text-white font-bold text-lg">Founder Memory AI</h1>
      </div>
      <button onClick={handleLogout}
        className="text-gray-400 hover:text-white text-sm transition-colors">
        Logout
      </button>
    </div>
  )
}