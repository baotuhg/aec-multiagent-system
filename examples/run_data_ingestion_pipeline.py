# -*- coding: utf-8 -*-
"""
VÍ DỤ THỰC THI CHUỖI TÁC TỬ THU NHẬN & HỢP NHẤT DỮ LIỆU ĐA PHƯƠNG THỨC
(MULTI-MODAL DATA INGESTION & FUSION PIPELINE)

Quy trình phối hợp 4 Agent:
1. aec_cad_extractor: Đọc bản vẽ AutoCAD DWG (cọc, mố, trụ, dầm Super-T).
2. aec_office_extractor: Bóc tách bảng tính Excel & Word (BBS, BoQ, KCS).
3. aec_markdown_ingestor: Phân tích thuyết minh thiết kế và quy chuẩn kỹ thuật Markdown.
4. aec_data_aggregator: Đối chiếu chéo (Cross-check), làm sạch và xuất Blackboard State chuẩn.
"""

import os
import sys

# Thêm đường dẫn gốc vào sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from agents.aec_cad_extractor import AECCadExtractor
from agents.aec_office_extractor import AECOfficeExtractor
from agents.aec_markdown_ingestor import AECMarkdownIngestor
from agents.aec_data_aggregator import AECDataAggregator

def main():
    print("=" * 75)
    print("  AEC MULTI-MODAL DATA INGESTION & RECONCILIATION PIPELINE")
    print("  Kiến trúc: Ingestion Cluster (CAD + Office + MD) -> Data Aggregator -> Blackboard")
    print("=" * 75)

    cad_agent = AECCadExtractor()
    office_agent = AECOfficeExtractor()
    md_agent = AECMarkdownIngestor()
    aggregator = AECDataAggregator()

    # Đường dẫn thư mục hồ sơ thiết kế
    design_base = r"c:\Users\baotu\Downloads\Documents\HSTK Cầu Km19+529.080_Marker\HSTK Cầu Km19+529.080_Marker\01.CAU KM19+529.08"
    md_file = r"c:\Users\baotu\Downloads\Documents\HSTK Cầu Km19+529.080_Marker\PHAN_TICH_KHOI_LUONG_QS_CAU_KM19+529.080.md"
    excel_file = os.path.join(design_base, r"06. QUANTITY\06.THKL_KM19.5.xlsx")
    cad_file = os.path.join(design_base, r"02. SUP\SUPER T 38.2\04. COT THEP DAM.dwg")

    print("\n--- BƯỚC 1: TÁC TỬ AEC_CAD_EXTRACTOR QUÉT BẢN VẼ CAD ---")
    if os.path.exists(cad_file):
        cad_res = cad_agent.process_drawing(cad_file)
        print(f"  -> Nhận diện cấu kiện CAD: {cad_res.get('structure_type')}")
        print(f"  -> Thông số: {cad_res.get('summary_quantities')}")
    else:
        cad_res = {"status": "MOCK", "structure_type": "DẦM SUPER-T", "summary_quantities": {"span_length_m": 38.2}}

    print("\n--- BƯỚC 2: TÁC TỬ AEC_OFFICE_EXTRACTOR BÓC TÁCH BẢNG TÍNH EXCEL ---")
    if os.path.exists(excel_file):
        wb_res = office_agent.process_workbook(excel_file)
        print(f"  -> Tổng số sheet trong tệp Excel: {wb_res.get('sheets_count')}")
        print(f"  -> Phân loại nội dung: {wb_res.get('detected_types')[:3]}...")
    else:
        wb_res = {}

    print("\n--- BƯỚC 3: TÁC TỬ AEC_MARKDOWN_INGESTOR ĐỌC HỒ SƠ THUYẾT MINH ---")
    if os.path.exists(md_file):
        md_res = md_agent.process_file(md_file)
        print(f"  -> Dung lượng văn bản: {md_res.get('file_size_chars')} ký tự, {md_res.get('tables_count')} bảng")
        print(f"  -> Mác bê tông phát hiện: {md_res.get('technical_specs', {}).get('concrete_grades')}")
        print(f"  -> Mác thép phát hiện: {md_res.get('technical_specs', {}).get('steel_grades')}")
    else:
        md_res = {}

    print("\n--- BƯỚC 4: TÁC TỬ AEC_DATA_AGGREGATOR ĐỐI CHIẾU CHÉO & HỢP NHẤT ---")
    discrepancies = aggregator.reconcile_sources(cad_res, wb_res, md_res)
    print(f"  -> Số điểm xung đột phát hiện: {len(discrepancies)}")

    target_state = os.path.join(root_dir, "templates", "PROJECT_STATE.json")
    state = aggregator.synthesize_to_project_state(design_base, target_state)
    print(f"  -> Đã tổng hợp thành công Single Source of Truth:")
    print(f"     * Thống kê thép BBS: {state['detailed_rebar_bbs_summary']['total_rebar_marks_count']} số hiệu thanh ({state['detailed_rebar_bbs_summary']['total_steel_and_cable_tons']:.3f} tấn)")
    print(f"     * Bê tông các loại: {state['concrete_mix_design_summary']['total_concrete_volume_m3']:.3f} m3 ({state['concrete_mix_design_summary']['total_cement_pcb40_tons']:.2f} tấn Xi măng)")
    print(f"     * Ma trận tần suất KCS: {state['qaqc_testing_frequency_summary']['total_mandatory_tests_and_samples']} tổ mẫu kiểm tra bắt buộc")

    print("\n" + "=" * 75)
    print("  [V] HOÀN TẤT THU NHẬN & HỢP NHẤT DỮ LIỆU. SẴN SÀNG CHUYỂN BƯỚC NGHIỆP VỤ!")
    print("=" * 75)

if __name__ == "__main__":
    main()
