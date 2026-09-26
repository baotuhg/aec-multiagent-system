# -*- coding: utf-8 -*-
"""
CAD/BIM DIFF & VERSIONING DEMO — So sánh phiên bản Rev00 vs Rev01
Minh họa tính năng Incremental Update:
Chỉ tính toán lại các cấu kiện có biến động hình học giữa 2 lần sửa đổi bản vẽ.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from tools.cad_diff_engine import CADDiffEngine


def run_diff_demo():
    print("=" * 70)
    print("  AEC CAD/BIM VERSIONING & INCREMENTAL DIFF ENGINE")
    print("  So sánh: Bản vẽ Rev00 (Thiết kế ban đầu) vs Rev01 (Sửa đổi hiện trường)")
    print("=" * 70)

    # Snapshot Rev00: Thiết kế duyệt ban đầu
    rev00 = {
        "components": [
            {"id": "COC-T1-01", "name": "Cọc Ø1200 T1-01", "wbs": "KẾT CẤU MÓNG CỌC",
             "concrete_m3": 45.24, "formwork_m2": 0.0, "rebar_kg": 1250.0},
            {"id": "COC-T1-02", "name": "Cọc Ø1200 T1-02", "wbs": "KẾT CẤU MÓNG CỌC",
             "concrete_m3": 45.24, "formwork_m2": 0.0, "rebar_kg": 1250.0},
            {"id": "BE-T1", "name": "Bệ trụ T1", "wbs": "KẾT CẤU TRỤ CẦU",
             "concrete_m3": 112.50, "formwork_m2": 185.0, "rebar_kg": 8200.0},
            {"id": "THAN-T1", "name": "Thân đặc T1", "wbs": "KẾT CẤU TRỤ CẦU",
             "concrete_m3": 65.80, "formwork_m2": 210.0, "rebar_kg": 4100.0},
            {"id": "XA-MU-T1", "name": "Xà mũ T1", "wbs": "KẾT CẤU TRỤ CẦU",
             "concrete_m3": 28.40, "formwork_m2": 95.0, "rebar_kg": 3200.0},
            {"id": "DAM-ST-01", "name": "Dầm Super-T D1", "wbs": "KẾT CẤU NHỊP",
             "concrete_m3": 28.99, "formwork_m2": 0.0, "rebar_kg": 2100.0},
        ]
    }

    # Snapshot Rev01: Sửa đổi do Karst sâu hơn (kéo dài cọc COC-T1-01 thêm 2m)
    # và bổ sung thêm dầm ngang liên kết KCT-01
    rev01 = {
        "components": [
            {"id": "COC-T1-01", "name": "Cọc Ø1200 T1-01", "wbs": "KẾT CẤU MÓNG CỌC",
             "concrete_m3": 47.50, "formwork_m2": 0.0, "rebar_kg": 1312.0}, # Tăng 2.26 m3 BT, 62kg thép
            {"id": "COC-T1-02", "name": "Cọc Ø1200 T1-02", "wbs": "KẾT CẤU MÓNG CỌC",
             "concrete_m3": 45.24, "formwork_m2": 0.0, "rebar_kg": 1250.0}, # Không đổi
            {"id": "BE-T1", "name": "Bệ trụ T1", "wbs": "KẾT CẤU TRỤ CẦU",
             "concrete_m3": 112.50, "formwork_m2": 185.0, "rebar_kg": 8200.0}, # Không đổi
            {"id": "THAN-T1", "name": "Thân đặc T1", "wbs": "KẾT CẤU TRỤ CẦU",
             "concrete_m3": 65.80, "formwork_m2": 210.0, "rebar_kg": 4100.0}, # Không đổi
            {"id": "XA-MU-T1", "name": "Xà mũ T1", "wbs": "KẾT CẤU TRỤ CẦU",
             "concrete_m3": 28.40, "formwork_m2": 95.0, "rebar_kg": 3200.0}, # Không đổi
            {"id": "DAM-ST-01", "name": "Dầm Super-T D1", "wbs": "KẾT CẤU NHỊP",
             "concrete_m3": 28.99, "formwork_m2": 0.0, "rebar_kg": 2100.0}, # Không đổi
            # Cấu kiện mới thêm vào:
            {"id": "DAM-NGANG-KCT", "name": "Dầm ngang tăng cường KCT-01", "wbs": "KẾT CẤU NHỊP",
             "concrete_m3": 3.85, "formwork_m2": 18.5, "rebar_kg": 420.0},
        ]
    }

    engine = CADDiffEngine()
    diff_res = engine.diff(rev00, rev01, rev_from="Rev00", rev_to="Rev01")

    print(f"\n[*] Kết quả so sánh {diff_res.rev_from} -> {diff_res.rev_to}:")
    print(f"  • Tổng cấu kiện khảo sát : {diff_res.total_components_compared}")
    print(f"  • Cấu kiện giữ nguyên     : {diff_res.unchanged_count}")
    print(f"  • Cấu kiện thêm mới       : {diff_res.added_count}")
    print(f"  • Cấu kiện sửa đổi        : {diff_res.modified_count}")
    print(f"  • Cấu kiện bị xóa         : {diff_res.removed_count}")

    print(f"\n[*] Biến động khối lượng tổng hợp (Net Delta):")
    print(f"  • Bê tông  : {diff_res.net_concrete_delta_m3:+.2f} m³")
    print(f"  • Ván khuôn: {diff_res.net_formwork_delta_m2:+.2f} m²")
    print(f"  • Cốt thép : {diff_res.net_rebar_delta_kg:+.2f} kg")

    print(f"\n[*] Danh sách cấu kiện cần TÍNH TOÁN LẠI (Incremental Queue):")
    for cid in diff_res.components_to_recalculate:
        delta = next(d for d in diff_res.deltas if d.component_id == cid)
        print(f"  → [{delta.change_type}] {cid} ({delta.component_name}): "
              f"ΔBT={delta.concrete_delta_m3:+.2f}m³, ΔThép={delta.rebar_delta_kg:+.2f}kg")

    print("\n" + "=" * 70)
    print("  KẾT LUẬN: Hệ thống chỉ tính lại 2 cấu kiện biến động, tiết kiệm > 70% thời gian.")
    print("=" * 70)


if __name__ == "__main__":
    run_diff_demo()
