import React from 'react';
import { 
  ShieldAlert, 
  ShieldCheck, 
  Lock, 
  AlertTriangle,
  ChevronRight
} from 'lucide-react';

const PolicyRow = ({ name, count, level }) => {
  const levelColors = {
    high: 'text-rose-400',
    medium: 'text-amber-400',
    low: 'text-sky-400'
  };

  return (
    <div className="flex items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/10 hover:border-white/20 transition-colors group cursor-pointer">
      <div className="flex items-center gap-4">
        <div className={`p-2 rounded-xl bg-white/5 ${levelColors[level]}`}>
          <ShieldAlert size={18} />
        </div>
        <div>
          <p className="font-semibold text-slate-100">{name}</p>
          <p className="text-xs text-slate-500 uppercase font-bold tracking-wider">{level} severity</p>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-xl font-bold text-white">{count}</span>
        <ChevronRight size={18} className="text-slate-600 group-hover:text-slate-300 transition-colors" />
      </div>
    </div>
  );
};

const GovernanceRisk = () => {
  return (
    <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-700">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Governance & Risk</h1>
        <p className="text-slate-400 mt-2">Real-time policy enforcement and runtime boundary monitoring.</p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Policy Section */}
        <div className="xl:col-span-2 space-y-6">
          <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8">
            <h2 className="text-xl font-bold text-white mb-6">Policy Enforcement Feed</h2>
            <div className="space-y-4">
              <PolicyRow name="HIGH_VALUE_TRANSACTION" count={42} level="high" />
              <PolicyRow name="RISK_SCORE_CRITICAL" count={28} level="high" />
              <PolicyRow name="AML_SECTION_3_COMPLIANCE" count={114} level="low" />
              <PolicyRow name="MANUAL_OVERRIDE_TRIGGER" count={17} level="medium" />
              <PolicyRow name="SECURITY_VALIDATION_FAILURE" count={9} level="high" />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-6 flex items-center gap-6">
                <div className="p-4 rounded-2xl bg-rose-500/10 text-rose-500">
                   <Lock size={28} />
                </div>
                <div>
                   <p className="text-sm font-medium text-slate-500 underline decoration-rose-500/30">Action Blocks</p>
                   <p className="text-3xl font-bold text-white">23</p>
                </div>
             </div>
             <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-6 flex items-center gap-6">
                <div className="p-4 rounded-2xl bg-amber-500/10 text-amber-500">
                   <AlertTriangle size={28} />
                </div>
                <div>
                   <p className="text-sm font-medium text-slate-500 underline decoration-amber-500/30">Runtime Warnings</p>
                   <p className="text-3xl font-bold text-white">156</p>
                </div>
             </div>
          </div>
        </div>

        {/* Risk Profile Card */}
        <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8">
          <h2 className="text-xl font-bold text-white mb-6">Risk Profile Matrix</h2>
          <div className="h-64 flex items-center justify-center relative">
            {/* Visual representation of a risk radar or simple radial */}
             <div className="w-48 h-48 rounded-full border-[10px] border-emerald-500/20 flex flex-col items-center justify-center">
                <ShieldCheck size={48} className="text-emerald-500 mb-2" />
                <span className="text-2xl font-black text-white">SAFE</span>
                <span className="text-[10px] font-bold text-slate-500 tracking-widest uppercase">Platform Bias</span>
             </div>
             <div className="absolute top-0 right-0 w-12 h-12 bg-rose-500 rounded-full blur-3xl opacity-20" />
             <div className="absolute bottom-10 left-0 w-20 h-20 bg-emerald-500 rounded-full blur-[80px] opacity-20" />
          </div>

          <div className="mt-8 space-y-4">
             <div className="flex justify-between items-center text-sm p-3 rounded-xl bg-white/5">
                <span className="text-slate-400">Strictness Level</span>
                <span className="text-sky-400 font-bold uppercase tracking-tighter">Enterprise Standard</span>
             </div>
             <div className="flex justify-between items-center text-sm p-3 rounded-xl bg-white/5">
                <span className="text-slate-400">Policy Version</span>
                <span className="text-slate-200 font-bold">v3.42.0</span>
             </div>
             <div className="flex justify-between items-center text-sm p-3 rounded-xl bg-white/5">
                <span className="text-slate-400">Governance Lag</span>
                <span className="text-emerald-400 font-bold">12ms</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GovernanceRisk;
