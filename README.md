# 🏗️ AEC-MultiAgent-System
### Nền tảng Đa Tác tử Thông minh Tự động hóa Kỹ thuật & Quản lý Dự án Xây dựng
**Kỹ sư Trưởng Số hóa: Bóc tách Hình học • Cắt thép 1D • Tổng hợp Vật tư BOM (Sắt thép từng Ø, Xi măng, Cát, Đá) • Dự toán $G_{XD}$ • Thanh toán 03a • Tiến độ CPM MS Project • Hồ sơ KCS Word • Thuyết minh BPTC**

---

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Standards: TCVN & BXD](https://img.shields.io/badge/Standards-TCVN%20%7C%20Lu%E1%BA%ADt%20XD%20135%2F2025-brightgreen)](workflows/)
[![Zero Dead Numbers](https://img.shields.io/badge/Math-100%25%20Dynamic%20Formulas-red.svg)](workflows/01_QUY_TRINH_BOC_TACH_HINH_HOC_TAKEOFF.md)
[![1D Rebar Cutting](https://img.shields.io/badge/Rebar%20Scrap-%3C%201.5%25-success)](workflows/02_QUY_TRINH_TO_HOP_CAT_THEP_1D.md)
[![BOM Material Engine](https://img.shields.io/badge/BOM-Materials%20Breakdown%20TT12-blue)](workflows/08_QUY_TRINH_PHAN_TICH_TONG_HOP_VAT_TU_DINH_MUC.md)
[![Hugging Face RAG](https://img.shields.io/badge/RAG-BGE--M3%20%2B%20Qwen2.5-blueviolet)](workflows/07_QUY_TRINH_THUYET_MINH_BIEN_PHAP_HUGGINGFACE.md)
[![AI Platforms](https://img.shields.io/badge/Compatible-Antigravity%20%7C%20Claude%20%7C%20ChatGPT-orange)](workflows/HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md)

---

## 📖 1. Giới thiệu Tổng quan (Overview)

**AEC-MultiAgent-System** là một giải pháp mã nguồn mở tiên phong về chuyển đổi số toàn diện trong ngành Xây dựng (AEC - Architecture, Engineering & Construction) tại Việt Nam. Hệ thống tích hợp mô hình **Mạng lưới Đa tác tử Tự trị (Autonomous Multi-Agent System)** phối hợp cùng **Mô hình Ngôn ngữ Lớn (LLM)** và **Mô hình Khôi phục Dữ liệu Tăng cường (RAG)** để tự động hóa toàn bộ chuỗi sản xuất hồ sơ kỹ thuật công trình từ thiết kế đến thi công và thanh quyết toán.

Hệ thống được thiết kế tuân thủ nghiêm ngặt khung pháp lý và quy chuẩn kỹ thuật hiện hành của Nhà nước Việt Nam:
- **Luật Xây dựng số 135/2025/QH15** & **Nghị định số 207/2026/NĐ-CP**: Quy định về quản lý chất lượng thi công, giám sát và nghiệm thu hoàn thành hạng mục công trình (KCS).
- **Nghị định số 99/2021/NĐ-CP**: Quản lý, thanh toán, quyết toán dự án sử dụng vốn đầu tư công (Mẫu biểu xác định khối lượng hoàn thành Phụ lục 03a).
- **Thông tư số 11/2021/TT-BXD**: Hướng dẫn phương pháp xác định và quản lý chi phí đầu tư xây dựng (Tổng mức kinh phí xây dựng $G_{XD} = T + GT + TL + VAT$).
- **Thông tư số 12/2021/TT-BXD**: Hệ thống định mức dự toán xây dựng công trình, định mức hao phí vật tư (xi măng, cát, đá, sắt thép, cáp DƯL), định mức lao động và ca máy.
- **Thông tư số 13/2021/TT-BXD**: Phương pháp xác định chỉ tiêu kinh tế kỹ thuật và đo bóc khối lượng công trình.
- **Tiêu chuẩn thiết kế & thi công**: **TCVN 11823:2017** (Thiết kế cầu đường bộ), **TCVN 9395:2012** (Cọc khoan nhồi), **TCVN 4453:1995** (Kết cấu bê tông cốt thép toàn khối), **TCVN 1651:2018** (Thép cốt bê tông), **QCVN 18:2021/BXD** (An toàn trong thi công xây dựng).

---

## 🏛️ 2. Nguyên lý Kiến trúc Cốt lõi (Core Principles)

```
       ┌────────────────────────────────────────────────────────┐
       │             HỒ SƠ BẢN VẼ THIẾT KẾ (PDF/CAD)            │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
        ┌──────────────────────────────────────────────────────┐
        │       BLACKBOARD ARCHITECTURE (PROJECT_STATE.JSON)   │
        └───┬────────────────┬───────────────────┬──────────┬───┘
            │                │                   │          │
            ▼                ▼                   ▼          ▼
   [aec_vision_takeoff] [aec_rebar_engineer] [aec_material] [aec_cost_engineer]
   100% Công thức động  Cắt thép 11.7m <1.5% BOM Vật tư WBS Dự toán G_XD & 03a
            │                │                   │          │
            └────────────────┼───────────────────┴──────────┘
                             ▼
     ┌─────────────────────────────────────────────────────────┐
     │  TOÁN TẤT ĐỊNH (DETERMINISTIC MATH - ZERO HALLUCINATION)│
     │  • openpyxl: 9 Sheet Excel liên kết động 100%           │
     │  • python-docx: 22 Biên bản KCS & Ma trận logic ngày     │
     │  • xml.etree: MS Project 2003-2021 XML (Đường găng CPM) │
     └─────────────────────────────┬───────────────────────────┘
                                   │
                ┌──────────────────┴────────────────────┐
                ▼                                       ▼
     [aec_lead_scheduler]                  [aec_method_statement_agent]
     WBS & CPM MS Project                  RAG Hugging Face BGE-M3 + Qwen2.5
                │                                       │
                └──────────────────┬────────────────────┘
                                   ▼
                   [aec_audit_verifier (INDEPENDENT)]
                   Kiểm toán độc lập • Chấm điểm 100/100
```

1. **Tách biệt Tuyệt đối Toán Kỹ thuật Tất định & Mô hình Ngôn ngữ Sinh:**
   - **Toán kỹ thuật (Deterministic Math):** Giao cho mã nguồn Python thuần (`openpyxl`, `python-docx`, `ezdxf`, `numpy`) tính toán dựa trên công thức giải tích hình học và thuật toán tối ưu. Tuyệt đối **CẤM SỐ CHẾT (Dead Numbers)**; 100% ô tính phải là công thức động (`SUM`, `PRODUCT`, `ROUND`, `SUMIF`, `VLOOKUP`).
   - **Mô hình Ngôn ngữ (Generative AI):** Chỉ đảm nhận vai trò đọc hiểu ngữ nghĩa bản vẽ, tra cứu ngữ cảnh kỹ thuật (RAG trên TCVN/QCVN) và soạn thảo Thuyết minh Biện pháp thi công. Mô hình AI bị khóa quyền, không được tự ý can thiệp hay "bịa" (hallucinate) các con số tài chính hoặc khối lượng nghiệm thu.
2. **Kiến trúc Bảng tin Dữ liệu Tập trung (Blackboard Architecture):**
   - Mọi tác tử trao đổi dữ liệu qua một tệp trạng thái duy nhất: `PROJECT_STATE.json` (Single Source of Truth).
   - Tác tử phía sau tiêu thụ dữ liệu đầu ra đã được kiểm chứng của tác tử phía trước, đảm bảo dữ liệu xuyên suốt từ Bóc tách $\rightarrow$ Cắt thép 1D $\rightarrow$ Phân rã Vật tư BOM $\rightarrow$ Dự toán $\rightarrow$ Thanh toán $\rightarrow$ Tiến độ $\rightarrow$ KCS.
3. **Cơ chế Thẩm tra Độc lập Đóng gói (Autonomous Audit Guardrail):**
   - Tác tử thẩm tra độc lập (`aec_audit_verifier`) tự động quét toàn bộ cây công thức Excel và ma trận ngày KCS. Nếu phát hiện công thức gãy (`#REF!`, `#VALUE!`), số chết vô căn cứ hoặc biên bản bị đá ngày (nghiệm thu trước ngày thi công), tác tử sẽ hạ điểm và chặn xuất bản hồ sơ.

---

## 📁 3. Cấu trúc Thư mục Kho Mã Nguồn (Repository Layout)

```text
DONG_GOI_HETHONG_AEC/
│
├── aec_core/                     # ⚙️ LÕI XỬ LÝ PYTHON (DETERMINISTIC ENGINE)
│   ├── __init__.py               # Khởi tạo package
│   ├── audit_verifier.py         # Module thẩm tra kiểm toán độc lập 100/100 (9 Sheet)
│   └── project_state.py          # Module quản trị dữ liệu tập trung (Blackboard State)
│
├── agents/                       # 🤖 ĐẶC TẢ TÁC TỬ & ĐIỀU PHỐI MULTI-AGENT
│   ├── HE_THONG_MULTI_AGENT_AEC.md            # Thiết kế vai trò 8 tác tử chuyên gia
│   ├── QUAN_LY_DIEU_PHOI_MULTI_AGENT_AEC.md   # Cơ chế điều phối Blackboard & State
│   ├── aec_audit_verifier.py                  # Script thẩm tra độc lập
│   ├── project_state_manager.py               # Quản lý vòng đời Single Source of Truth
│   ├── rag_method_statement_huggingface.py    # Pipeline RAG Hugging Face BGE-M3 + Qwen2.5
│   └── PROJECT_STATE.json                     # Snapshot trạng thái dự án mẫu (BOM data)
│
├── workflows/                    # 📋 CHUỖI 8 QUY TRÌNH CHUẨN AEC & HƯỚNG DẪN AI
│   ├── 00_TONG_QUAN_QUY_TRINH_KHEP_KIN_AEC.md          # Bản đồ chuỗi giá trị 8 bước
│   ├── 01_QUY_TRINH_BOC_TACH_HINH_HOC_TAKEOFF.md       # Quy trình 1: Bóc tách 100% công thức sống
│   ├── 02_QUY_TRINH_TO_HOP_CAT_THEP_1D.md              # Quy trình 2: Cắt thép 11.7m (< 1.5% đề-xê)
│   ├── 03_QUY_TRINH_DU_TOAN_GXD_TT11.md                # Quy trình 4: Dự toán G_XD Thông tư 11/2021
│   ├── 04_QUY_TRINH_THANH_TOAN_PHU_LUC_03A.md          # Quy trình 5: Thanh toán 03a Nghị định 99/2021
│   ├── 05_QUY_TRINH_TIEN_DO_CPM_MS_PROJECT.md          # Quy trình 6: Tiến độ WBS & MS Project XML
│   ├── 06_QUY_TRINH_KCS_LOGIC_CHEO_XUAT_WORD.md        # Quy trình 7: KCS Word & Ma trận ngày chéo
│   ├── 07_QUY_TRINH_THUYET_MINH_BIEN_PHAP_HUGGINGFACE.md # Quy trình 8: RAG Hugging Face BPTC
│   ├── 08_QUY_TRINH_PHAN_TICH_TONG_HOP_VAT_TU_DINH_MUC.md # Quy trình 3: Phân tích & Tổng hợp Vật tư BOM
│   ├── 09_QUY_TRINH_THONG_KE_THEP_BBS_VA_TAN_SUAT_THI_NGHIEM.md # Quy trình 9: Thống kê thép chi tiết BBS & Ma trận tần suất KCS
│   └── HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md  # Sổ tay vận hành Antigravity, Claude, GPT
│
├── prompts/                      # 🧠 MASTER SYSTEM PROMPTS CHUYÊN DỤNG
│   ├── 00_PROMPT_TONG_HOP_MULTI_AGENT_AEC.md           # Prompt tổng hợp điều phối 8 tác tử
│   ├── 01_PROMPT_GIAO_THONG_CAU_DUONG.md               # Prompt chuyên sâu Cầu - Đường bộ
│   └── 02_PROMPT_DAN_DUNG_NHA_CAO_TANG.md              # Prompt chuyên sâu Nhà dân dụng cao tầng
│
├── skills/                       # 🛠️ AGY EXPERT SKILLS (CHO GOOGLE ANTIGRAVITY)
│   ├── aec-cad-automation/       # Kỹ năng CAD MCP, trích xuất hình học DWG tự động
│   ├── aec-cost-tender/          # Kỹ năng Bóc tách BoQ, Dự toán G_XD, So sánh Document Diff
│   ├── aec-qlcl/                 # Kỹ năng Nghiệm thu KCS, kiểm tra logic chéo ngày tháng
│   └── aec-rebar-optimizer/      # Kỹ năng Giải bài toán cắt thép 1 chiều (1D Cutting Stock)
│
├── templates/                    # 📦 SẢN PHẨM MẪU SỐ HÓA HOÀN THIỆN
│   ├── Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx       # Workbook 11 sheet liên kết động hoàn hảo
│   ├── Tien_Do_Thi_Cong_Cau_Km19+529.080.xml           # File MS Project XML (36 công tác, CPM)
│   ├── Tien_Do_Thi_Cong_Cau_Km19+529.080.mpp           # File Microsoft Project Native binary
│   ├── Ho_So_Bien_Ban_Nghiem_Thu_KCS_Cau_Km19+529.080.docx # Trọn bộ 22 Biên bản KCS chuẩn NĐ 207
│   ├── Thuyet_Minh_Bien_Phap_Thi_Cong_Cau_Km19+529.080.md  # Thuyết minh BPTC 8 chương TCVN
│   ├── BAO_CAO_THAM_TRA_AEC_AUDIT.md                   # Báo cáo thẩm tra độc lập Điểm 100/100 (11 sheet)
│   ├── PROJECT_STATE.json                              # Trạng thái dự án mẫu hoàn chỉnh (BOM data)
│   ├── Ho_So_KCS_QS_Cau_Khai_Hoang_2.xlsx              # File mẫu Cầu Khai Hoang 2
│   ├── Tien_Do_Thi_Cong_Cau_Khai_Hoang_2.xml           # File tiến độ Cầu Khai Hoang 2
│   ├── Ho_So_KCS_QS_TienDo_Nha_Dan_Dung.xlsx           # File mẫu Nhà Dân dụng cao tầng
│   └── Tien_Do_Thi_Cong_Dan_Dung.xml                   # File tiến độ Nhà Dân dụng cao tầng
│
├── examples/                     # 🚀 VÍ DỤ THỰC THI & SCRIPT CHẠY MẪU
│   ├── run_pipeline.py                                 # Pipeline runner kiểm tra & audit toàn bộ 11 sheet
│   ├── generate_sample_bridge_project.py               # Script tự tạo lại toàn bộ Workbook & XML Cầu
│   ├── update_material_sheets.py                       # Script phân tích & tổng hợp vật tư BOM
│   ├── add_rebar_bbs_and_mix_sheets.py                 # Script trích xuất BBS 390 thanh & Ma trận tần suất KCS
│   └── generate_kcs_word_package.py                    # Script tự xuất bộ 22 biên bản KCS Word
│
├── .gitignore                    # Bộ lọc file rác Python, OS và Office lock
├── LICENSE                       # Giấy phép bản quyền MIT
├── pyproject.toml                # Cấu hình đóng gói chuẩn PEP 621
├── requirements.txt              # Thư viện phụ thuộc chính (openpyxl, docx, ezdxf...)
└── README.md                     # Tài liệu giới thiệu chính của repository
```

---

## 🔄 4. Chuỗi Quy trình Kỹ thuật Khép kín (11 Sheet Excel Động)

| Bước / Sheet | Tên Quy trình & Tên Sheet Excel | Tác tử Phụ trách | Chuẩn Pháp lý / Kỹ thuật | Sản phẩm Đầu ra |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Bóc tách Takeoff WBS**<br>`QS_DIEN_GIAI_CHI_TIET` | `aec_vision_takeoff` | TCVN 11823:2017, TT 13/2021 | 100% công thức động Dài x Rộng x Cao x SL x Hệ số, CẤM SỐ CHẾT |
| **02** | **Tối ưu Cắt thép 1D**<br>`TO_HOP_CAT_THEP_11M7` | `aec_rebar_engineer` | TCVN 1651:2018, Cutting Stock | Tổ hợp thanh trên cây 11.7m, phôi thừa đề-xê < 1.5% |
| **03** | **Thống kê Thép Chi tiết (BBS)**<br>`THONG_KE_THEP_CHI_TIET` | `aec_rebar_engineer` | Bản vẽ CAD, TCVN 1651:2018 | Bar Bending Schedule 390 thanh thép chi tiết từng cấu kiện: Cọc D1200, Mố M1/M2, Trụ T1/T2, Dầm Super-T, Mặt cầu, Bản quá độ, Gờ lan can |
| **04** | **Cấp phối $1\text{ m}^3$ & Tần suất KCS**<br>`CAP_PHOI_1M3_VA_TAN_SUAT` | `aec_material_estimator` & `aec_qaqc_engineer` | TT 12/2021/TT-BXD, TCVN 4453, TCVN 9396, ASTM D6760 | Phân tích $1\text{ m}^3$ bê tông C10, C25, C30, C35, C40, C45 và Ma trận 809 phép thử KCS (Kéo uốn thép, nén R7/R28, siêu âm cọc, PDA) |
| **05** | **Phân rã Định mức Vật tư WBS**<br>`PHAN_TICH_VAT_TU_WBS` | `aec_material_estimator` | Thông tư 12/2021/TT-BXD | Chi tiết xi măng, cát, đá, sắt thép từng loại $\varnothing$, cáp DƯL liên kết công thức động từ Sheet QS |
| **06** | **Tổng hợp Vật tư Toàn cầu (BOM)**<br>`TONG_HOP_VAT_TU_TOAN_BO` | `aec_material_estimator` | TT 12/2021, Chuỗi cung ứng | BOM toàn cầu, tính hao hụt thi công và Kế hoạch cấp hàng theo 4 giai đoạn |
| **07** | **Dự toán $G_{XD}$**<br>`TONG_HOP_DU_TOAN_GXD` | `aec_cost_engineer` | TT 11/2021/TT-BXD, TT 13/2021 | $G_{XD} = T + GT(7.3\%) + TL(5.5\%) + VAT(8\%)$ |
| **08** | **Thanh toán Kỳ 03a**<br>`THANH_TOAN_KY_PHU_LUC_03A` | `aec_cost_engineer` | Nghị định 99/2021/NĐ-CP | Lũy kế thực hiện, giữ lại bảo hành 5% theo hợp đồng |
| **09** | **Tiến độ CPM & Gantt**<br>`TIEN_DO_THI_CONG_WBS` | `aec_lead_scheduler` | TT 12/2021/TT-BXD, CPM Method | Sheet `TIEN_DO_THI_CONG_WBS` + Tệp `MS Project (.xml/.mpp)` (Critical Path, 36 tasks) |
| **10** | **Hồ sơ KCS Word**<br>`HOSO_KCS_NGHIEM_THU` | `aec_qaqc_engineer` | Nghị định 207/2026/NĐ-CP | File Word `.docx` (22 Biên bản nghiệm thu KCS + Ma trận kiểm tra logic ngày chéo) |
| **11** | **Thuyết minh BPTC & Audit**<br>`BAO_CAO_THAM_TRA_AEC_AUDIT` | `aec_method_statement_agent` & `aec_audit_verifier` | RAG Hugging Face BGE-M3 + Qwen2.5 | File Thuyết minh BPTC 8 chương + Báo cáo thẩm tra độc lập Audit Score 100/100 |

---

## ⚡ 5. Cài đặt & Bắt đầu Nhanh (Quickstart)

```bash
# 1. Clone kho lưu trữ
git clone https://github.com/baotuhg/aec-multiagent-system.git
cd aec-multiagent-system

# 2. Cài đặt các gói phụ thuộc Python
pip install -r requirements.txt

# 3. Chạy chuỗi kiểm toán độc lập trên Workbook 11 Sheet (Audit Score 100/100)
python examples/run_pipeline.py

# 4. Trích xuất Bar Bending Schedule (BBS) và Ma trận tần suất KCS
python examples/add_rebar_bbs_and_mix_sheets.py

# 5. Xuất trọn bộ 22 Biên bản nghiệm thu KCS có ma trận logic ngày ra tệp Word (.docx)
python examples/generate_kcs_word_package.py
```
```

---

## 🏆 6. Chi tiết 9 Sheet Bảng tính Mẫu Hoàn thiện (Templates Deliverables)

Tệp Excel Master: **[`templates/Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx`](templates/Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx)** gồm **9 Sheet** liên thông 100% công thức động:

1. **`TO_HOP_CAT_THEP_11M7`**: Tổ hợp cắt thép thanh 11.7m theo bài toán 1D Cutting Stock, đề-xê hao hụt đạt **1.44%** (< 1.5%).
2. **`KHOI_LUONG_DAO_DAP`**: Thể tích đào đắp trắc ngang $V = \frac{F_1 + F_2}{2} \times L$.
3. **`QS_DIEN_GIAI_CHI_TIET`**: Bóc tách hình học 100% công thức động Dài x Rộng x Cao x Số lượng x Hệ số, CẤM SỐ CHẾT.
4. **`TONG_HOP_DU_TOAN_GXD`**: Tổng hợp kinh phí xây dựng Thông tư 11/2021/TT-BXD ($G_{XD} = 15.352$ tỷ VNĐ).
5. **`THANH_TOAN_KY_PHU_LUC_03A`**: Bảng xác định giá trị khối lượng công việc hoàn thành đề nghị thanh toán theo Nghị định 99/2021/NĐ-CP.
6. **`TIEN_DO_THI_CONG_WBS`**: 36 công tác WBS, định mức nhân công TT 12/2021, biểu đồ Gantt Chart CPM.
7. **`HOSO_KCS_NGHIEM_THU`**: 22 Biên bản nghiệm thu KCS theo Nghị định 207/2026/NĐ-CP đồng bộ ngày tháng.
8. **`PHAN_TICH_VAT_TU_WBS`** *(MỚI)*: Phân tích định mức chi tiết vật liệu cấu thành cho từng hạng mục công tác WBS theo Thông tư 12/2021/TT-BXD (Xi măng, cát, đá, sắt thép từng loại $\varnothing$, cáp DƯL, gối chậu, khe co giãn...).
9. **`TONG_HOP_VAT_TU_TOAN_BO`** *(MỚI)*: Bảng tổng hợp toàn bộ nhu cầu vật liệu toàn công trình (BOM) bằng công thức `=SUMIF` động, tính khối lượng cung ứng có hệ số hao hụt thi công và phân bổ theo 4 giai đoạn cấp hàng công trường.

---

## ⚖️ 7. Giấy phép Bản quyền (License)

Dự án được phân phối dưới giấy phép mã nguồn mở **[MIT License](LICENSE)**.

*Hệ thống được nghiên cứu, phát triển và đóng gói bởi Cộng đồng Kỹ sư Xây dựng Số hóa Việt Nam.*
