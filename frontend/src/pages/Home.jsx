import { useState, useRef } from 'react'
import { detectEmail } from '../services/api.js'
import ResultCard from '../components/ResultCard.jsx'

export default function Home() {
  const [subject, setSubject] = useState('')
  const [body, setBody] = useState('')
  const [headers, setHeaders] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [fileName, setFileName] = useState('')
  const fileInputRef = useRef(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!body.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await detectEmail(subject, body, headers || null)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Detection failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  async function handleFileUpload(e) {
    const file = e.target.files[0]
    if (!file) return
    setFileName(file.name)
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const text = await file.text()
      const lines = text.split('\n')
      let parsedHeaders = ''
      let parsedBody = ''
      let parsedSubject = ''
      let inHeaders = true
      for (const line of lines) {
        if (inHeaders) {
          if (line.trim() === '') {
            inHeaders = false
            continue
          }
          if (line.toLowerCase().startsWith('subject:')) {
            parsedSubject = line.slice(8).trim()
          }
          parsedHeaders += line + '\n'
        } else {
          parsedBody += line + '\n'
        }
      }

      setSubject(parsedSubject)
      setBody(parsedBody.trim())
      setHeaders(parsedHeaders.trim())

      const data = await detectEmail(parsedSubject, parsedBody.trim(), parsedHeaders.trim() || null)
      setResult(data)
    } catch (err) {
      setError('Failed to read file. Make sure it is a .txt or .eml file.')
    } finally {
      setLoading(false)
    }
  }

  const samples = {
    phishing: {
      subject: "URGENT: Your Account Has Been Compromised",
      headers: "From: security@paypa1-secure.com\nReply-To: verify@paypa1-secure.com",
      body: "Dear valued customer,\n\nWe have detected unusual activity on your account. Your account has been temporarily suspended.\n\nTo restore access, you must verify your identity immediately:\nhttp://paypa1-secure.com/verify-now\n\nFailure to verify within 24 hours will result in permanent account closure.\n\nThis is an automated message. Do not reply to this email.\n\nSincerely,\nPayPal Security Team",
    },
    legitimate: {
      subject: "Weekly Team Meeting Notes — May 23",
      headers: "From: john.smith@company.com\nTo: team@company.com",
      body: "Hi team,\n\nHere are the notes from today's sprint planning:\n\n1. Frontend: Complete user dashboard by Friday\n2. Backend: Deploy API v2.1 to staging\n3. QA: Run regression tests before release\n\nPlease review your action items and let me know if anything is missing.\n\nBest,\nJohn",
    },
  }

  function loadSample(type) {
    setSubject(samples[type].subject)
    setBody(samples[type].body)
    setHeaders(samples[type].headers)
    setResult(null)
    setError('')
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-white">Phishing Email Detector</h1>
        <p className="text-slate-400 mt-2">Paste email content or upload a .eml/.txt file for instant AI analysis</p>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="border-2 border-dashed border-slate-600 rounded-lg p-6 text-center space-y-3">
          <input
            ref={fileInputRef}
            type="file"
            accept=".eml,.txt"
            onChange={handleFileUpload}
            className="hidden"
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
            className="bg-slate-700 hover:bg-slate-600 text-slate-300 font-semibold py-2 px-6 rounded-lg transition disabled:opacity-50"
          >
            {fileName ? `File: ${fileName}` : 'Upload .eml or .txt file'}
          </button>
        </div>
      </div>

      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => loadSample('phishing')}
          className="flex-1 bg-red-900/40 hover:bg-red-900/60 border border-red-700 text-red-300 font-semibold py-2 px-4 rounded-lg transition text-sm"
        >
          Try Phishing Sample
        </button>
        <button
          type="button"
          onClick={() => loadSample('legitimate')}
          className="flex-1 bg-green-900/40 hover:bg-green-900/60 border border-green-700 text-green-300 font-semibold py-2 px-4 rounded-lg transition text-sm"
        >
          Try Legitimate Sample
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Subject</label>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-400"
            placeholder="Email subject line..."
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Email Body</label>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={8}
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-400 font-mono text-sm"
            placeholder="Paste the full email body here..."
            required
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Headers (optional)</label>
          <textarea
            value={headers}
            onChange={(e) => setHeaders(e.target.value)}
            rows={3}
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-400 font-mono text-sm"
            placeholder="From: support@example.com&#10;Reply-To: ..."
          />
        </div>
        <button
          type="submit"
          disabled={loading || !body.trim()}
          className="w-full bg-cyan-500 hover:bg-cyan-400 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition"
        >
          {loading ? 'Analyzing...' : 'Analyze Email'}
        </button>
      </form>

      {error && (
        <div className="bg-red-900/50 border border-red-500 rounded-lg p-4 text-red-200">
          {error}
        </div>
      )}

      {result && <ResultCard result={result} />}
    </div>
  )
}
