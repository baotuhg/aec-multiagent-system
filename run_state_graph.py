# -*- coding: utf-8 -*-
"""
RUN STATE GRAPH — Entry Point cho 23HG MultiAgent System v3.0
Kiến trúc: State Graph + Supervisor Pattern (thay thế Linear Pipeline cũ)

Dùng lệnh:
  python run_state_graph.py                       # Chạy toàn bộ (auto-approve human gate)
  python run_state_graph.py --phase cad rebar     # Chạy chọn phase
  python run_state_graph.py --human-gate cli      # Bật chế độ CLI approval
  python run_state_graph.py --solver-test         # Chỉ test OR-Tools solver

Backward compatibility:
  Pipeline cũ (run_pipeline.py) vẫn hoạt động bình thường.
  Script này chạy SONG SONG — không thay thế file cũ.
"""

import argparse
import os
import sys

# Thêm project root vào sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from core.supervisor.supervisor_agent import AECSupervisor
from core.state.shared_state import ProjectPhase


# ── CONFIG ───────────────────────────────────────────────────────────────────

EXCEL_MASTER = os.path.join(ROOT, "templates", "Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx")
DRAWINGS_FOLDER = r"c:\Users\baotu\Downloads\Documents\HSTK Cầu Km19+529.080_Marker\HSTK Cầu Km19+529.080_Marker\01.CAU KM19+529.08"
RUNTIME_STATE = os.path.join(ROOT, "agents", "RUNTIME_STATE.json")


PHASE_MAP = {
    "cad":      ProjectPhase.CAD_TAKEOFF,
    "rebar":    ProjectPhase.REBAR_CUT,
    "qs":       ProjectPhase.QS_ESTIMATE,
    "qaqc":     ProjectPhase.QAQC_REVIEW,
    "gate":     ProjectPhase.HUMAN_GATE,
    "schedule": ProjectPhase.SCHEDULE_CPM,
    "asbuilt":  ProjectPhase.ASBUILT_LOOP,
}


# ── MAIN ─────────────────────────────────────────────────────────────────────

def run_solver_test():
    """Quick test OR-Tools + CPM Calculator."""
    print("\n" + "═" * 55)
    print("  TEST: OR-Tools Cutting Stock Solver")
    print("═" * 55)

    from tools.cutting_stock_solver import CuttingStockSolver, CutDemand
    demands = [
        CutDemand(length_mm=4500, quantity=30, diameter_mm=20, mark="T1"),
        CutDemand(length_mm=3200, quantity=50, diameter_mm=20, mark="T2"),
        CutDemand(length_mm=2800, quantity=20, diameter_mm=16, mark="D1"),
    ]
    sol = CuttingStockSolver().solve(demands)
    print(f"  Status: {sol.status}")
    print(f"  Số cây: {sol.total_bars_needed}")
    print(f"  Đề-xê: {sol.waste_ratio_pct:.2f}%")
    if sol.warning:
        print(f"  ⚠ {sol.warning}")

    print("\n" + "═" * 55)
    print("  TEST: CPM Calculator")
    print("═" * 55)

    from tools.cpm_calculator import CPMCalculator
    tasks = [
        {"id": "T01", "name": "Tim mốc", "duration": 3, "predecessors": []},
        {"id": "T02", "name": "Cọc nhồi", "duration": 30, "predecessors": ["T01"]},
        {"id": "T03", "name": "Bệ trụ", "duration": 20, "predecessors": ["T02"]},
        {"id": "T04", "name": "Dầm Super-T", "duration": 10, "predecessors": ["T03"]},
        {"id": "T05", "name": "Thử tải", "duration": 5, "predecessors": ["T04"]},
    ]
    result = CPMCalculator().calculate(tasks, start_date_str="2026-10-01")
    print(f"  Tổng thời gian: {result.total_duration_days} ngày")
    print(f"  Hoàn thành: {result.project_finish}")
    print(f"  Đường găng: {' → '.join(result.critical_path)}")
    print("\n  ✅ Tất cả tools hoạt động bình thường!\n")


def main():
    parser = argparse.ArgumentParser(
        description="23HG MultiAgent System v3.0 — State Graph + Supervisor"
    )
    parser.add_argument(
        "--phase", nargs="*",
        choices=list(PHASE_MAP.keys()),
        help="Chỉ chạy các phase được chỉ định (mặc định: tất cả)"
    )
    parser.add_argument(
        "--human-gate", choices=["cli", "auto", "file"],
        default="auto",
        help="Chế độ Human Gate (mặc định: auto)"
    )
    parser.add_argument(
        "--solver-test", action="store_true",
        help="Chỉ test OR-Tools và CPM Calculator"
    )
    parser.add_argument(
        "--excel", default=EXCEL_MASTER,
        help="Đường dẫn file Excel master"
    )
    parser.add_argument(
        "--drawings", default=DRAWINGS_FOLDER,
        help="Thư mục chứa bản vẽ DWG"
    )

    args = parser.parse_args()

    if args.solver_test:
        run_solver_test()
        return

    # Khởi tạo Supervisor
    supervisor = AECSupervisor(
        project_root=ROOT,
        excel_master_path=args.excel,
        drawings_folder=args.drawings,
        human_gate_mode=args.human_gate,
        max_retries=3,
        persist_path=RUNTIME_STATE,
    )

    # Đăng ký tất cả Sub-Agent
    from core.agents.sub_agents import (
        CADAgent, QSAgent, BPTCKCSAgent, SchedulerAgent
    )
    from core.agents.rebar_agent import RebarAgent
    from core.agents.asbuilt_agent import AsBuiltAgent

    supervisor.register_agent(CADAgent(drawings_folder=args.drawings))
    supervisor.register_agent(RebarAgent())
    supervisor.register_agent(QSAgent())
    supervisor.register_agent(BPTCKCSAgent())
    supervisor.register_agent(SchedulerAgent())
    supervisor.register_agent(AsBuiltAgent())

    # Chọn phases
    selected_phases = None
    if args.phase:
        selected_phases = [PHASE_MAP[p] for p in args.phase]

    # Chạy State Graph
    success = supervisor.run(phases=selected_phases)

    # In báo cáo cuối
    report = supervisor.get_status_report()
    print(f"\n  📋 Báo cáo cuối:")
    print(f"     Session   : {report['session_id']}")
    print(f"     Phase     : {report['phase']}")
    print(f"     Cập nhật  : {report['updated_at']}")
    print(f"     Lỗi       : {report['errors_count']}")
    print(f"     Chờ duyệt : {report['pending_approvals']}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
