import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function Onboard() {
  const navigate = useNavigate()
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hi! I'm your AI memory assistant. Let's set up your company. What's your business about?" }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'user', content: input }
    const updatedMessages = [...messages, userMsg]
    setMessages(updatedMessages)
    setInput('')
    setLoading(true)

    try {
      const res = await api.post('/onboard/chat', {
        message: input,
        history: messages
      })
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.reply }])
      if (res.data.done) {
        setTimeout(() => navigate('/dashboard'), 2000)
      }
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Something went wrong.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-gray-900 rounded-2xl flex flex-col h-[600px]">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-white font-bold text-lg">Company Onboarding</h1>
          <p className="text-gray-400 text-sm">Tell us about your business</p>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-xl text-sm ${
                m.role === 'user' ? 'bg-violet-600 text-white' : 'bg-gray-800 text-gray-200'
              }`}>
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 text-gray-400 px-4 py-2 rounded-xl text-sm">Thinking...</div>
            </div>
          )}
        </div>
        <div className="p-4 border-t border-gray-800 flex gap-2">
          <input value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send()}
            placeholder="Type your answer..."
            className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg outline-none text-sm" />
          <button onClick={send}
            className="bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg text-sm font-semibold">
            Send
          </button>
        </div>
      </div>
    </div>
  )
}