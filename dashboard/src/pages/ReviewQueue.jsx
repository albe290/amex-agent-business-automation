import React, { useState } from 'react';
import { 
  History, 
  ExternalLink, 
  CheckCircle2, 
  XCircle, 
  CornerUpRight,
  Filter,
  MoreHorizontal
} from 'lucide-react';

const ReviewQueue = () => {
  const [activeTab, setActiveTab] = useState('pending');

  const cases = [
    { id: 'REV-1007', reqId: 'REQ-24019', domain: 'Merchant Ops', reason: 'High Risk Merchant + New Account', status: 'Pending', age: '12m', owner: 'A. Glenn' },
    { id: 'REV-1006', reqId: 'REQ-24017', domain: 'Compliance', reason: 'Large Value Dispute', status: 'Pending', age: '26m', owner: 'N. Pierce' },
    { id: 'REV-1005', reqId: 'REQ-24011', domain: 'Fraud Ops', reason: 'Velocity Pattern Alert', status: 'In Review', age: '41m', owner: 'Self' },
    { id: 'REV-1004', reqId: 'REQ-24010', domain: 'Consumer Card', reason: 'Account Override Request', status: 'Closed', age: '1h 12m', owner: 'A. Glenn' },
  ];

  return (
    <div className="space-y-8 animate-in zoom-in-95 duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Review Queue</h1>
          <p className="text-slate-400 mt-2">Human-in-the-loop decision capture and override tracking.</p>
        </div>
        <div className="flex gap-3">
          <div className="flex rounded-xl bg-white/5 border border-white/10 p-1">
             <button 
               onClick={() => setActiveTab('pending')}
               className={`px-4 py-2 text-xs font-bold uppercase tracking-wider rounded-lg transition-all ${activeTab === 'pending' ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/20' : 'text-slate-500 hover:text-slate-300'}`}
             >
               Pending
             </button>
             <button 
               onClick={() => setActiveTab('closed')}
               className={`px-4 py-2 text-xs font-bold uppercase tracking-wider rounded-lg transition-all ${activeTab === 'closed' ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/20' : 'text-slate-500 hover:text-slate-300'}`}
             >
               History
             </button>
          </div>
          <button className="p-3 rounded-xl bg-white/5 border border-white/10 text-slate-400 hover:text-white transition-colors">
            <Filter size={20} />
          </button>
        </div>
      </div>

      <div className="rounded-3xl border border-white/10 bg-[#121a2f] overflow-hidden">
        <div className="grid grid-cols-12 bg-white/5 px-6 py-4 text-xs font-bold uppercase tracking-[0.15em] text-slate-500">
          <div className="col-span-1">ID</div>
          <div className="col-span-2">Source Req</div>
          <div className="col-span-2">Domain</div>
          <div className="col-span-3">Review Reason</div>
          <div className="col-span-1">Age</div>
          <div className="col-span-2">Owner</div>
          <div className="col-span-1 text-right">Actions</div>
        </div>
        <div className="divide-y divide-white/5">
          {cases.map((c) => (
            <div key={c.id} className="grid grid-cols-12 px-6 py-5 items-center hover:bg-white/[0.02] transition-colors group">
              <div className="col-span-1">
                 <span className="font-bold text-sky-400 cursor-pointer hover:underline">{c.id}</span>
              </div>
              <div className="col-span-2 text-sm text-slate-300 font-mono">{c.reqId}</div>
              <div className="col-span-2">
                 <span className="text-xs font-bold px-2 py-1 rounded bg-white/5 text-slate-400 border border-white/10">{c.domain}</span>
              </div>
              <div className="col-span-3 text-sm text-slate-100">{c.reason}</div>
              <div className="col-span-1 text-xs text-slate-500">{c.age}</div>
              <div className="col-span-2">
                 <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-slate-700 flex items-center justify-center text-[10px] font-bold text-white border border-white/10">
                       {c.owner[0]}
                    </div>
                    <span className="text-sm text-slate-400">{c.owner}</span>
                 </div>
              </div>
              <div className="col-span-1 text-right flex justify-end gap-2">
                 <button className="p-2 rounded-lg bg-emerald-500/10 text-emerald-500 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-emerald-500 hover:text-white">
                    <CheckCircle2 size={16} />
                 </button>
                 <button className="p-2 rounded-lg bg-white/5 text-slate-400 hover:text-white opacity-0 group-hover:opacity-100 transition-opacity">
                    <MoreHorizontal size={16} />
                 </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
         <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
               <History className="text-sky-500" />
               Recent Overrides
            </h2>
            <div className="space-y-4">
               {[
                 { id: 'REQ-23992', analyst: 'A. Glenn', note: 'Verified via escalation channel.', type: 'APPROVAL' },
                 { id: 'REQ-23985', analyst: 'D. Smith', note: 'Policy block bypassed after compliance review.', type: 'ALLOW' },
               ].map((item, i) => (
                 <div key={i} className="p-4 rounded-2xl bg-[#0b1020] border border-white/10 relative overflow-hidden group">
                    <div className="flex justify-between items-start mb-2">
                       <span className="text-sm font-bold text-sky-400">{item.id}</span>
                       <span className="text-[10px] font-black uppercase tracking-widest text-emerald-500">{item.type}</span>
                    </div>
                    <p className="text-sm text-slate-300 italic">"{item.note}"</p>
                    <div className="mt-3 flex justify-between items-center bg-white/5 -mx-4 -mb-4 p-3 border-t border-white/10 group-hover:bg-sky-500/10 transition-colors">
                       <span className="text-xs text-slate-500 font-bold uppercase">Analyst: {item.analyst}</span>
                       <ExternalLink size={14} className="text-slate-600" />
                    </div>
                 </div>
               ))}
            </div>
         </div>

         <div className="rounded-3xl border border-white/10 bg-[#121a2f] p-8">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
               <CornerUpRight className="text-violet-500" />
               Queue Health
            </h2>
            <div className="space-y-6">
                <div className="flex justify-between items-center">
                   <span className="text-sm text-slate-400">Mean Time to Resolution (MTTR)</span>
                   <span className="text-lg font-bold text-white">18.4m</span>
                </div>
                <div className="flex justify-between items-center">
                   <span className="text-sm text-slate-400">Queue Depth</span>
                   <span className="text-lg font-bold text-white">4 Active</span>
                </div>
                <div className="h-px bg-white/5" />
                <div className="space-y-2">
                   <p className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-4">Availability Overview</p>
                   <div className="flex gap-2">
                      {[1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1].map((v, i) => (
                        <div key={i} className={`flex-1 h-8 rounded-md ${v ? 'bg-sky-500/20 border border-sky-500/20' : 'bg-white/5 border border-white/5 opacity-30'}`} />
                      ))}
                   </div>
                   <div className="flex justify-between text-[10px] text-slate-500 font-bold">
                      <span>00:00</span>
                      <span>12:00</span>
                      <span>23:59</span>
                   </div>
                </div>
            </div>
         </div>
      </div>
    </div>
  );
};

export default ReviewQueue;
