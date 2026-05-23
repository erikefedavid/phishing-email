import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Dashboard from './pages/Dashboard.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen">
        <nav className="border-b border-slate-700 px-6 py-4">
          <div className="max-w-5xl mx-auto flex items-center justify-between">
            <a href="/" className="text-xl font-bold text-cyan-400">PhishGuard AI</a>
            <div className="space-x-4">
              <a href="/" className="text-slate-300 hover:text-white transition">Detect</a>
              <a href="/dashboard" className="text-slate-300 hover:text-white transition">History</a>
            </div>
          </div>
        </nav>
        <main className="max-w-5xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
