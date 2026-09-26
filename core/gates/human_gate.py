# -*- coding: utf-8 -*-
"""
HUMAN-IN-THE-LOOP GATE — Cổng phê duyệt của Kỹ sư trưởng
Hiển thị cảnh báo clash/anomaly và chờ Approve/Reject trước khi
xuất tài liệu pháp lý (BBNT, Dự toán G_XD, Phụ lục 03a).

Trong production: giao diện CLI hoặc web UI để Kỹ sư trưởng nhập phán quyết.
Trong test mode: auto-approve hoặc đọc từ file config.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ApprovalRequest:
    gate_id: str
    gate_name: str
    phase: str
    document_ref: str
    clashes: List[str] = field(default_factory=list)
    anomalies: List[str] = field(default_factory=list)
    summary_data: Dict[str, Any] = field(default_factory=dict)
    requested_at: str = ""


@dataclass
class ApprovalDecision:
    gate_id: str
    approved: bool
    approver: str = "KS_TRUONG"
    comments: str = ""
    decided_at: str = ""


class HumanGate:
    """
    Cổng phê duyệt Human-in-the-Loop.

    Modes:
      - "cli"       : Hiển thị thông tin + nhập từ bàn phím (production)
      - "auto"      : Tự động approve (CI/CD, testing)
      - "file"      : Đọc phán quyết từ file JSON (batch approval)
      - "callback"  : Gọi hàm callback tùy chỉnh (tích hợp web)
    """

    def __init__(
        self,
        mode: str = "cli",
        auto_approve: bool = False,
        decisions_file: Optional[str] = None,
        callback: Optional[Callable] = None,
    ):
        self.mode = mode
        self.auto_approve = auto_approve
        self.decisions_file = decisions_file
        self.callback = callback
        self._predefined_decisions: Dict[str, bool] = {}

        if decisions_file and os.path.exists(decisions_file):
            with open(decisions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._predefined_decisions = {
                    d["gate_id"]: d.get("approved", True)
                    for d in data.get("decisions", [])
                }

    def request_approval(self, req: ApprovalRequest) -> ApprovalDecision:
        """
        Đưa ra yêu cầu phê duyệt và chờ phán quyết.
        Trả về ApprovalDecision (approved=True/False).
        """
        req.requested_at = datetime.now().isoformat(timespec="seconds")
        self._display_request(req)

        if self.mode == "auto" or self.auto_approve:
            return ApprovalDecision(
                gate_id=req.gate_id,
                approved=True,
                approver="AUTO_APPROVE",
                comments="[Auto-approved in test mode]",
                decided_at=datetime.now().isoformat(timespec="seconds"),
            )

        if self.mode == "file" and req.gate_id in self._predefined_decisions:
            approved = self._predefined_decisions[req.gate_id]
            return ApprovalDecision(
                gate_id=req.gate_id,
                approved=approved,
                approver="FILE_BATCH",
                comments=f"[Batch decision from {self.decisions_file}]",
                decided_at=datetime.now().isoformat(timespec="seconds"),
            )

        if self.mode == "callback" and self.callback:
            approved, approver, comments = self.callback(req)
            return ApprovalDecision(
                gate_id=req.gate_id,
                approved=approved,
                approver=approver,
                comments=comments,
                decided_at=datetime.now().isoformat(timespec="seconds"),
            )

        # Default: CLI mode
        return self._cli_prompt(req)

    def _display_request(self, req: ApprovalRequest) -> None:
        """In thông tin yêu cầu phê duyệt lên màn hình."""
        print("\n" + "╔" + "═" * 60 + "╗")
        print(f"║  ⏳ YÊU CẦU PHÊ DUYỆT — {req.gate_name[:38]}")
        print(f"║  Gate ID : {req.gate_id}")
        print(f"║  Phase   : {req.phase}")
        print(f"║  Tài liệu: {req.document_ref}")
        print("╠" + "═" * 60 + "╣")

        if req.summary_data:
            print("║  📊 TÓM TẮT:")
            for k, v in req.summary_data.items():
                print(f"║    {k}: {v}")

        if req.clashes:
            print(f"║  ⚠ CLASH PHÁT HIỆN ({len(req.clashes)}):")
            for c in req.clashes[:5]:
                print(f"║    → {c}")
            if len(req.clashes) > 5:
                print(f"║    ... và {len(req.clashes) - 5} clash khác")

        if req.anomalies:
            print(f"║  🔍 BẤT THƯỜNG ({len(req.anomalies)}):")
            for a in req.anomalies[:5]:
                print(f"║    → {a}")

        print("╚" + "═" * 60 + "╝")

    def _cli_prompt(self, req: ApprovalRequest) -> ApprovalDecision:
        """Nhập phán quyết từ CLI."""
        while True:
            try:
                choice = input("\n  [A] Phê duyệt (Approve)  [R] Từ chối (Reject)  [S] Bỏ qua: ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                print("\n  [HumanGate] Bị ngắt — tự động Reject để an toàn")
                choice = "R"

            if choice in ("A", "R", "S"):
                break
            print("  Vui lòng nhập A, R hoặc S")

        approved = (choice == "A")
        comments = ""
        if choice != "S":
            try:
                comments = input("  Ghi chú (Enter để bỏ qua): ").strip()
            except (EOFError, KeyboardInterrupt):
                pass
        try:
            approver = input("  Tên Kỹ sư duyệt (Enter = KS_TRUONG): ").strip() or "KS_TRUONG"
        except (EOFError, KeyboardInterrupt):
            approver = "KS_TRUONG"

        return ApprovalDecision(
            gate_id=req.gate_id,
            approved=approved,
            approver=approver,
            comments=comments or ("[Skipped]" if choice == "S" else ""),
            decided_at=datetime.now().isoformat(timespec="seconds"),
        )
