#!/usr/bin/env python3
"""Calculate Cross-Section Areas and Earthwork Volumes from CAD Coordinates.

Supports:
- Polyline polygon area calculation (Shoelace formula).
- Cut & Fill area segmentation.
- Average-end-area volume calculation between consecutive chainages (Lý trình Km).
"""
import argparse
import json
import math
from typing import List, Tuple, Dict


def polygon_area(points: List[Tuple[float, float]]) -> float:
    """Calculate 2D polygon area using Shoelace formula."""
    n = len(points)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2.0


def calculate_volumes(sections: List[Dict]) -> List[Dict]:
    """Calculate volumes between successive cross-sections.

    Each section dict should contain:
    - 'chainage': float (e.g. 100.0 for Km0+100)
    - 'cut_area': float (m2)
    - 'fill_area': float (m2)
    """
    results = []
    for i in range(len(sections) - 1):
        s1 = sections[i]
        s2 = sections[i + 1]
        length = abs(s2["chainage"] - s1["chainage"])

        v_cut = ((s1["cut_area"] + s2["cut_area"]) / 2.0) * length
        v_fill = ((s1["fill_area"] + s2["fill_area"]) / 2.0) * length

        results.append({
            "from_chainage": s1["chainage"],
            "to_chainage": s2["chainage"],
            "distance": length,
            "cut_area_1": s1["cut_area"],
            "cut_area_2": s2["cut_area"],
            "volume_cut_m3": round(v_cut, 3),
            "fill_area_1": s1["fill_area"],
            "fill_area_2": s2["fill_area"],
            "volume_fill_m3": round(v_fill, 3),
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Calculate earthwork volume from cross section data")
    parser.add_argument("--json-input", help="Path to JSON file containing cross sections data")
    args = parser.parse_args()

    if args.json_input:
        with open(args.json_input, "r", encoding="utf-8") as f:
            data = json.load(f)
        sections = data.get("sections", [])
        vols = calculate_volumes(sections)
        total_cut = sum(v["volume_cut_m3"] for v in vols)
        total_fill = sum(v["volume_fill_m3"] for v in vols)

        print("=== BẢNG TÍNH KHỐI LƯỢNG ĐÀO ĐẮP MẶT CẮT NGANG ===")
        print(f"{'Từ lý trình':<12} | {'Đến lý trình':<12} | {'Cự ly (m)':<10} | {'Đào (m3)':<12} | {'Đắp (m3)':<12}")
        print("-" * 65)
        for v in vols:
            print(f"Km {v['from_chainage']:<9.1f} | Km {v['to_chainage']:<9.1f} | {v['distance']:<10.2f} | {v['volume_cut_m3']:<12.3f} | {v['volume_fill_m3']:<12.3f}")
        print("-" * 65)
        print(f"TỔNG CỘNG: Khối lượng đào = {total_cut:.3f} m3 | Khối lượng đắp = {total_fill:.3f} m3")


if __name__ == "__main__":
    main()
