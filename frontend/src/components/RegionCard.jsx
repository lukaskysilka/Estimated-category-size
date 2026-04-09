import { Users, ShoppingCart } from 'lucide-react'

const REGION_FLAGS = { CZ: '🇨🇿', EU: '🇪🇺', USA: '🇺🇸' }

const fmt = (n) => new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(n)

export default function RegionCard({ regionKey, data }) {
  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 card-glow transition-all">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{REGION_FLAGS[regionKey]}</span>
          <span className="font-display font-bold text-white text-lg">{regionKey}</span>
        </div>
        <span className="text-xs text-orange-400 bg-orange-500/10 px-2 py-1 rounded-full border border-orange-500/20">
          {data.product_count} produktů
        </span>
      </div>

      <div className="mb-4">
        <p className="text-slate-400 text-sm mb-1">Odhad objemu trhu</p>
        <p className="font-display font-bold text-3xl gradient-text">
          {data.currency_symbol}{fmt(data.total_local)}
        </p>
        <p className="text-slate-500 text-xs mt-1">≈ ${fmt(data.total_usd)} USD</p>
      </div>

      <div className="grid grid-cols-2 gap-3 pt-4 border-t border-slate-700">
        <div className="flex items-center gap-2">
          <ShoppingCart size={14} className="text-orange-400" />
          <div>
            <p className="text-slate-400 text-xs">Průměrná cena</p>
            <p className="text-white text-sm font-medium">
              {data.currency_symbol}{fmt(data.avg_price)}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Users size={14} className="text-orange-400" />
          <div>
            <p className="text-slate-400 text-xs">Celkem recenzí</p>
            <p className="text-white text-sm font-medium">{fmt(data.total_reviews)}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
