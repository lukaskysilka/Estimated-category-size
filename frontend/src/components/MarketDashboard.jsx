import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import RegionCard from './RegionCard'
import CompetitorTable from './CompetitorTable'
import { Globe } from 'lucide-react'

const fmt = (n) => new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(n)
const COLORS = ['#F97316', '#FB923C', '#FCD34D']

export default function MarketDashboard({ data }) {
  if (!data) return null

  const chartData = Object.entries(data.regions).map(([key, r]) => ({
    name: key,
    usd: r.total_usd,
  }))

  return (
    <div className="space-y-6 mt-8">
      {/* Total KPI */}
      <div className="text-center py-8 bg-gradient-to-r from-orange-500/10 via-slate-800/60 to-orange-500/10
                      border border-orange-500/20 rounded-2xl">
        <p className="text-slate-400 text-sm uppercase tracking-widest mb-2">Celková velikost trhu</p>
        <p className="font-display font-bold text-5xl gradient-text">
          ${fmt(data.total_market_usd)}
        </p>
        <p className="text-slate-500 text-sm mt-2">CZ + EU + USA dohromady</p>
        <p className="text-slate-600 text-xs mt-1">{data.methodology.note}</p>
      </div>

      {/* Region Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(data.regions).map(([key, region]) => (
          <RegionCard key={key} regionKey={key} data={region} />
        ))}
      </div>

      {/* Chart */}
      <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Globe size={18} className="text-orange-400" />
          <h3 className="font-display font-bold text-white">Tržby podle regionu (USD)</h3>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={chartData} barCategoryGap="30%">
            <XAxis dataKey="name" stroke="#64748B" tick={{ fill: '#94A3B8', fontFamily: 'DM Sans' }} />
            <YAxis stroke="#64748B" tick={{ fill: '#94A3B8', fontSize: 12 }}
                   tickFormatter={v => `$${(v / 1_000_000).toFixed(1)}M`} />
            <Tooltip
              formatter={(v) => [`$${fmt(v)}`, 'Odhad trhu']}
              contentStyle={{ background: '#1E293B', border: '1px solid #334155', borderRadius: '12px', color: '#F1F5F9' }}
            />
            <Bar dataKey="usd" radius={[6, 6, 0, 0]}>
              {chartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Competitor Table */}
      <CompetitorTable competitors={data.top_global_competitors} />
    </div>
  )
}
