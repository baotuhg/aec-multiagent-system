# -*- coding: utf-8 -*-
"""
CAD DIFF ENGINE — So sánh phiên bản bản vẽ (Rev01 vs Rev02)
Incremental Update: chỉ tính lại cấu kiện có biến động

Input:  snapshot_v1 (dict), snapshot_v2 (dict) — từ CAD Agent
Output: CADDiffResult với danh sách thay đổi và delta khối lượng
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ComponentDelta:
    """Sự thay đổi của một cấu kiện giữa 2 bản vẽ."""
    component_id: str
    component_name: str
    wbs: str
    change_type: str                # ADDED / REMOVED / MODIFIED
    # Volume deltas
    concrete_delta_m3: float = 0.0
    formwork_delta_m2: float = 0.0
    rebar_delta_kg: float = 0.0
    # Cũ vs mới
    old_values: Dict[str, Any] = field(default_factory=dict)
    new_values: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CADDiffResult:
    rev_from: str = ""
    rev_to: str = ""
    total_components_compared: int = 0
    unchanged_count: int = 0
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    deltas: List[ComponentDelta] = field(default_factory=list)
    # Tổng biến động khối lượng
    net_concrete_delta_m3: float = 0.0
    net_formwork_delta_m2: float = 0.0
    net_rebar_delta_kg: float = 0.0
    # Danh sách component cần tính lại
    components_to_recalculate: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class CADDiffEngine:
    """
    So sánh 2 snapshot bản vẽ CAD và trả về danh sách cấu kiện biến động.
    Chỉ cấu kiện có biến động mới được đưa vào vòng tính lại.
    """

    TOLERANCE_M3 = 0.001   # 1 lít — dưới ngưỡng này coi như không đổi
    TOLERANCE_M2 = 0.01    # 0.01 m² 
    TOLERANCE_KG = 0.1     # 0.1 kg

    def diff(
        self,
        snapshot_v1: Dict[str, Any],
        snapshot_v2: Dict[str, Any],
        rev_from: str = "Rev00",
        rev_to: str = "Rev01",
    ) -> CADDiffResult:
        """
        snapshot format:
        {
          "components": [
            {"id": "COC-T1-01", "name": "Cọc Ø1200 T1-01", "wbs": "KẾT CẤU MÓNG CỌC",
             "concrete_m3": 45.24, "formwork_m2": 0.0, "rebar_kg": 1250.0}, ...
          ]
        }
        """
        result = CADDiffResult(rev_from=rev_from, rev_to=rev_to)

        comps_v1: Dict[str, Dict] = {
            c["id"]: c for c in snapshot_v1.get("components", [])
        }
        comps_v2: Dict[str, Dict] = {
            c["id"]: c for c in snapshot_v2.get("components", [])
        }

        all_ids = set(comps_v1.keys()) | set(comps_v2.keys())
        result.total_components_compared = len(all_ids)

        for cid in sorted(all_ids):
            v1 = comps_v1.get(cid)
            v2 = comps_v2.get(cid)

            if v1 is None:
                # ADDED in v2
                delta = ComponentDelta(
                    component_id=cid,
                    component_name=v2.get("name", cid),
                    wbs=v2.get("wbs", ""),
                    change_type="ADDED",
                    concrete_delta_m3=v2.get("concrete_m3", 0),
                    formwork_delta_m2=v2.get("formwork_m2", 0),
                    rebar_delta_kg=v2.get("rebar_kg", 0),
                    new_values=v2,
                )
                result.deltas.append(delta)
                result.added_count += 1
                result.components_to_recalculate.append(cid)

            elif v2 is None:
                # REMOVED in v2
                delta = ComponentDelta(
                    component_id=cid,
                    component_name=v1.get("name", cid),
                    wbs=v1.get("wbs", ""),
                    change_type="REMOVED",
                    concrete_delta_m3=-v1.get("concrete_m3", 0),
                    formwork_delta_m2=-v1.get("formwork_m2", 0),
                    rebar_delta_kg=-v1.get("rebar_kg", 0),
                    old_values=v1,
                )
                result.deltas.append(delta)
                result.removed_count += 1
                result.components_to_recalculate.append(cid)

            else:
                # Compare values
                dc = v2.get("concrete_m3", 0) - v1.get("concrete_m3", 0)
                df = v2.get("formwork_m2", 0) - v1.get("formwork_m2", 0)
                dr = v2.get("rebar_kg", 0) - v1.get("rebar_kg", 0)

                if (abs(dc) > self.TOLERANCE_M3 or
                        abs(df) > self.TOLERANCE_M2 or
                        abs(dr) > self.TOLERANCE_KG):
                    delta = ComponentDelta(
                        component_id=cid,
                        component_name=v2.get("name", cid),
                        wbs=v2.get("wbs", ""),
                        change_type="MODIFIED",
                        concrete_delta_m3=dc,
                        formwork_delta_m2=df,
                        rebar_delta_kg=dr,
                        old_values=v1,
                        new_values=v2,
                    )
                    result.deltas.append(delta)
                    result.modified_count += 1
                    result.components_to_recalculate.append(cid)
                else:
                    result.unchanged_count += 1

        # Tính tổng delta
        result.net_concrete_delta_m3 = sum(d.concrete_delta_m3 for d in result.deltas)
        result.net_formwork_delta_m2 = sum(d.formwork_delta_m2 for d in result.deltas)
        result.net_rebar_delta_kg = sum(d.rebar_delta_kg for d in result.deltas)

        return result
