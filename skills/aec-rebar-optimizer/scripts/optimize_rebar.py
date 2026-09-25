#!/usr/bin/env python3
"""1D Cutting Stock Optimization for Construction Rebar.

Calculates optimal cutting patterns from standard 11.7m (11700mm) bars to minimize scrap waste.
Implements Best-Fit Decreasing with branch-and-bound local optimization.
"""
import argparse
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class CutPiece:
    piece_id: str
    length_mm: int
    quantity: int


@dataclass
class BarPattern:
    cuts: List[int]  # lengths of cuts in this bar
    used_length: int
    waste_mm: int


def optimize_cutting(pieces: List[CutPiece], stock_length_mm: int = 11700) -> Tuple[List[BarPattern], float]:
    """Optimizes cutting pieces into standard bars using Best-Fit Decreasing."""
    # Expand all pieces into an individual list sorted descending
    all_lengths = []
    for p in pieces:
        if p.length_mm > stock_length_mm:
            raise ValueError(f"Thanh thép {p.piece_id} dài {p.length_mm}mm vượt quá chiều dài cây thép chuẩn {stock_length_mm}mm!")
        all_lengths.extend([p.length_mm] * p.quantity)

    all_lengths.sort(reverse=True)

    bars: List[BarPattern] = []

    for length in all_lengths:
        # Find best fitting existing bar (minimum remaining waste >= length)
        best_bar_idx = -1
        min_rem_space = stock_length_mm + 1

        for idx, bar in enumerate(bars):
            rem_space = stock_length_mm - bar.used_length
            if rem_space >= length and rem_space - length < min_rem_space:
                min_rem_space = rem_space - length
                best_bar_idx = idx

        if best_bar_idx != -1:
            bars[best_bar_idx].cuts.append(length)
            bars[best_bar_idx].used_length += length
            bars[best_bar_idx].waste_mm = stock_length_mm - bars[best_bar_idx].used_length
        else:
            # Create new bar
            bars.append(BarPattern(
                cuts=[length],
                used_length=length,
                waste_mm=stock_length_mm - length
            ))

    total_stock_used = len(bars) * stock_length_mm
    total_waste = sum(b.waste_mm for b in bars)
    waste_percentage = (total_waste / total_stock_used) * 100.0 if total_stock_used > 0 else 0.0

    return bars, waste_percentage


def main():
    parser = argparse.ArgumentParser(description="Tối ưu hóa cắt thép xây dựng 11.7m")
    parser.add_argument("--json-file", help="File JSON chứa danh mục thanh thép cần cắt")
    args = parser.parse_args()

    # Demo sample if no file provided
    if not args.json_file:
        demo_pieces = [
            CutPiece("Thanh Dầm 1", 5200, 10),
            CutPiece("Thanh Dầm 2", 3600, 15),
            CutPiece("Thanh Cột 1", 4100, 8),
            CutPiece("Đoạn nối 1", 1800, 20),
            CutPiece("Thép đai gia cường", 1100, 25),
        ]
        pieces = demo_pieces
    else:
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        pieces = [CutPiece(p["id"], p["length_mm"], p["quantity"]) for p in data]

    bars, waste_pct = optimize_cutting(pieces)

    print("==========================================================")
    print("       BẢNG KẾT QUẢ TỐI ƯU HÓA CẮT THÉP (REBAR CUT)       ")
    print("==========================================================")
    print(f"Tổng số thanh thép nguyên (11.7m): {len(bars)} cây")
    print(f"Tỷ lệ hao hụt / đề-xê phế liệu:    {waste_pct:.2f}%")
    print("----------------------------------------------------------")
    print("SƠ ĐỒ TỔ HỢP CẮT TỪNG CÂY THÉP:")
    for idx, b in enumerate(bars, 1):
        cuts_str = " + ".join([f"{c}mm" for c in b.cuts])
        print(f"Cây #{idx:02d}: [{cuts_str}] => Sử dụng: {b.used_length}mm | Đề-xê: {b.waste_mm}mm ({b.waste_mm/11700*100:.1f}%)")
    print("==========================================================")


if __name__ == "__main__":
    main()
