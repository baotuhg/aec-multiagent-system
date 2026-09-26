# -*- coding: utf-8 -*-
"""
SITE LOG SCHEMA — Nhật ký hiện trường & Khối lượng hoàn công (As-Built)
Phục vụ vòng lặp phản hồi hiện trường (Site Feedback Loop):
  daily_site_log + as_built_quantity -> Actual vs Planned -> CPM + Phụ lục 03a
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import date


@dataclass
class SiteTaskExecution:
    """Một hạng mục công việc được thực hiện trong ca/ngày."""
    task_id: str                      # Mã công việc tương ứng trong CPM (e.g., "T04")
    wbs_code: str                     # Mã phân rã WBS (e.g., "KẾT CẤU MÓNG CỌC")
    component_id: str                 # Cấu kiện (e.g., "COC-T1-01")
    description: str                  # Diễn giải công việc
    unit: str                         # Đơn vị tính (m3, m, tấn, cọc...)
    planned_volume: float             # Khối lượng theo kế hoạch/thiết kế
    actual_volume: float              # Khối lượng thực tế thi công trong ngày
    cumulative_actual: float = 0.0    # Khối lượng lũy kế đến hiện tại
    worker_count: int = 0             # Số nhân công tham gia
    machinery_used: List[str] = field(default_factory=list) # Thiết bị sử dụng
    quality_status: str = "PASS"      # Đạt / Cần sửa / Chờ kết quả thí nghiệm
    notes: str = ""                   # Ghi chú hiện trường


@dataclass
class DailySiteLogEntry:
    """Bản ghi nhật ký thi công hiện trường hàng ngày."""
    log_id: str                       # e.g., "LOG-2026-10-15"
    log_date: str                     # YYYY-MM-DD
    weather: str = "Nắng ráo"         # Điều kiện thời tiết (ảnh hưởng bê tông/đắp đất)
    temperature_celsius: float = 28.0 # Nhiệt độ (ảnh hưởng bảo dưỡng bê tông)
    shift_count: int = 1              # Số ca làm việc
    site_engineer: str = ""           # Kỹ sư hiện trường lập nhật ký
    supervision_consultant: str = ""  # Tư vấn giám sát xác nhận
    tasks_executed: List[SiteTaskExecution] = field(default_factory=list)
    incidents_or_delays: List[str] = field(default_factory=list)
    safety_environmental_notes: str = "Đảm bảo ATLĐ và VSMT"


@dataclass
class AsBuiltVarianceItem:
    """Mục đối soát chênh lệch khối lượng thực tế so với thiết kế (Phát sinh)."""
    task_id: str
    component_id: str
    description: str
    unit: str
    contract_volume: float            # Khối lượng hợp đồng
    as_built_volume: float            # Khối lượng hoàn công thực tế
    delta_volume: float               # Chênh lệch (+: tăng, -: giảm)
    unit_price_vnd: float             # Đơn giá hợp đồng (VNĐ)
    delta_amount_vnd: float           # Giá trị phát sinh (+/- VNĐ)
    appendix_03a_category: str = "TRONG_HOP_DONG" # TRONG_HOP_DONG / PHAT_SINH_NGOAI_HD
    justification: str = ""           # Lý do phát sinh / căn cứ kỹ thuật
