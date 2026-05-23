import { useState } from 'react'
import { detectEmail } from '../services/api.js'

export default function EmailInput({ onResult }) {
  const [subject, setSubject] = useState('')
  const [body, setBody] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!body.trim()) return
    setLoading(true)
    try {
      const data = await detectEmail(subject, body, null)
      onResult(data)
    } catch {
      // handled by parent
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input
        type="text"
        placeholder="Subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        className="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-white"
      />
      <textarea
        placeholder="Paste email body..."
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows={6}
        className="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-white font-mono text-sm"
        required
      />
      <button
        type="submit"
        disabled={loading}
        className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-slate-600 text-white font-semibold py-2 px-4 rounded transition"
      >
        {loading ? 'Analyzing...' : 'Detect Phishing'}
      </button>
    </form>
  )
}
