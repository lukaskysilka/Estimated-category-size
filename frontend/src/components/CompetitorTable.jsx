import { ExternalLink, Star } from 'lucide-react'

const fmt = (n) => new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(n)
const FLAGS = { CZ: '🇨🇿', EU: '🇪🇺', USA: '🇺🇸' }

export default function CompetitorTable({ competitors }) {
  if (!competitors?.length) return null

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-2xl overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-700">
        <h3 className="font-display font-bold text-white text-lg">Největší konkurenti</h3>
        <p className="text-slate-400 text-sm mt-0.5">Seřazeno podle odhadovaných tržeb</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-400 text-xs uppercase tracking-wider bg-slate-900/40">
              <th className="px-6 py-3 text-left">#</th>
              <th className="px-6 py-3 text-left">Produkt</th>
              <th className="px-6 py-3 text-center">Region</th>
              <th className="px-6 py-3 text-right">Cena</th>
              <th className="px-6 py-3 text-right">Recenze</th>
              <th className="px-6 py-3 text-right">Odhad prodejů</th>
              <th className="px-6 py-3 text-right">Odhad tržeb (USD)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {competitors.map((c, i) => (
              <tr key={i} className="hover:bg-slate-700/30 transition-colors">
                <td className="px-6 py-4 text-slate-500 font-mono">{i + 1}</td>
                <td className="px-6 py-4 max-w-xs">
                  <a
                    href={c.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white hover:text-orange-400 transition-colors flex items-start gap-1.5 group"
                  >
                    <span className="line-clamp-2">{c.name}</span>
                    <ExternalLink size={12} className="shrink-0 mt-1 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </a>
                  {c.rating && (
                    <span className="flex items-center gap-1 text-yellow-400 text-xs mt-1">
                      <Star size={10} fill="currentColor" />
                      {c.rating}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 text-center">
                  <span className="text-base">{FLAGS[c.region]}</span>
                </td>
                <td className="px-6 py-4 text-right text-slate-300">
                          {c.currency === 'CZK' ? `${fmt(c.price)} Kč` :
                   c.currency === 'EUR' ? `€${c.price.toFixed(2)}` :
                   `$${c.price.toFixed(2)}`}
                </td>
                <td className="px-6 py-4 text-right text-slate-300">
                  {fmt(c.reviews)}
                </td>
                <td className="px-6 py-4 text-right text-slate-300">{fmt(c.estimated_sales)}</td>
                <td className="px-6 py-4 text-right font-semibold text-orange-400">
                  ${fmt(c.revenue_usd)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="px-6 py-3 bg-slate-900/30 border-t border-slate-700">
        <p className="text-slate-500 text-xs">
          ⚠️ Pouze produkty s reálně nalezenou cenou a počtem recenzí. Výpočet: recenze × 50 × cena.
        </p>
      </div>
    </div>
  )
}
