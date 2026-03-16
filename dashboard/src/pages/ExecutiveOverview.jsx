import React from 'react';
import { 
  Shield, 
  ArrowUpRight, 
  ArrowDownRight, 
  Zap, 
  Clock, 
  AlertCircle 
} from 'lucide-react';

const KPICard = ({ label, value, delta, sublabel, trend }) => (
  <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-6 shadow-2xl shadow-black/20">
    <div className="flex justify-between items-start mb-4">
      <span className="text-sm font-medium text-slate-400">{label}</span>
      <div className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded-full ${
        trend === 'up' ? 'text-emerald-400 bg-emerald-400/10' : 'text-rose-400 bg-rose-400/10'
      }`}>
        {trend === 'up' ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
        {delta}
      </div>
    </div>
    <div className="text-4xl font-bold tracking-tight text-white mb-2">{value}</div>
    <span className="text-xs text-slate-500 font-medium uppercase tracking-wider">{sublabel}</span>
  </div>
);

const ExecutiveOverview = () => {
  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Executive Overview</h1>
        <p className="text-slate-400 mt-2">Operational performance and governance health for the agentic platform.</p>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <KPICard 
          label="Automation Rate" 
          value="64.2%" 
          delta="+4.8%" 
          sublabel="Target: 70%" 
          trend="up" 
        />
        <KPICard 
          label="Review Rate" 
          value="21.7%" 
          delta="-2.1%" 
          sublabel="Human Intervention" 
          trend="down" 
        />
        <KPICard 
          label="Risk Captured" 
          value="184" 
          delta="+12" 
          sublabel="Policy Prevented" 
          trend="up" 
        />
        <KPICard 
          label="Avg Latency" 
          value="1.4s" 
          delta="-0.3s" 
          sublabel="Backend Spine" 
          trend="down" 
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Main Chart Section */}
        <div className="xl:col-span-2 rounded-3xl border border-white/10 bg-[#121a2f] p-8">
          <div className="flex justify-between items-center mb-10">
            <div>
              <h2 className="text-xl font-bold text-white">Platform Throughput</h2>
              <p className="text-sm text-slate-500 mt-1">Live execution trends over last 24 hours.</p>
            </div>
            <div className="flex gap-2">
               <div className="flex items-center gap-2 text-xs text-slate-400 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10">
                  <div className="w-2 h-2 rounded-full bg-sky-500" />
                  Automated
               </div>
               <div className="flex items-center gap-2 text-xs text-slate-400 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10">
                  <div className="w-2 h-2 rounded-full bg-violet-500" />
                  Escalated
               </div>
            </div>
          </div>

          <div className="h-64 flex items-end gap-3 px-2">
            {[32, 45, 67, 52, 88, 72, 59, 91, 76, 85, 93, 70, 62, 78, 85, 92].map((val, i) => (
              <div key={i} className="flex-1 group relative">
                <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-white text-[#0b1020] px-2 py-1 rounded text-[10px] font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                  {val}%
                </div>
                <div 
                  className="w-full bg-sky-500/20 rounded-t-xl group-hover:bg-sky-500/40 transition-colors" 
                  style={{ height: `${val}%` }} 
                />
                <div 
                  className="absolute bottom-0 w-full bg-sky-500 rounded-t-xl" 
                  style={{ height: `${val * 0.7}%` }} 
                />
              </div>
            ))}
          </div>
        </div>

        {/* Distribution Section */}
        <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8">
          <h2 className="text-xl font-bold text-white mb-6">Strategy Distribution</h2>
          <div className="space-y-6">
            {[
              { label: 'Automate', value: 64, color: 'bg-emerald-500' },
              { label: 'Investigate', value: 22, color: 'bg-sky-500' },
              { label: 'Escalate', value: 10, color: 'bg-amber-500' },
              { label: 'Block', value: 4, color: 'bg-rose-500' },
            ].map((item) => (
              <div key={item.label}>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-400 font-medium">{item.label}</span>
                  <span className="text-white font-bold">{item.value}%</span>
                </div>
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className={`h-full ${item.color}`} style={{ width: `${item.value}%` }} />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-10 p-4 rounded-2xl bg-white/5 border border-white/10 text-center">
            <p className="text-xs text-slate-500 uppercase font-bold tracking-widest mb-1">Health Score</p>
            <p className="text-3xl font-black text-white">98.4</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExecutiveOverview;
