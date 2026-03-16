from app.evals.scenarios import get_baseline_scenarios
from app.evals.offline_eval import OfflineEvalEngine
from app.evals.metrics import PlatformMetrics
from app.evals.scorecard import PlatformScorecard
from app.evals.analyzer import EvalAnalyzer
from app.evals.reporter import EvalReporter

def run_full_evaluation():
    print("--- Phase 4: Platform Evaluation Suite ---")
    
    # 1. Initialize Engine
    engine = OfflineEvalEngine()
    metrics_calc = PlatformMetrics()
    scorecard_gen = PlatformScorecard()
    analyzer = EvalAnalyzer()
    reporter = EvalReporter()

    # 2. Load and Run Scenarios
    print("\n[STEP 1] Loading baseline scenarios...")
    scenarios = get_baseline_scenarios()
    
    print(f"[STEP 2] Running {len(scenarios)} cases through the platform...")
    results = engine.run_suite(scenarios)
    
    # 3. Process Metrics
    print("[STEP 3] Calculating performance signals...")
    metrics = metrics_calc.calculate_snapshot(results)
    
    # 4. Generate Scorecard and Insights
    print("[STEP 4] Generating qualitative scorecard...")
    scorecard = scorecard_gen.generate(metrics)
    insights = analyzer.analyze(metrics)
    
    # 5. Output Report
    reporter.print_summary(results, metrics, scorecard, insights)

if __name__ == "__main__":
    run_full_evaluation()
