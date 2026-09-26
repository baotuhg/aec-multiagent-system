# -*- coding: utf-8 -*-
"""
CPM CALCULATOR — Critical Path Method (Phương pháp đường găng)
Pure Python, Zero LLM — tính toán xác định 100% bằng code.

Tính:
  - Early Start (ES), Early Finish (EF) — Forward Pass
  - Late Start (LS), Late Finish (LF) — Backward Pass
  - Total Float (TF) = LF - EF
  - Critical Path (TF = 0)
  - So sánh Planned vs Actual — As-Built Loop

Input: tasks = [{"id":..., "name":..., "duration":..., "predecessors":[...]}]
Output: CPMResult
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from datetime import date, timedelta


@dataclass
class CPMTask:
    task_id: str
    name: str
    duration_days: int
    predecessors: List[str] = field(default_factory=list)
    # Calculated
    es: int = 0    # Early Start (ngày thứ)
    ef: int = 0    # Early Finish
    ls: int = 0    # Late Start
    lf: int = 0    # Late Finish
    tf: int = 0    # Total Float
    is_critical: bool = False
    # As-Built
    planned_volume: float = 0.0
    actual_volume: float = 0.0
    actual_start_day: Optional[int] = None
    actual_finish_day: Optional[int] = None


@dataclass
class CPMResult:
    tasks: List[CPMTask] = field(default_factory=list)
    critical_path: List[str] = field(default_factory=list)
    total_duration_days: int = 0
    project_start: str = ""
    project_finish: str = ""
    overall_progress_pct: float = 0.0
    delay_days: int = 0
    status: str = "OK"
    warnings: List[str] = field(default_factory=list)


class CPMCalculator:
    """
    Tính Critical Path Method theo thuật toán Topological Sort + Forward/Backward Pass.
    """

    def calculate(self, tasks_input: List[Dict[str, Any]], start_date_str: str = "") -> CPMResult:
        """
        tasks_input: [
            {"id": "T01", "name": "Tim mốc định vị", "duration": 3, "predecessors": []},
            {"id": "T02", "name": "Đường công vụ", "duration": 7, "predecessors": ["T01"]},
            ...
        ]
        """
        result = CPMResult()

        # Build task dict
        task_dict: Dict[str, CPMTask] = {}
        for t in tasks_input:
            cpm_task = CPMTask(
                task_id=t["id"],
                name=t.get("name", t["id"]),
                duration_days=int(t.get("duration", 1)),
                predecessors=t.get("predecessors", []),
                planned_volume=t.get("planned_volume", 0.0),
                actual_volume=t.get("actual_volume", 0.0),
                actual_start_day=t.get("actual_start_day"),
                actual_finish_day=t.get("actual_finish_day"),
            )
            task_dict[cpm_task.task_id] = cpm_task

        if not task_dict:
            result.status = "ERROR"
            result.warnings.append("Không có công việc nào được cung cấp")
            return result

        # Topological Sort (Kahn's algorithm)
        order = self._topological_sort(task_dict)
        if order is None:
            result.status = "ERROR"
            result.warnings.append("Phát hiện vòng lặp (circular dependency) trong biểu đồ CPM!")
            return result

        # Forward Pass — tính ES, EF
        for tid in order:
            t = task_dict[tid]
            if not t.predecessors:
                t.es = 0
            else:
                t.es = max(task_dict[p].ef for p in t.predecessors if p in task_dict)
            t.ef = t.es + t.duration_days

        # Project duration
        total_dur = max(t.ef for t in task_dict.values())
        result.total_duration_days = total_dur

        # Backward Pass — tính LS, LF
        for tid in reversed(order):
            t = task_dict[tid]
            successors = [s for s in task_dict.values() if tid in s.predecessors]
            if not successors:
                t.lf = total_dur
            else:
                t.lf = min(s.ls for s in successors)
            t.ls = t.lf - t.duration_days
            t.tf = t.lf - t.ef
            t.is_critical = (t.tf == 0)

        # Critical Path
        result.critical_path = [tid for tid in order if task_dict[tid].is_critical]
        result.tasks = list(task_dict.values())

        # Date mapping
        if start_date_str:
            try:
                start = date.fromisoformat(start_date_str)
                result.project_start = start_date_str
                finish = start + timedelta(days=total_dur)
                result.project_finish = finish.isoformat()
            except ValueError:
                result.warnings.append(f"Không thể parse ngày bắt đầu: {start_date_str}")

        # As-Built: tính % hoàn thành và delay
        result = self._calculate_asbuilt(result, task_dict)

        return result

    def _topological_sort(self, task_dict: Dict[str, CPMTask]) -> Optional[List[str]]:
        """Kahn's algorithm — trả về None nếu có vòng."""
        in_degree: Dict[str, int] = {tid: 0 for tid in task_dict}
        for t in task_dict.values():
            for p in t.predecessors:
                if p in in_degree:
                    in_degree[t.task_id] += 1

        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            queue.sort()  # Deterministic ordering
            tid = queue.pop(0)
            order.append(tid)
            for t in task_dict.values():
                if tid in t.predecessors:
                    in_degree[t.task_id] -= 1
                    if in_degree[t.task_id] == 0:
                        queue.append(t.task_id)

        if len(order) != len(task_dict):
            return None  # Circular dependency
        return order

    def _calculate_asbuilt(self, result: CPMResult, task_dict: Dict[str, CPMTask]) -> CPMResult:
        """So sánh Planned vs Actual để tính % hoàn thành và delay."""
        total_planned = sum(t.planned_volume for t in task_dict.values())
        total_actual = sum(t.actual_volume for t in task_dict.values())

        if total_planned > 0:
            result.overall_progress_pct = round(total_actual / total_planned * 100, 1)

        # Delay: dựa trên ngày thực tế của công việc găng cuối
        critical_tasks = [t for t in task_dict.values() if t.is_critical]
        if critical_tasks and any(t.actual_finish_day is not None for t in critical_tasks):
            last_critical = max(critical_tasks, key=lambda t: t.ef)
            if last_critical.actual_finish_day is not None:
                result.delay_days = max(0, last_critical.actual_finish_day - last_critical.ef)

        return result


# ─────────────────────────────────────────────────────────────────────────────
# QUICK TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tasks = [
        {"id": "T01", "name": "Tim mốc định vị", "duration": 3, "predecessors": []},
        {"id": "T02", "name": "Đường công vụ", "duration": 7, "predecessors": ["T01"]},
        {"id": "T03", "name": "Khoan dò Karst", "duration": 14, "predecessors": ["T02"]},
        {"id": "T04", "name": "Cọc nhồi T1/T2", "duration": 30, "predecessors": ["T03"]},
        {"id": "T05", "name": "Bệ trụ T1/T2", "duration": 20, "predecessors": ["T04"]},
        {"id": "T06", "name": "Thân đặc T1/T2", "duration": 25, "predecessors": ["T05"]},
        {"id": "T07", "name": "Xà mũ T1/T2", "duration": 15, "predecessors": ["T06"]},
        {"id": "T08", "name": "Lao dầm Super-T", "duration": 10, "predecessors": ["T07"]},
        {"id": "T09", "name": "Mặt cầu C35", "duration": 30, "predecessors": ["T08"]},
        {"id": "T10", "name": "Thảm BTN C16", "duration": 7, "predecessors": ["T09"]},
        {"id": "T11", "name": "Thử tải", "duration": 5, "predecessors": ["T10"]},
    ]

    calc = CPMCalculator()
    result = calc.calculate(tasks, start_date_str="2026-10-01")

    print(f"\n{'='*60}")
    print(f"  CPM RESULT — Cầu Km19+529.080")
    print(f"{'='*60}")
    print(f"  Tổng thời gian: {result.total_duration_days} ngày")
    print(f"  Ngày KT dự kiến: {result.project_finish}")
    print(f"  Đường găng: {' → '.join(result.critical_path)}")
    print(f"\n  {'ID':<6} {'Tên':<30} {'ES':>4} {'EF':>4} {'TF':>4} {'găng'}")
    print(f"  {'─'*56}")
    for t in result.tasks:
        star = "★" if t.is_critical else " "
        print(f"  {t.task_id:<6} {t.name:<30} {t.es:>4} {t.ef:>4} {t.tf:>4}  {star}")
