import ConfidenceBar from './ConfidenceBar.jsx'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { useEffect } from 'react'

export default function ResultCard({ result }) {
  useEffect(() => {
    const history = JSON.parse(localStorage.getItem('phishguard_history') || '[]')
    history.unshift({ ...result, timestamp: new Date().toISOString() })
    localStorage.setItem('phishguard_history', JSON.stringify(history.slice(0, 50)))
  }, [result])

  const chartData = result.top_features.map((f) => ({
    name: f.feature,
    weight: f.weight,
  }))

  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Detection Result</h2>
        <span className="text-sm text-slate-400">{result.processing_ms}ms</span>
      </div>

      <ConfidenceBar confidence={result.confidence} isPhishing={result.is_phishing} />

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="bg-slate-900 rounded-lg p-3">
          <span className="text-slate-400">Label</span>
          <p className={`text-lg font-bold ${result.is_phishing ? 'text-red-400' : 'text-green-400'}`}>
            {result.label.toUpperCase()}
          </p>
        </div>
        <div className="bg-slate-900 rounded-lg p-3">
          <span className="text-slate-400">Phishing Risk</span>
          <p className="text-lg font-bold text-white">
            {result.is_phishing
              ? `${(result.confidence * 100).toFixed(0)}%`
              : `${((1 - result.confidence) * 100).toFixed(0)}%`}
          </p>
        </div>
      </div>

      {chartData.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-400 mb-2">Top Contributing Features</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData} layout="vertical" margin={{ left: 100 }}>
              <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis dataKey="name" type="category" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#e2e8f0' }}
              />
              <Bar dataKey="weight" fill="#06b6d4" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
