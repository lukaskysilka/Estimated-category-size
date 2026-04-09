import { useState } from 'react'
import { Search, Zap } from 'lucide-react'

export default function SearchForm({ onSubmit, loading }) {
  const [ingredients, setIngredients] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (ingredients.trim()) {
      onSubmit({ ingredients: ingredients.trim() })
    }
  }

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-8 backdrop-blur-sm">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-orange-500/20 rounded-lg">
          <Zap className="text-orange-400" size={22} />
        </div>
        <h2 className="font-display text-xl font-bold text-white">Analyzovat trh</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-400 mb-2">
            Složení produktu
          </label>
          <textarea
            rows={4}
            value={ingredients}
            onChange={e => setIngredients(e.target.value)}
            placeholder="např. černý česnek, allicin, vitamin C&#10;např. kofein, taurin, B6, B12, L-karnitin"
            className="w-full bg-slate-900/80 border border-slate-600 rounded-xl px-4 py-3
                       text-white placeholder-slate-500 focus:outline-none focus:border-orange-500
                       transition-colors resize-none"
          />
          <p className="text-slate-500 text-xs mt-1.5">
            Zadejte ingredience oddělené čárkou.
          </p>
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading || !ingredients}
          className="w-full flex items-center justify-center gap-2 bg-orange-500 hover:bg-orange-400
                     disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold
                     py-3.5 rounded-xl transition-all duration-200 font-display tracking-wide"
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Analyzing markets...
            </>
          ) : (
            <>
              <Search size={18} />
              Odhadnout velikost trhu
            </>
          )}
        </button>
      </div>
    </div>
  )
}
