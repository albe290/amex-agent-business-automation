import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppLayout } from './components/Layout';
import ExecutiveOverview from './pages/ExecutiveOverview';
import GovernanceRisk from './pages/GovernanceRisk';
import ReviewQueue from './pages/ReviewQueue';
import EvaluationScorecards from './pages/EvaluationScorecards';

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<ExecutiveOverview />} />
          <Route path="/governance" element={<GovernanceRisk />} />
          <Route path="/reviews" element={<ReviewQueue />} />
          <Route path="/evals" element={<EvaluationScorecards />} />
          <Route path="/traces" element={<div className="text-slate-400">Audit Explorer (Coming Soon)</div>} />
          <Route path="/settings" element={<div className="text-slate-400">Settings (Coming Soon)</div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
