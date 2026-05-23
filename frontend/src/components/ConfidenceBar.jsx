export default function ConfidenceBar({ confidence, isPhishing }) {
  const riskPct = isPhishing ? Math.round(confidence * 100) : Math.round((1 - confidence) * 100)

  let color
  if (riskPct >= 70) color = 'bg-red-500'
  else if (riskPct >= 40) color = 'bg-amber-500'
  else color = 'bg-green-500'

  let label
  if (riskPct >= 70) label = 'PHISHING'
  else if (riskPct >= 40) label = 'SUSPICIOUS'
  else label = 'SAFE'

  const labelColor =
    riskPct >= 70 ? 'text-red-400' : riskPct >= 40 ? 'text-amber-400' : 'text-green-400'

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="text-slate-400">Risk Level</span>
        <span className={`font-bold ${labelColor}`}>{label}</span>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-4 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${riskPct}%` }}
        />
      </div>
      <div className="flex justify-between text-xs text-slate-500">
        <span>Safe (0%)</span>
        <span>{riskPct}% phishing risk</span>
        <span>Phishing (100%)</span>
      </div>
    </div>
  )
}
