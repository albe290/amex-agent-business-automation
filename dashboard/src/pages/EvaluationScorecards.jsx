import React from 'react';
import { 
  Trophy, 
  Target, 
  Activity, 
  CheckCircle, 
  Search,
  Zap,
  Layout
} from 'lucide-react';

const ScoreCard = ({ title, score, icon: Icon, color, details }) => (
  <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8 relative overflow-hidden group">
    <div className={`absolute top-0 right-0 w-32 h-32 ${color} blur-[100px] opacity-10 group-hover:opacity-20 transition-opacity`} />
    <div className="flex items-center gap-4 mb-6">
      <div className={`p-3 rounded-2xl bg-white/5 ${color.replace('bg-', 'text-')}`}>
        <Icon size={24} />
      </div>
      <div>
        <h3 className="text-lg font-bold text-white uppercase tracking-tight">{title}</h3>
        <p className="text-xs text-slate-500 font-black tracking-widest uppercase">Platform Benchmark</p>
      </div>
    </div>
    <div className="text-5xl font-black text-white mb-6 uppercase tracking-tighter">{score}</div>
    <p className="text-sm text-slate-400 font-medium leading-relaxed">{details}</p>
  </div>
);

const MetricItem = ({ label, value, sublabel }) => (
  <div className="p-5 rounded-2xl bg-white/5 border border-white/10 flex justify-between items-center group hover:bg-white/[0.08] transition-all">
    <div>
      <p className="text-sm font-bold text-slate-100">{label}</p>
      <p className="text-xs text-slate-500 uppercase tracking-widest font-black mt-1">{sublabel}</p>
    </div>
    <span className="text-2xl font-black text-sky-400">{value}</span>
  </div>
);

const EvaluationScorecards = () => {
  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Evaluation & Scorecards</h1>
          <p className="text-slate-400 mt-2">Quantitative and qualitative platform performance benchmarks.</p>
        </div>
        <div className="rounded-2xl border border-sky-500/20 bg-sky-500/10 px-4 py-2 flex items-center gap-3">
          <Activity size={18} className="text-sky-400" />
          <span className="text-sm font-black text-sky-400 uppercase tracking-widest">v1.2.4-stable</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <ScoreCard 
          title="Governance" 
          score="STRONG" 
          icon={Shield} 
          color="bg-emerald-500"
          details="Policy precision and block accuracy are within the 99th percentile. No unauthorized escalations detected in the current run."
        />
        <ScoreCard 
          title="Routing" 
          score="STRONG" 
          icon={Target} 
          color="bg-sky-500"
          details="Strategy match rate meets enterprise benchmarks. 100% alignment with deterministic business logic for high-value cases."
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <div className="xl:col-span-2 rounded-3xl border border-white/10 bg-[#121a2f] p-8">
           <h2 className="text-xl font-bold text-white mb-8 flex items-center gap-3">
              <Zap className="text-amber-400" />
              Platform Efficiency Metrics
           </h2>
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <MetricItem label="Automation Precision" value="96.4%" sublabel="Agent accuracy" />
              <MetricItem label="Routing Success" value="100%" sublabel="Path alignment" />
              <MetricItem label="Context Yield" value="0.84" sublabel="Evidence score" />
              <MetricItem label="Policy Precision" value="94.2%" sublabel="Detection rate" />
              <MetricItem label="Review Alignment" value="89.1%" sublabel="Human vs Machine" />
              <MetricItem label="Override Frequency" value="7.1%" sublabel="Discrepancy rate" />
           </div>
        </div>

        <div className="flex flex-col gap-6">
           <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8 flex-1">
              <h2 className="text-lg font-bold text-white mb-6 uppercase tracking-tight">Diagnostic Insights</h2>
              <div className="space-y-4">
                 <div className="p-4 rounded-xl bg-sky-500/10 border border-sky-500/20">
                    <p className="text-xs font-black text-sky-400 uppercase tracking-[0.15em] mb-1">Stability</p>
                    <p className="text-sm text-slate-300">Metrics are within optimal enterprise bounds. Platform baseline is healthy.</p>
                 </div>
                 <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <p className="text-xs font-black text-slate-500 uppercase tracking-[0.15em] mb-1">Optimization</p>
                    <p className="text-sm text-slate-400">High review rate suggests opportunity for risk threshold tuning in low-value pools.</p>
                 </div>
              </div>
           </div>
           
           <button className="w-full py-4 rounded-2xl bg-white text-[#0b1020] font-black uppercase tracking-widest hover:bg-sky-400 transition-colors flex items-center justify-center gap-3 shadow-xl shadow-sky-500/5">
              <Search size={18} />
              Inspect Full Trace
           </button>
        </div>
      </div>
    </div>
  );
};

// Internal Shield mock for local component
const Shield = ({ size }) => <Trophy size={size} />;

export default EvaluationScorecards;
