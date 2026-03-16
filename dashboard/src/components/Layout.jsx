import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { 
  BarChart3, 
  ShieldCheck, 
  Users, 
  Activity, 
  Search, 
  LayoutDashboard,
  Bell,
  Settings
} from 'lucide-react';

const SidebarLink = ({ to, icon: Icon, label }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      `flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors rounded-xl ${
        isActive 
          ? 'bg-sky-500/10 text-sky-400 border border-sky-500/20' 
          : 'text-slate-400 hover:text-slate-100 hover:bg-white/5'
      }`
    }
  >
    <Icon size={18} />
    <span>{label}</span>
  </NavLink>
);

export const AppLayout = () => {
  return (
    <div className="flex h-screen bg-[#0b1020]">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/10 flex flex-col p-4">
        <div className="flex items-center gap-3 px-4 py-6 mb-4">
          <div className="w-8 h-8 bg-sky-500 rounded-lg flex items-center justify-center font-bold text-white">B</div>
          <span className="text-xl font-bold tracking-tight text-white">BlueShield</span>
        </div>
        
        <nav className="flex-1 space-y-1">
          <SidebarLink to="/" icon={LayoutDashboard} label="Executive Overview" />
          <SidebarLink to="/governance" icon={ShieldCheck} label="Governance & Risk" />
          <SidebarLink to="/reviews" icon={Users} label="Review Queue" />
          <SidebarLink to="/evals" icon={BarChart3} label="Evaluation & Evals" />
          <SidebarLink to="/traces" icon={Search} label="Audit Explorer" />
        </nav>

        <div className="pt-4 border-t border-white/10">
          <SidebarLink to="/settings" icon={Settings} label="Settings" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 border-b border-white/10 bg-[#0f172a]/50 backdrop-blur-xl flex items-center justify-between px-8">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span>Platform</span>
            <span>/</span>
            <span className="text-slate-100 font-medium">Dashboard</span>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/10 text-emerald-400 text-xs font-bold uppercase tracking-wider">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              System Healthy
            </div>
            <button className="text-slate-400 hover:text-white transition-colors">
              <Bell size={20} />
            </button>
            <div className="w-8 h-8 rounded-full bg-slate-700 border border-white/10 overflow-hidden">
               <div className="w-full h-full flex items-center justify-center text-xs font-bold">AG</div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <section className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </section>
      </main>
    </div>
  );
};
