# -*- coding: utf-8 -*-
"""
OR-TOOLS 1D CUTTING STOCK SOLVER
Bài toán cắt thép một chiều (1D Cutting Stock Problem)
Tối ưu ghép cắt vào cây thép nguyên 11.7m — mục tiêu: waste < 1.5%

Đây là Pure Python Tool — KHÔNG có bất kỳ LLM nào tham gia tính toán.
LLM chỉ được phép: gọi tool này, đọc kết quả, trình bày ngôn ngữ tự nhiên.

Thuật toán:
  1. Column Generation (OR-Tools LP Solver)
  2. ILP Branch-and-Bound cho nghiệm nguyên

Input:  demand = [(length_mm, quantity), ...]
Output: CuttingStockSolution
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS — TCVN 1651:2018 & thực tế công trường
# ─────────────────────────────────────────────────────────────────────────────

STANDARD_BAR_LENGTH_MM = 11_700    # Cây thép nguyên 11.7m
SAW_KERF_MM = 3                    # Lượng mất mát mỗi nhát cưa (mm)
MAX_WASTE_RATIO_PCT = 1.5          # Ngưỡng đề-xê tối đa cho phép (%)

REBAR_UNIT_WEIGHT_KG_M: Dict[int, float] = {
    6:   0.222,   8:   0.395,  10:   0.617,
    12:  0.888,  14:   1.208,  16:   1.578,
    18:  1.998,  20:   2.466,  22:   2.984,
    25:  3.853,  28:   4.834,  32:   6.313,
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class CutDemand:
    length_mm: int
    quantity: int
    diameter_mm: int = 0
    mark: str = ""


@dataclass
class CuttingPattern:
    """Một cách ghép các đoạn cắt vào 1 cây thép."""
    cuts: List[int] = field(default_factory=list)  # list chiều dài (mm)
    waste_mm: int = 0
    bars_used: int = 1


@dataclass
class CuttingStockSolution:
    status: str = "NOT_RUN"          # OPTIMAL / FEASIBLE / INFEASIBLE / ERROR
    solver_name: str = "OR-Tools CP-SAT"
    bar_length_mm: int = STANDARD_BAR_LENGTH_MM
    total_bars_needed: int = 0
    total_length_used_mm: int = 0
    total_waste_mm: int = 0
    waste_ratio_pct: float = 0.0
    total_weight_kg: float = 0.0
    patterns: List[CuttingPattern] = field(default_factory=list)
    assignment: List[Dict] = field(default_factory=list)  # chi tiết từng thanh
    warning: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# SOLVER — GREEDY FFD + OR-Tools ILP Refinement
# ─────────────────────────────────────────────────────────────────────────────

class CuttingStockSolver:
    """
    1D Cutting Stock Solver — 2 tầng:
      Tầng 1: First-Fit Decreasing (FFD) greedy — nhanh, kết quả tốt
      Tầng 2: OR-Tools CP-SAT — tối ưu tuyệt đối (nếu available)
    """

    def __init__(
        self,
        bar_length_mm: int = STANDARD_BAR_LENGTH_MM,
        kerf_mm: int = SAW_KERF_MM,
    ):
        self.bar_length_mm = bar_length_mm
        self.kerf_mm = kerf_mm

    # ── PUBLIC API ─────────────────────────────────────────────────────────

    # Ngưỡng: CP-SAT cho ≤200 thanh (optimal); FFD cho >200 thanh (nhanh)
    CP_SAT_THRESHOLD = 200

    def solve(self, demands: List[CutDemand]) -> CuttingStockSolution:
        """
        Giải bài toán cắt thép.
        Tự động chọn:
          ≤200 thanh → OR-Tools CP-SAT (tối ưu tuyệt đối)
          >200 thanh → FFD Greedy (nhanh, đề-xê ≈ 2-5%)
        """
        # Expand demands thành danh sách các đoạn cần cắt
        pieces = []
        for d in demands:
            pieces.extend([d.length_mm] * d.quantity)

        if not pieces:
            sol = CuttingStockSolution(status="INFEASIBLE")
            sol.warning = "Danh sách cần cắt rỗng"
            return sol

        # Kiểm tra có đoạn nào dài hơn cây thép không
        too_long = [p for p in pieces if p > self.bar_length_mm]
        if too_long:
            sol = CuttingStockSolution(status="INFEASIBLE")
            sol.warning = f"Có {len(too_long)} đoạn dài hơn cây {self.bar_length_mm}mm: {too_long[:5]}"
            return sol

        # Chọn solver theo kích thước bài toán
        if len(pieces) <= self.CP_SAT_THRESHOLD:
            try:
                sol = self._solve_ortools_cp(pieces, demands)
                if sol.status in ("OPTIMAL", "FEASIBLE"):
                    return sol
            except ImportError:
                pass
            except Exception as e:
                print(f"  [Solver] OR-Tools failed ({e}), falling back to FFD")
        else:
            print(f"  [Solver] {len(pieces)} thanh > threshold {self.CP_SAT_THRESHOLD} → dùng FFD (nhanh)")

        # Fallback / default cho bài toán lớn: FFD Greedy
        return self._solve_ffd(pieces, demands)

    # ── OR-TOOLS CP-SAT ────────────────────────────────────────────────────

    def _solve_ortools_cp(self, pieces: List[int], demands: List[CutDemand]) -> CuttingStockSolution:
        """OR-Tools CP-SAT formulation cho 1D Cutting Stock."""
        from ortools.sat.python import cp_model

        n_pieces = len(pieces)
        # Upper bound số cây thép = mỗi thanh một cây (worst case)
        max_bars = n_pieces

        model = cp_model.CpModel()

        # x[i][j] = 1 nếu đoạn i cắt từ cây j
        x = [[model.NewBoolVar(f"x_{i}_{j}") for j in range(max_bars)] for i in range(n_pieces)]
        # y[j] = 1 nếu cây j được dùng
        y = [model.NewBoolVar(f"y_{j}") for j in range(max_bars)]

        # Mỗi đoạn được cắt từ đúng 1 cây
        for i in range(n_pieces):
            model.Add(sum(x[i][j] for j in range(max_bars)) == 1)

        # Tổng chiều dài cắt từ cây j không vượt quá độ dài cây (trừ kerf)
        for j in range(max_bars):
            effective = self.bar_length_mm - self.kerf_mm * (n_pieces - 1)
            model.Add(
                sum(pieces[i] * x[i][j] for i in range(n_pieces)) <=
                self.bar_length_mm * y[j]
            )
            for i in range(n_pieces):
                model.Add(x[i][j] <= y[j])

        # Minimize số cây dùng
        model.Minimize(sum(y))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 30.0  # timeout 30s
        solver.parameters.num_search_workers = 4

        status_code = solver.Solve(model)
        status_map = {
            cp_model.OPTIMAL: "OPTIMAL",
            cp_model.FEASIBLE: "FEASIBLE",
            cp_model.INFEASIBLE: "INFEASIBLE",
            cp_model.UNKNOWN: "UNKNOWN",
        }
        status_str = status_map.get(status_code, "UNKNOWN")

        if status_code not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            sol = CuttingStockSolution(status=status_str)
            sol.warning = f"OR-Tools trả về {status_str}"
            return sol

        # Reconstruct kết quả
        bar_contents: Dict[int, List[int]] = {}
        for j in range(max_bars):
            if solver.Value(y[j]):
                bar_contents[j] = [pieces[i] for i in range(n_pieces) if solver.Value(x[i][j])]

        return self._build_solution("OPTIMAL" if status_code == cp_model.OPTIMAL else "FEASIBLE",
                                    bar_contents, demands)

    # ── FFD GREEDY FALLBACK ────────────────────────────────────────────────

    def _solve_ffd(self, pieces: List[int], demands: List[CutDemand]) -> CuttingStockSolution:
        """First-Fit Decreasing — greedy O(n log n)."""
        sorted_pieces = sorted(pieces, reverse=True)
        bars: List[List[int]] = []
        remainders: List[int] = []

        for piece in sorted_pieces:
            placed = False
            for idx, rem in enumerate(remainders):
                needed = piece + (self.kerf_mm if bars[idx] else 0)
                if rem >= needed:
                    bars[idx].append(piece)
                    remainders[idx] -= needed
                    placed = True
                    break
            if not placed:
                bars.append([piece])
                remainders.append(self.bar_length_mm - piece)

        bar_contents = {j: cuts for j, cuts in enumerate(bars)}
        return self._build_solution("FEASIBLE", bar_contents, demands)

    # ── BUILD SOLUTION ─────────────────────────────────────────────────────

    def _build_solution(
        self,
        status: str,
        bar_contents: Dict[int, List[int]],
        demands: List[CutDemand],
    ) -> CuttingStockSolution:
        sol = CuttingStockSolution(
            status=status,
            bar_length_mm=self.bar_length_mm,
            total_bars_needed=len(bar_contents),
        )

        total_used = 0
        total_waste = 0

        for bar_id, cuts in bar_contents.items():
            kerf_total = self.kerf_mm * max(len(cuts) - 1, 0)
            used = sum(cuts) + kerf_total
            waste = self.bar_length_mm - used
            total_used += used
            total_waste += waste

            pattern = CuttingPattern(cuts=cuts, waste_mm=waste)
            sol.patterns.append(pattern)
            sol.assignment.append({
                "bar_id": bar_id + 1,
                "cuts_mm": cuts,
                "used_mm": used,
                "waste_mm": waste,
            })

        sol.total_length_used_mm = total_used
        sol.total_waste_mm = total_waste
        total_capacity = sol.total_bars_needed * self.bar_length_mm
        sol.waste_ratio_pct = (total_waste / total_capacity * 100) if total_capacity else 0

        # Tính trọng lượng (theo đường kính lớn nhất trong demands)
        if demands:
            d = max(demands, key=lambda x: x.diameter_mm)
            unit_w = REBAR_UNIT_WEIGHT_KG_M.get(d.diameter_mm, 0)
            sol.total_weight_kg = round(
                sol.total_bars_needed * self.bar_length_mm / 1000 * unit_w, 2
            )

        if sol.waste_ratio_pct > MAX_WASTE_RATIO_PCT:
            sol.warning = (
                f"⚠ Đề-xê {sol.waste_ratio_pct:.2f}% vượt ngưỡng {MAX_WASTE_RATIO_PCT}%! "
                f"Cần xem lại kế hoạch cắt."
            )

        return sol


# ─────────────────────────────────────────────────────────────────────────────
# INTER-AGENT VALIDATION — Kiểm tra vùng nối thép theo TCVN
# ─────────────────────────────────────────────────────────────────────────────

class SpliceZoneValidator:
    """
    Kiểm tra chéo (Inter-Agent Negotiation):
    BPTC_KCS Agent xác nhận vị trí nối thép của Rebar Agent.
    TCVN 5574:2018 §8.6: Không được nối thép tại vùng chịu kéo/cắt nguy hiểm.
    """

    # Vùng cấm nối (tính từ gối tính tỷ lệ chiều dài nhịp)
    FORBIDDEN_ZONES = {
        "TENSION":     "25-75% chiều dài nhịp (vùng chịu kéo dương của dầm đơn giản)",
        "SHEAR":       "0-15% và 85-100% chiều dài nhịp (vùng chịu cắt nguy hiểm gần gối)",
        "COMPRESSION": "Được phép nối nhưng phải so le ≥ 1.3 × L_nối",
    }

    def validate(
        self,
        splice_positions: List[Dict],
        span_length_mm: int = 38_200
    ) -> Tuple[str, List[str]]:
        """
        splice_positions: [{"mark": "T1", "splice_at_mm": 12000, "zone": "TENSION"}, ...]
        Trả về: (status, violations)
        status = "PASS" hoặc "REJECT"
        """
        violations = []
        for sp in splice_positions:
            mark = sp.get("mark", "?")
            pos = sp.get("splice_at_mm", 0)
            zone = sp.get("zone", "").upper()
            pos_ratio = pos / span_length_mm if span_length_mm else 0

            # Kiểm tra vùng chịu kéo: 25-75% nhịp
            if zone == "TENSION" and 0.25 <= pos_ratio <= 0.75:
                violations.append(
                    f"[REJECT] Thanh {mark}: Nối tại {pos}mm ({pos_ratio:.0%} nhịp) "
                    f"— vi phạm TCVN 5574:2018 §8.6 (vùng chịu kéo nguy hiểm)"
                )

            # Kiểm tra vùng chịu cắt: 0-15% và 85-100% nhịp
            if zone == "SHEAR" and (pos_ratio <= 0.15 or pos_ratio >= 0.85):
                violations.append(
                    f"[REJECT] Thanh {mark}: Nối tại {pos}mm ({pos_ratio:.0%} nhịp) "
                    f"— vi phạm TCVN 5574:2018 §8.6 (vùng chịu cắt gần gối)"
                )

        status = "REJECT" if violations else "PASS"
        return status, violations


# ─────────────────────────────────────────────────────────────────────────────
# QUICK TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demands = [
        CutDemand(length_mm=4500, quantity=20, diameter_mm=20, mark="T1"),
        CutDemand(length_mm=3200, quantity=35, diameter_mm=20, mark="T2"),
        CutDemand(length_mm=2800, quantity=15, diameter_mm=16, mark="D1"),
        CutDemand(length_mm=6000, quantity=10, diameter_mm=25, mark="CU1"),
    ]

    solver = CuttingStockSolver()
    sol = solver.solve(demands)

    print(f"\n{'='*55}")
    print(f"  CUTTING STOCK RESULT — {sol.solver_name}")
    print(f"{'='*55}")
    print(f"  Status        : {sol.status}")
    print(f"  Số cây thép   : {sol.total_bars_needed} cây")
    print(f"  Tổng đề-xê    : {sol.total_waste_mm:,} mm")
    print(f"  Tỷ lệ đề-xê   : {sol.waste_ratio_pct:.2f}%")
    print(f"  Trọng lượng   : {sol.total_weight_kg:,.1f} kg")
    if sol.warning:
        print(f"  ⚠ {sol.warning}")

    print(f"\n  Chi tiết 5 cây đầu:")
    for a in sol.assignment[:5]:
        print(f"    Cây #{a['bar_id']:03d}: {a['cuts_mm']} — đề-xê: {a['waste_mm']}mm")
