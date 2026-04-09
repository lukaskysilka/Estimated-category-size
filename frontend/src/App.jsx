import { useState } from 'react'
import SearchForm from './components/SearchForm'
import MarketDashboard from './components/MarketDashboard'
import { estimateMarket } from './api/marketApi'
import { Zap, AlertCircle } from 'lucide-react'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await estimateMarket(formData)
      setResult(data)
    } catch (err) {
      setError(err?.response?.data?.detail || 'API call failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-movit-dark">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
              <Zap size={16} className="text-white" fill="white" />
            </div>
            <span className="font-display font-bold text-white text-lg tracking-tight">
              Movit <span className="gradient-text">Energy</span>
            </span>
          </div>
          <span className="text-slate-500 text-xs bg-slate-800 px-3 py-1 rounded-full border border-slate-700">
            Odhad velikosti trhu
          </span>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-6xl mx-auto px-6 py-10">
        <div className="mb-10 text-center">
          <h1 className="font-display font-extrabold text-4xl text-white mb-3">
            Jak velký je váš <span className="gradient-text">trh?</span>
          </h1>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            Zadejte složení produktu — vyhledáme konkurenci na trzích CZ, EU a USA
            a odhadneme velikost trhu podle počtu recenzí a cen.
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          <SearchForm onSubmit={handleSubmit} loading={loading} />
        </div>

        {error && (
          <div className="mt-6 max-w-2xl mx-auto flex items-start gap-3 bg-red-500/10 border border-red-500/30
                          text-red-400 rounded-xl p-4 text-sm">
            <AlertCircle size={18} className="shrink-0 mt-0.5" />
            <span>{error === 'API call failed. Is the backend running?' ? 'Připojení k backendu selhalo. Běží Python server?' : error}</span>
          </div>
        )}

        {result && <MarketDashboard data={result} />}
      </main>
    </div>
  )
}
