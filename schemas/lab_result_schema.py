# -*- coding: utf-8 -*-
"""
LAB RESULT SCHEMA — Quản lý phiếu thí nghiệm vật liệu & kết cấu (QA/QC Lab Link)
Ánh xạ kết quả thí nghiệm nén bê tông (R7/R28), kéo thép, siêu âm cọc, PDA
vào biên bản nghiệm thu KCS (BBNT-01 -> BBNT-22).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ConcreteCompressionTest:
    """Phiếu thí nghiệm nén mẫu bê tông (TCVN 3118:1993)."""
    test_id: str                      # Mã phiếu TN (e.g., "TN-BT-01")
    sample_code: str                  # Ký hiệu tổ mẫu (3 viên 15x15x15 cm)
    component_id: str                 # Cấu kiện đúc (e.g., "COC-T1-01", "DAM-ST-01")
    casting_date: str                 # Ngày đúc mẫu
    testing_date: str                 # Ngày nén mẫu
    age_days: int                     # Tuổi mẫu (3, 7, 14, 28 ngày)
    design_grade: str                 # Mác thiết kế (e.g., "C30", "C45/55")
    required_strength_mpa: float      # Cường độ yêu cầu theo thiết kế (MPa)
    actual_strength_mpa: float        # Cường độ nén thực tế trung bình (MPa)
    strength_ratio_pct: float         # Tỷ lệ % so với cường độ thiết kế
    status: str = "PASS"              # PASS / FAIL
    lab_name: str = "LAS-XD 188"      # Phòng thí nghiệm hợp chuẩn
    technician: str = "KS. Thí nghiệm"
    linked_bbnt: str = ""             # BBNT liên kết (e.g., "BBNT-04")
    is_hold_point_cleared: bool = False # Đã giải tỏa điểm dừng kỹ thuật chưa?


@dataclass
class RebarMillTest:
    """Chứng chỉ xuất xưởng & kết quả kéo uốn cốt thép (TCVN 1651:2018)."""
    cert_id: str                      # Số chứng chỉ / phiếu TN
    heat_number: str                  # Số lô luyện thép (Heat No.)
    rebar_diameter_mm: int            # Đường kính thép
    steel_grade: str                  # CB300-V, CB400-V, CB500-V
    yield_strength_mpa: float         # Giới hạn chảy thực tế (fy)
    tensile_strength_mpa: float       # Giới hạn bền thực tế (fu)
    elongation_pct: float             # Độ giãn dài tương đối (%)
    cold_bend_test: str = "DAT"       # Uốn nguội 180 độ
    status: str = "PASS"
    manufacturer: str = "Thép Hòa Phát / Việt Đức"
    linked_bbnt: str = ""


@dataclass
class PileIntegrityTestRecord:
    """Kết quả thí nghiệm cọc khoan nhồi (Siêu âm cọc / Nén động PDA)."""
    pile_id: str                      # Mã cọc (e.g., "COC-T1-01")
    test_type: str                    # "SONIC_LOGGING" (Siêu âm) hoặc "PDA" (Nén động)
    test_date: str
    cross_sections_tested: int = 4    # Số mặt cắt siêu âm
    integrity_category: str = "CAT_1" # Loại 1 (Đồng nhất, hoàn hảo), Loại 2, Loại 3, Loại 4
    capacity_kn: Optional[float] = None # Sức chịu tải theo PDA (kN)
    required_capacity_kn: Optional[float] = None
    status: str = "PASS"
    report_ref: str = ""
    linked_bbnt: str = ""
