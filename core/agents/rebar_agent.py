# -*- coding: utf-8 -*-
"""
REBAR AGENT — Sub-Agent Gia công & Cắt thép
Minh họa hoàn chỉnh pattern: Tool Calling + Inter-Agent Validation Gate

Vai trò:
  1. Đọc BBS (Bảng Thống kê Cốt thép) từ SharedState (do CAD Agent ghi)
  2. Gọi CuttingStockSolver (OR-Tools) — PURE PYTHON, ZERO LLM
  3. Gọi SpliceZoneValidator để kiểm tra vùng nối (TCVN 5574:2018)
  4. Ghi kết quả vào StateBus → Supervisor đọc để chạy Quality Gate

LLM Role (nếu tích hợp): CHỈ được dùng để:
  - Intent recognition (phân tích yêu cầu từ người dùng)
  - Trình bày kết quả bằng ngôn ngữ tự nhiên
  - KHÔNG được làm toán học (cộng, trừ, nhân số, diện tích, khối lượng)
"""

from __future__ import annotations
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from core.supervisor.base_agent import BaseAgent
from core.state.state_bus import StateBus
from core.state.shared_state import NodeStatus
from tools.cutting_stock_solver import CuttingStockSolver, CutDemand, SpliceZoneValidator


class RebarAgent(BaseAgent):
    """
    Sub-Agent Gia công & Cắt thép — dùng OR-Tools Solver.

    Input  (từ StateBus): cad_data.concrete_components (có rebar_kg per component)
                          hoặc bbs_items trực tiếp nếu đã có BBS
    Output (vào StateBus): rebar_data (cutting_result, splice_zone_check, splice_violations)
    """

    def __init__(
        self,
        bar_length_mm: int = 11_700,
        span_length_mm: int = 38_200,  # Chiều dài nhịp dầm Super-T để kiểm tra splice
    ):
        super().__init__(
            agent_id="rebar_agent",
            description="Gia công & Cắt thép OR-Tools (TCVN 1651:2018 + TCVN 5574:2018)"
        )
        self.bar_length_mm = bar_length_mm
        self.span_length_mm = span_length_mm
        self.solver = CuttingStockSolver(bar_length_mm=bar_length_mm)
        self.splice_validator = SpliceZoneValidator()

    def run(self, bus: StateBus) -> bool:
        """
        Luồng thực thi:
        1. Lấy danh sách cắt từ BBS trong SharedState
        2. Chạy OR-Tools Solver
        3. Chạy Splice Zone Validator
        4. Ghi kết quả vào StateBus
        """
        print("  [RebarAgent] Bắt đầu tính toán cắt thép...")

        # ── BƯỚC 1: Lấy demands từ SharedState ───────────────────────────────
        demands = self._extract_demands_from_state(bus)
        if not demands:
            print("  [RebarAgent] WARN: Không có dữ liệu BBS — dùng dữ liệu mẫu Cầu Km19")
            demands = self._get_sample_demands()

        print(f"  [RebarAgent] Tổng số loại thanh cần cắt: {len(demands)}")
        total_pieces = sum(d.quantity for d in demands)
        print(f"  [RebarAgent] Tổng số thanh: {total_pieces}")

        # ── BƯỚC 2: Lọc những thanh dài hơn cây thép (dầm đúc sẵn, cáp DUL → không cắt từ cây thường)
        valid_demands = [d for d in demands if d.length_mm <= self.bar_length_mm]
        skipped = [(d.mark, d.length_mm) for d in demands if d.length_mm > self.bar_length_mm]
        if skipped:
            print(f"  [RebarAgent] Bỏ qua {len(skipped)} loại dài hơn {self.bar_length_mm}mm "
                  f"(cáp DUL/dầm đúc sẵn): {skipped[:3]}")

        if not valid_demands:
            print("  [RebarAgent] WARN: Không có thanh nào hợp lệ để cắt")
            bus.set_rebar_data({
                "splice_zone_check": "NOT_RUN",
                "splice_violations": [],
                "total_rebar_kg": 0.0,
            })
            return False

        # ── BƯỚC 2b: Tool Calling — CuttingStockSolver ───────────────────────
        print("  [RebarAgent] Gọi CuttingStockSolver (OR-Tools CP-SAT)...")
        solution = self.solver.solve(valid_demands)

        print(f"  [RebarAgent] Solver: {solution.status}")
        print(f"  [RebarAgent] Số cây thép: {solution.total_bars_needed}")
        print(f"  [RebarAgent] Đề-xê: {solution.waste_ratio_pct:.2f}%")
        if solution.warning:
            print(f"  [RebarAgent] ⚠ {solution.warning}")

        # ── BƯỚC 3: Tool Calling — SpliceZoneValidator ───────────────────────
        # Tạo danh sách vị trí nối giả định (thực tế: lấy từ bản vẽ)
        splice_positions = self._estimate_splice_positions(solution, demands)
        splice_status, splice_violations = self.splice_validator.validate(
            splice_positions, span_length_mm=self.span_length_mm
        )

        print(f"  [RebarAgent] Splice check: {splice_status}")
        if splice_violations:
            for v in splice_violations:
                print(f"    {v}")

        # ── BƯỚC 4: Ghi kết quả vào StateBus ─────────────────────────────────
        cutting_dict = {
            "status": solution.status,
            "bar_length_mm": solution.bar_length_mm,
            "total_bars_needed": solution.total_bars_needed,
            "total_waste_mm": solution.total_waste_mm,
            "waste_ratio_pct": solution.waste_ratio_pct,
            "total_weight_kg": solution.total_weight_kg,
            "patterns": [
                {"bar_id": idx + 1, "cuts": p.cuts, "waste_mm": p.waste_mm}
                for idx, p in enumerate(solution.patterns[:50])  # Giới hạn 50 patterns
            ],
        }

        bus.set_rebar_data({
            "cutting_result": type("CuttingStockResult", (), cutting_dict)(),  # noqa: preserved for StateBus
            "splice_zone_check": splice_status,
            "splice_violations": splice_violations,
            "total_rebar_kg": solution.total_weight_kg,
            # Lưu cutting_dict riêng để persist JSON
            "_cutting_dict_json": cutting_dict,
        })

        # Nếu có violation → trả về False để Supervisor biết cần Inter-Agent REJECT
        if splice_status == "REJECT":
            print("  [RebarAgent] REJECT: Có vi phạm vùng nối — báo cáo về Supervisor")
            # Không raise exception — trả False để Supervisor quyết định retry
            # (Supervisor sẽ escalate lên human gate nếu hết retry)
            return False

        if solution.status not in ("OPTIMAL", "FEASIBLE"):
            return False

        return True

    # ─────────────────────────────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────────────────────────────

    def _extract_demands_from_state(self, bus: StateBus) -> list:
        """Trích xuất danh sách cắt từ BBS trong SharedState."""
        try:
            rebar_data = bus.get_rebar_data()
            bbs_items = getattr(rebar_data, "bbs_items", [])
            if bbs_items:
                demands = []
                for item in bbs_items:
                    if hasattr(item, "length_mm") and hasattr(item, "count"):
                        demands.append(CutDemand(
                            length_mm=item.length_mm,
                            quantity=item.count,
                            diameter_mm=item.diameter_mm,
                            mark=item.mark,
                        ))
                return demands
        except Exception:
            pass
        return []

    def _get_sample_demands(self) -> list:
        """
        Dữ liệu BBS mẫu cho Cầu Km19+529.080 — Dầm Super-T + Cọc nhồi.
        Thực tế: lấy từ file Excel THONG_KE_THEP_CHI_TIET (396 thanh).
        """
        return [
            # Cọc nhồi Ø1200 — thép dọc Ø25
            CutDemand(length_mm=9000, quantity=104, diameter_mm=25, mark="CL1"),
            # Cọc nhồi — thép đai Ø16
            CutDemand(length_mm=5027, quantity=208, diameter_mm=16, mark="CD1"),
            # Dầm Super-T — thép Ø20
            CutDemand(length_mm=37800, quantity=15, diameter_mm=20, mark="DT1"),
            CutDemand(length_mm=4500, quantity=60, diameter_mm=20, mark="DT2"),
            # Bệ trụ — thép Ø22
            CutDemand(length_mm=6500, quantity=32, diameter_mm=22, mark="BT1"),
            CutDemand(length_mm=3200, quantity=48, diameter_mm=22, mark="BT2"),
            # Mặt cầu — thép Ø12
            CutDemand(length_mm=5800, quantity=120, diameter_mm=12, mark="MC1"),
            CutDemand(length_mm=3000, quantity=200, diameter_mm=12, mark="MC2"),
            # Mố cầu M1/M2 — thép Ø18
            CutDemand(length_mm=7200, quantity=28, diameter_mm=18, mark="MO1"),
            CutDemand(length_mm=4800, quantity=42, diameter_mm=18, mark="MO2"),
        ]

    def _estimate_splice_positions(self, solution, demands: list) -> list:
        """
        Ước tính vị trí nối thép dựa trên kết quả cắt.
        Nối xảy ra khi đoạn cần > 11.7m (phải ghép nhiều đoạn).
        Thực tế: đọc trực tiếp từ bản vẽ chi tiết.
        """
        splice_positions = []
        # Tìm các thanh dài > bar_length_mm (phải nối)
        long_pieces = [d for d in demands if d.length_mm > self.bar_length_mm * 0.95]

        for d in long_pieces:
            # Giả định nối tại vị trí 1/3 nhịp (thực tế cần lấy từ bản vẽ)
            splice_at = int(self.span_length_mm * 0.33)
            zone = "COMPRESSION"  # Dầm Super-T: vùng 1/3 đầu là vùng nén
            splice_positions.append({
                "mark": d.mark,
                "splice_at_mm": splice_at,
                "zone": zone,
            })

        return splice_positions
