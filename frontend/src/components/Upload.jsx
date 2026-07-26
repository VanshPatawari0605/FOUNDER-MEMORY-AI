import { useState } from 'react'
import api from '../api/axios'

export default function Upload() {
  const [files, setFiles] = useState([])
  const [uploads, setUploads] = useState([])
  const [loading, setLoading] = useState(false)

  const handleDrop = (e) => {
    e.preventDefault()
    setFiles([...e.dataTransfer.files])
  }

  const handleSelect = (e) => {
    setFiles([...e.target.files])
  }

  const upload = async () => {
    if (!files.length) return
    setLoading(true)
    const results = []

    for (const file of files) {
      try {
        const form = new FormData()
        form.append('file', file)
        const res = await api.post('/ingest/upload', form)
        results.push({ name: file.name, status: 'processing', id: res.data.document_id })
      } catch (e) {
        results.push({ name: file.name, status: 'failed' })
      }
    }

    setUploads(prev => [...prev, ...results])
    setFiles([])
    setLoading(false)
  }

  return (
    <div className="space-y-4">
      <div
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        className="bg-gray-900 border-2 border-dashed border-gray-700 rounded-2xl p-12 text-center hover:border-violet-500 transition-colors cursor-pointer"
      >
        <p className="text-gray-400 text-sm mb-2">Drag and drop files here</p>
        <p className="text-gray-600 text-xs mb-4">PDF, DOCX, Excel, TXT supported</p>
        <label className="bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg text-sm font-semibold cursor-pointer">
          Browse Files
          <input type="file" multiple onChange={handleSelect} className="hidden"
            accept=".pdf,.docx,.xlsx,.txt" />
        </label>
      </div>

      {files.length > 0 && (
        <div className="bg-gray-900 rounded-2xl p-4 space-y-2">
          <p className="text-gray-400 text-sm font-semibold">Ready to upload:</p>
          {[...files].map((f, i) => (
            <div key={i} className="flex items-center justify-between">
              <span className="text-white text-sm">{f.name}</span>
              <span className="text-gray-500 text-xs">{(f.size / 1024).toFixed(1)} KB</span>
            </div>
          ))}
          <button onClick={upload} disabled={loading}
            className="w-full bg-violet-600 hover:bg-violet-700 text-white py-2 rounded-lg text-sm font-semibold mt-2">
            {loading ? 'Uploading...' : 'Upload All'}
          </button>
        </div>
      )}

      {uploads.length > 0 && (
        <div className="bg-gray-900 rounded-2xl p-4 space-y-2">
          <p className="text-gray-400 text-sm font-semibold">Uploaded:</p>
          {uploads.map((u, i) => (
            <div key={i} className="flex items-center justify-between">
              <span className="text-white text-sm">{u.name}</span>
              <span className={`text-xs px-2 py-1 rounded-full ${
                u.status === 'processing' ? 'bg-yellow-900 text-yellow-400' : 'bg-red-900 text-red-400'
              }`}>
                {u.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}