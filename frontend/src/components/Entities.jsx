import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function Entities() {
  const [tab, setTab] = useState('people')
  const [people, setPeople] = useState([])
  const [promises, setPromises] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchData()
  }, [tab])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (tab === 'people') {
        const res = await api.get('/entities/people')
        setPeople(res.data)
      } else {
        const res = await api.get('/entities/promises')
        setPromises(res.data)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-900 rounded-2xl p-4">
      <div className="flex gap-2 mb-4">
        <button onClick={() => setTab('people')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold ${
            tab === 'people' ? 'bg-violet-600 text-white' : 'bg-gray-800 text-gray-400'
          }`}>
          People
        </button>
        <button onClick={() => setTab('promises')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold ${
            tab === 'promises' ? 'bg-violet-600 text-white' : 'bg-gray-800 text-gray-400'
          }`}>
          Promises
        </button>
      </div>

      {loading && <p className="text-gray-400 text-sm text-center py-8">Loading...</p>}

      {!loading && tab === 'people' && (
        <div className="space-y-2">
          {people.length === 0 && (
            <p className="text-gray-600 text-sm text-center py-8">
              No people extracted yet. Upload some documents first.
            </p>
          )}
          {people.map((p, i) => (
            <div key={i} className="bg-gray-800 rounded-xl p-3 flex items-start gap-3">
              <div className="w-8 h-8 bg-violet-700 rounded-full flex items-center justify-center text-white text-sm font-bold shrink-0">
                {p.name[0]}
              </div>
              <div>
                <p className="text-white text-sm font-semibold">{p.name}</p>
                {p.description && <p className="text-gray-400 text-xs mt-1">{p.description}</p>}
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && tab === 'promises' && (
        <div className="space-y-2">
          {promises.length === 0 && (
            <p className="text-gray-600 text-sm text-center py-8">
              No promises extracted yet. Upload meeting notes or transcripts.
            </p>
          )}
          {promises.map((p, i) => (
            <div key={i} className="bg-gray-800 rounded-xl p-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-violet-400 text-sm font-semibold">{p.person}</span>
                {p.date_mentioned && (
                  <span className="text-gray-500 text-xs">
                    {new Date(p.date_mentioned).toLocaleDateString()}
                  </span>
                )}
              </div>
              <p className="text-gray-300 text-sm">{p.commitment}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}