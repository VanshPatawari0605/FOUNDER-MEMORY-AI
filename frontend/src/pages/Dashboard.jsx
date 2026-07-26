import { useState } from 'react'
import Navbar from '../components/Navbar'
import Chat from '../components/Chat'
import Upload from '../components/Upload'
import Entities from '../components/Entities'

const TABS = ['Chat', 'Upload', 'Entities']

export default function Dashboard() {
  const [tab, setTab] = useState('Chat')

  return (
    <div className="min-h-screen bg-gray-950">
      <Navbar />
      <div className="max-w-5xl mx-auto p-4">
        <div className="flex gap-2 mb-6">
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                tab === t ? 'bg-violet-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
              }`}>
              {t}
            </button>
          ))}
        </div>
        {tab === 'Chat' && <Chat />}
        {tab === 'Upload' && <Upload />}
        {tab === 'Entities' && <Entities />}
      </div>
    </div>
  )
}