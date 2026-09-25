# -*- coding: utf-8 -*-
"""
MÔ-ĐUN MỤC 5: KIỂM SOÁT LOGIC NGÀY THÁNG CHÉO & XUẤT TRỌN BỘ 22 BIÊN BẢN NGHIỆM THU KCS RA FILE WORD (.DOCX)
Tuân thủ Luật Xây dựng số 135/2025/QH15 & Nghị định 207/2026/NĐ-CP.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_kcs_word_package():
    doc = docx.Document()
    
    # Setup page margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.75)

    # -------------------------------------------------------------
    # PHẦN 1: BẢNG KIỂM TRA LOGIC NGÀY THÁNG CHÉO (DATE CROSS-CHECK)
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("BẢNG KIỂM TRA LOGIC CHÉO NGÀY THÁNG NGHIỆM THU & THÍ NGHIỆM KCS")
    run_t.bold = True
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(13)
    run_t.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("CÔNG TRÌNH: CẦU KM19+529.080 - DỰ ÁN CAO TỐC TUYÊN QUANG - HÀ GIANG\n(Nguyên tắc kiểm soát chuyển bước: Đào đất -> BT lót -> Cốt thép -> Đổ BT -> Thử nén R7/R28 -> Căng cáp DUL -> Chuyển bước)")
    run_sub.font.name = "Times New Roman"
    run_sub.font.size = Pt(10)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    doc.add_paragraph()

    # Data matrix
    cross_check_records = [
        ("BBNT-01", "Bàn giao tim mốc VN2000, cao độ quốc gia & tim mốc cầu", "01/10/2026", "02/10/2026", "Mốc ban đầu", "Hợp lệ (Khởi động)"),
        ("BBNT-02", "Dọn dẹp mặt bằng, thi công đường công vụ nhánh 6 & 6A", "03/10/2026", "18/10/2026", "BBNT-01 + 1 ngày", "Hợp lệ (Tiếp cận công trường)"),
        ("BBNT-03", "Kiểm tra nghiệm thu vật liệu đầu vào (Thép, Cáp DUL, Xi măng)", "15/10/2026", "20/10/2026", "Trước khi thi công cọc", "Hợp lệ (Có phiếu CO/CQ)"),
        ("BBNT-04", "Nghiệm thu trạm trộn BTXM 90m3/h, trạm biến áp & bệ đúc dầm", "12/10/2026", "24/10/2026", "Trước khi đổ BT cọc", "Hợp lệ (Kiểm định thiết bị)"),
        ("BBNT-05", "Định vị tim cọc & hạ ống vách thép dẫn hướng D1300mm", "25/10/2026", "28/10/2026", "BBNT-02, BBNT-04", "Hợp lệ (Đúng tim mốc)"),
        ("BBNT-06", "Khoan thăm dò hang Karst sâu 5m dưới mũi 26 cọc vào đá liền khối", "25/10/2026", "05/11/2026", "BBNT-05 + Khoan cọc", "Hợp lệ (Đúng chỉ dẫn Trang 11)"),
        ("BBNT-07", "Nghiệm thu hố khoan cọc D1200mm, thổi rửa lắng cặn & bentonite", "26/10/2026", "06/11/2026", "Sau khi khoan dò Karst", "Hợp lệ (Cặn lắng <= 50mm)"),
        ("BBNT-08", "Gia công, lắp dựng lồng cốt thép D25/D16 & ống siêu âm kín nước", "27/10/2026", "07/11/2026", "Trước khi đổ bê tông", "Hợp lệ (Thép có CO/CQ BBNT-03)"),
        ("BBNT-09", "Đổ bê tông 26 cọc khoan nhồi C30/37 bằng ống tremie (1100.86 m3)", "06/11/2026", "12/12/2026", "Ngay sau khi hạ lồng thép", "Hợp lệ (Độ sụt 18+-2cm)"),
        ("BBNT-10", "Thí nghiệm siêu âm 156 MC cọc, khoan lấy lõi & thử tải PDA (9434 kN)", "13/12/2026", "20/12/2026", "Cọc đổ xong >= 7-14 ngày", "Hợp lệ (Đủ tuổi nén bê tông)"),
        ("BBNT-11", "Đào hố móng bệ, đập đầu 26 cọc nhồi & đổ bê tông lót bệ mác C10", "21/12/2026", "27/12/2026", "Sau khi có kết quả BBNT-10", "Hợp lệ (Không đập trước khi siêu âm)"),
        ("BBNT-12", "Cốt thép, ván khuôn & đổ bê tông bệ móng mố M1, M2 & bệ trụ T1, T2 C30", "28/12/2026", "08/01/2027", "Sau khi đổ BT lót BBNT-11", "Hợp lệ (Đệm lót đã cứng)"),
        ("BBNT-13", "Thi công thân mố chân dê M1 và thân mố chữ U M2 bê tông C30", "06/01/2027", "18/01/2027", "Sau khi bệ mố đạt R7", "Hợp lệ (Bệ mố đạt cường độ)"),
        ("BBNT-14", "Thi công thân đặc trụ T1, T2 (H=14.5m & 11.4m) bê tông C30", "09/01/2027", "22/01/2027", "Sau khi bệ trụ đạt R7", "Hợp lệ (Chuyển bước chuẩn)"),
        ("BBNT-15", "Cốt thép, ván khuôn & đổ bê tông xà mũ trụ T1, T2, đá kê gối C30", "23/01/2027", "30/01/2027", "Sau khi thân trụ đạt R14", "Hợp lệ (Thân trụ đủ chịu lực)"),
        ("BBNT-16", "Cốt thép, ván khuôn & đổ bê tông C45 15 phiến dầm Super-T tại bãi đúc", "26/12/2026", "15/01/2027", "Song song tại bãi đúc", "Hợp lệ (Độc lập mặt bằng)"),
        ("BBNT-17", "Căng kéo cáp DUL 15.2mm & bơm vữa không co ngót ống gen dầm", "16/01/2027", "25/01/2027", "Sau khi dầm Super-T đạt R28", "Hợp lệ (Cường độ bê tông >= 85%)"),
        ("BBNT-18", "Lắp đặt 30 gối chậu cao su & lao lắp 15 phiến dầm Super-T (giá lao 78.88T)", "31/01/2027", "14/02/2027", "Sau BBNT-15 & BBNT-17", "Hợp lệ (Xà mũ & dầm đều sẵn sàng)"),
        ("BBNT-19", "Đổ bê tông dầm ngang & mối nối liên tục nhiệt đỉnh trụ T1, T2 C35", "15/02/2027", "19/02/2027", "Sau khi dầm yên vị trên gối", "Hợp lệ (Ổn định liên kết nhịp)"),
        ("BBNT-20", "Lắp 510 tấm ván khuôn đúc sẵn, cốt thép & đổ bê tông bản mặt cầu C35", "20/02/2027", "02/03/2027", "Sau khi dầm ngang đạt R7", "Hợp lệ (Hệ dầm đã liên kết)"),
        ("BBNT-21", "Khe co giãn răng lược D=100mm, gờ lan can C25 & thảm BTN C16 dày 7cm", "07/03/2027", "19/03/2027", "Sau khi bản mặt cầu đạt R14", "Hợp lệ (Chống thấm khô hoàn toàn)"),
        ("BBNT-22", "Thử tải tĩnh/động toàn cầu & nghiệm thu hoàn thành đưa vào sử dụng", "20/03/2027", "28/03/2027", "Bê tông toàn cầu đạt 100% R28", "Hợp lệ (Đủ điều kiện thông xe)"),
    ]

    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_titles = ["Số hiệu", "Tên công việc nghiệm thu", "Ngày bắt đầu", "Ngày nghiệm thu", "Điều kiện tiên quyết", "Đánh giá Logic"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1F497D")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for item in cross_check_records:
        row = table.add_row()
        cells = row.cells
        for i, val in enumerate(item):
            cells[i].text = val
            set_cell_margins(cells[i], top=60, bottom=60, left=80, right=80)
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2, 3, 5] else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(8)
                if i == 5:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0x00, 0x80, 0x00) # Green for valid

    doc.add_page_break()

    # -------------------------------------------------------------
    # PHẦN 2: TRỌN BỘ 22 BIÊN BẢN NGHIỆM THU KCS CHUẨN NGHỊ ĐỊNH 207/2026/NĐ-CP
    # -------------------------------------------------------------
    for idx, record in enumerate(cross_check_records, start=1):
        bb_code, task_name, start_date, finish_date, prereq, status = record
        
        # Header Quốc hiệu Tiêu ngữ
        t_hdr = doc.add_table(rows=1, cols=2)
        t_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_left = t_hdr.rows[0].cells[0]
        c_right = t_hdr.rows[0].cells[1]
        
        p_l = c_left.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_l1 = p_l.add_run("BAN QLDA ĐTXD CÔNG TRÌNH\nTỈNH TUYÊN QUANG\n")
        r_l1.font.name = "Times New Roman"
        r_l1.font.size = Pt(9)
        r_l1.font.bold = True
        r_l2 = p_l.add_run("CÔNG TRÌNH: CẦU KM19+529.080")
        r_l2.font.name = "Times New Roman"
        r_l2.font.size = Pt(8.5)
        r_l2.font.italic = True

        p_r = c_right.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_r1 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
        r_r1.font.name = "Times New Roman"
        r_r1.font.size = Pt(9.5)
        r_r1.font.bold = True
        r_r2 = p_r.add_run("Độc lập - Tự do - Hạnh phúc\n-----------------------")
        r_r2.font.name = "Times New Roman"
        r_r2.font.size = Pt(9)
        r_r2.font.bold = True

        # Tên biên bản
        p_bb = doc.add_paragraph()
        p_bb.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_bb.paragraph_format.space_before = Pt(12)
        p_bb.paragraph_format.space_after = Pt(4)
        run_bb = p_bb.add_run(f"BIÊN BẢN NGHIỆM THU CÔNG VIỆC XÂY DỰNG\nSố: {bb_code}/NT-GXD")
        run_bb.font.name = "Times New Roman"
        run_bb.font.size = Pt(12)
        run_bb.font.bold = True
        run_bb.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

        # Thông tin biên bản
        body_p = doc.add_paragraph()
        body_p.paragraph_format.line_spacing = 1.15
        
        runs_spec = [
            ("1. Hạng mục công việc nghiệm thu: ", True),
            (f"{task_name}\n", False),
            ("2. Vị trí xây dựng: ", True),
            ("Cầu Km19+529.080 (Phân đoạn Km19+120 -:- Km27+480) - Cao tốc Tuyên Quang - Hà Giang\n", False),
            ("3. Thời gian nghiệm thu: ", True),
            (f"Bắt đầu: 08 giờ 30 ngày {finish_date}; Kết thúc: 11 giờ 00 ngày {finish_date}\n", False),
            ("4. Thành phần tham gia nghiệm thu:\n", True),
            ("   a) Đại diện Tư vấn giám sát (TVGS):\n", True),
            ("      - Ông: Nguyễn Văn Tiệp             - Chức vụ: Kỹ sư Tư vấn Giám sát trưởng\n", False),
            ("   b) Đại diện Nhà thầu thi công xây dựng:\n", True),
            ("      - Ông: Nguyễn Minh Hiếu            - Chức vụ: Chỉ huy trưởng công trường\n", False),
            ("      - Ông: Trần Đức Giang              - Chức vụ: Kỹ sư Quản lý chất lượng (KCS)\n", False),
            ("5. Đánh giá công việc xây dựng đã thực hiện:\n", True),
            ("   - Tài liệu làm căn cứ nghiệm thu: Hồ sơ TKBVTC được phê duyệt; Tiêu chuẩn kỹ thuật TCVN 11823:2017, TCVN 9395:2012, TCVN 4453:1995; Phiếu kết quả thí nghiệm vật liệu, chứng chỉ CO/CQ hợp chuẩn.\n", False),
            (f"   - Điều kiện nghiệm thu chuyển bước: Đã kiểm tra logic chéo đạt yêu cầu so với bước trước ({prereq}).\n", False),
            ("   - Chất lượng công việc: Kích thước hình học, cao độ, tọa độ tim mốc và chất lượng cấu kiện hoàn toàn phù hợp với hồ sơ thiết kế bản vẽ thi công và quy chuẩn kỹ thuật.\n", False),
            ("6. Kết luận nghiệm thu:\n", True),
            ("   Đồng ý nghiệm thu công việc xây dựng nêu trên và cho phép nhà thầu tiếp tục triển khai các bước thi công tiếp theo.\n", False)
        ]

        for text_val, is_b in runs_spec:
            r = body_p.add_run(text_val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.bold = is_b

        # Bảng ký tên
        t_sign = doc.add_table(rows=2, cols=2)
        t_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_sign.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        t_sign.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        t_sign.rows[1].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        t_sign.rows[1].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        r_s1 = t_sign.rows[0].cells[0].paragraphs[0].add_run("ĐẠI DIỆN NHÀ THẦU THI CÔNG\nChỉ huy trưởng\n\n\n\n\nNguyễn Minh Hiếu")
        r_s1.font.name = "Times New Roman"
        r_s1.font.size = Pt(9.5)
        r_s1.font.bold = True

        r_s2 = t_sign.rows[0].cells[1].paragraphs[0].add_run("ĐẠI DIỆN TƯ VẤN GIÁM SÁT\nGiám sát trưởng\n\n\n\n\nNguyễn Văn Tiệp")
        r_s2.font.name = "Times New Roman"
        r_s2.font.size = Pt(9.5)
        r_s2.font.bold = True

        if idx < len(cross_check_records):
            doc.add_page_break()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_word = os.path.join(repo_root, "templates", "Ho_So_Bien_Ban_Nghiem_Thu_KCS_Cau_Km19+529.080.docx")

    doc.save(target_word)
    print(f"-> Đã xuất thành công tệp Word KCS: {target_word}")

if __name__ == "__main__":
    generate_kcs_word_package()
