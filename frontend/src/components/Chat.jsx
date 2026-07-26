import { useState } from 'react'
import api from '../api/axios'

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim()) return
    const question = input
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await api.post('/agent/query', { question })
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.answer,
        sources: res.data.sources
      }])
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Something went wrong.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-900 rounded-2xl flex flex-col h-[600px]">
      <div className="p-4 border-b border-gray-800">
        <h2 className="text-white font-semibold">Ask your memory</h2>
        <p className="text-gray-400 text-xs">Query anything from your documents, meetings, decisions</p>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 && (
          <div className="text-gray-600 text-sm text-center mt-20">
            Ask something like "What did we decide about pricing?" or "Who was in the April meeting?"
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xl px-4 py-3 rounded-xl text-sm ${
              m.role === 'user' ? 'bg-violet-600 text-white' : 'bg-gray-800 text-gray-200'
            }`}>
              <p>{m.content}</p>
              {m.sources?.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-700">
                  <p className="text-xs text-gray-400">Sources:</p>
                  {m.sources.map((s, j) => (
                    <span key={j} className="text-xs text-violet-400 mr-2">{s}</span>
                  ))}
                </div>
              )}
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
          placeholder="Ask anything about your company..."
          className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg outline-none text-sm" />
        <button onClick={send}
          className="bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg text-sm font-semibold">
          Ask
        </button>
      </div>
    </div>
  )
}