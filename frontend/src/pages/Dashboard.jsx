import { useState, useEffect } from 'react'
import { healthCheck } from '../services/api.js'

export default function Dashboard() {
  const [history, setHistory] = useState([])
  const [health, setHealth] = useState(null)

  useEffect(() => {
    healthCheck().then(setHealth).catch(() => setHealth({ status: 'unreachable' }))
    const stored = localStorage.getItem('phishguard_history')
    if (stored) setHistory(JSON.parse(stored))
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Dashboard</h1>

      {health && (
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-2">API Status</h2>
          <div className="flex gap-4 text-sm">
            <span className={health.status === 'ok' ? 'text-green-400' : 'text-red-400'}>
              {health.status === 'ok' ? 'Online' : 'Offline'}
            </span>
            {health.version && <span className="text-slate-400">v{health.version}</span>}
            {health.uptime && <span className="text-slate-400">{health.uptime}</span>}
          </div>
        </div>
      )}

      <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
        <h2 className="text-lg font-semibold text-white mb-4">Detection History</h2>
        {history.length === 0 ? (
          <p className="text-slate-400">No detections yet. Analyze an email to see history here.</p>
        ) : (
          <div className="space-y-2">
            {history.map((item, i) => (
              <div key={i} className="flex items-center justify-between bg-slate-900 rounded-lg px-4 py-3 text-sm">
                <span className="text-slate-300 truncate max-w-md">{item.subject || '(no subject)'}</span>
                <span className={`font-semibold ${item.is_phishing ? 'text-red-400' : 'text-green-400'}`}>
                  {item.label}
                </span>
                <span className="text-slate-500">{new Date(item.timestamp).toLocaleString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
