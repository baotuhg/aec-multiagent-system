# -*- coding: utf-8 -*-
"""
AEC Master Core Engine
Hệ thống lõi tự động hóa tính toán Kỹ thuật, Dự toán, Tiến độ và Pháp lý Xây dựng.
Tuân thủ Luật Xây dựng 135/2025/QH15, NĐ 207/2026/NĐ-CP, NĐ 99/2021/NĐ-CP & TT 11/2021/TT-BXD.
"""

from .audit_verifier import AECAuditVerifier
from .project_state import ProjectStateManager

__version__ = "2.0.0"
__all__ = ["AECAuditVerifier", "ProjectStateManager"]
