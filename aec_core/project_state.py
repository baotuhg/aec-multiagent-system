# -*- coding: utf-8 -*-
"""
PROJECT STATE MANAGER
Bộ quản lý trạng thái dự án (Single Source of Truth)
"""

import os
import json

class ProjectStateManager:
    def __init__(self, state_file_path=None):
        if state_file_path is None:
            self.state_file_path = os.path.join(os.path.dirname(__file__), "..", "agents", "PROJECT_STATE.json")
        else:
            self.state_file_path = state_file_path
        self.state = self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file_path):
            try:
                with open(self.state_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Lỗi đọc state: {e}. Tạo mới.")
        return {}

    def save_state(self, state_data=None):
        if state_data is not None:
            self.state = state_data
        os.makedirs(os.path.dirname(os.path.abspath(self.state_file_path)), exist_ok=True)
        with open(self.state_file_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
        print(f"[*] Đã lưu trạng thái dự án: {self.state_file_path}")
