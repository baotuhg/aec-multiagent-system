# 🏗️ AEC-MultiAgent-System
### Nền tảng Đa Tác tử Thông minh Tự động hóa Kỹ thuật & Quản lý Dự án Xây dựng
**Kỹ sư Trưởng Số hóa: Bóc tách Hình học • Tối ưu Thép 1D • Dự toán $G_{XD}$ • Thanh toán 03a • Tiến độ CPM MS Project • Hồ sơ KCS Word • Thuyết minh BPTC**

---

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Standards: TCVN & BXD](https://img.shields.io/badge/Standards-TCVN%20%7C%20Lu%E1%BA%ADt%20XD%20135%2F2025-brightgreen)](workflows/)
[![Zero Dead Numbers](https://img.shields.io/badge/Math-100%25%20Dynamic%20Formulas-red.svg)](workflows/01_QUY_TRINH_BOC_TACH_HINH_HOC_TAKEOFF.md)
[![1D Rebar Cutting](https://img.shields.io/badge/Rebar%20Scrap-%3C%201.5%25-success)](workflows/02_QUY_TRINH_TO_HOP_CAT_THEP_1D.md)
[![Hugging Face RAG](https://img.shields.io/badge/RAG-BGE--M3%20%2B%20Qwen2.5-blueviolet)](workflows/07_QUY_TRINH_THUYET_MINH_BIEN_PHAP_HUGGINGFACE.md)
[![AI Platforms](https://img.shields.io/badge/Compatible-Antigravity%20%7C%20Claude%20%7C%20ChatGPT-orange)](workflows/HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md)

---

## 📖 1. Giới thiệu Tổng quan (Overview)

**AEC-MultiAgent-System** là một giải pháp mã nguồn mở tiên phong về chuyển đổi số toàn diện trong ngành Xây dựng (AEC - Architecture, Engineering & Construction) tại Việt Nam. Hệ thống tích hợp mô hình **Mạng lưới Đa tác tử Tự trị (Autonomous Multi-Agent System)** phối hợp cùng **Mô hình Ngôn ngữ Lớn (LLM)** và **Mô hình Khôi phục Dữ liệu Tăng cường (RAG)** để tự động hóa toàn bộ chuỗi sản xuất hồ sơ kỹ thuật công trình từ thiết kế đến thi công và thanh quyết toán.

Hệ thống được thiết kế tuân thủ nghiêm ngặt khung pháp lý và quy chuẩn kỹ thuật hiện hành của Nhà nước Việt Nam:
- **Luật Xây dựng số 135/2025/QH15** & **Nghị định số 207/2026/NĐ-CP**: Quy định về quản lý chất lượng thi công, giám sát và nghiệm thu hoàn thành hạng mục công trình (KCS).
- **Nghị định số 99/2021/NĐ-CP**: Quản lý, thanh toán, quyết toán dự án sử dụng vốn đầu tư công (Mẫu biểu xác định khối lượng hoàn thành Phụ lục 03a).
- **Thông tư số 11/2021/TT-BXD**: Hướng dẫn phương pháp xác định và quản lý chi phí đầu tư xây dựng (Tổng mức kinh phí xây dựng $G_{XD} = T + GT + TL + VAT$).
- **Thông tư số 12/2021/TT-BXD**: Hệ thống định mức dự toán xây dựng công trình, định mức hao phí lao động và ca máy.
- **Thông tư số 13/2021/TT-BXD**: Phương pháp xác định chỉ tiêu kinh tế kỹ thuật và đo bóc khối lượng công trình.
- **Tiêu chuẩn thiết kế & thi công**: **TCVN 11823:2017** (Thiết kế cầu đường bộ), **TCVN 9395:2012** (Cọc khoan nhồi), **TCVN 4453:1995** (Kết cấu bê tông cốt thép toàn khối), **QCVN 18:2021/BXD** (An toàn trong thi công xây dựng).

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
        └───────┬──────────────────┬────────────────────┬──────┘
                │                  │                    │
                ▼                  ▼                    ▼
     [aec_vision_takeoff]  [aec_rebar_engineer]  [aec_cost_engineer]
     100% Công thức động   Cắt thép 11.7m <1.5%  Dự toán G_XD & 03a
                │                  │                    │
                └──────────────────┼────────────────────┘
                                   ▼
     ┌─────────────────────────────────────────────────────────┐
     │  TOÁN TẤT ĐỊNH (DETERMINISTIC MATH - ZERO HALLUCINATION)│
     │  • openpyxl: 7 Sheet Excel liên kết động 100%           │
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
   - **Toán kỹ thuật (Deterministic Math):** Giao cho mã nguồn Python thuần (`openpyxl`, `python-docx`, `ezdxf`, `numpy`) tính toán dựa trên công thức giải tích hình học và thuật toán tối ưu. Tuyệt đối **CẤM SỐ CHẾT (Dead Numbers)**; 100% ô tính phải là công thức động (`SUM`, `PRODUCT`, `ROUND`, `VLOOKUP`).
   - **Mô hình Ngôn ngữ (Generative AI):** Chỉ đảm nhận vai trò đọc hiểu ngữ nghĩa bản vẽ, tra cứu ngữ cảnh kỹ thuật (RAG trên TCVN/QCVN) và soạn thảo Thuyết minh Biện pháp thi công. Mô hình AI bị khóa quyền, không được tự ý can thiệp hay "bịa" (hallucinate) các con số tài chính hoặc khối lượng nghiệm thu.
2. **Kiến trúc Bảng tin Dữ liệu Tập trung (Blackboard Architecture):**
   - Mọi tác tử trao đổi dữ liệu qua một tệp trạng thái duy nhất: `PROJECT_STATE.json` (Single Source of Truth).
   - Tác tử phía sau tiêu thụ dữ liệu đầu ra đã được kiểm chứng của tác tử phía trước, đảm bảo dữ liệu xuyên suốt từ Bóc tách $\rightarrow$ Cắt thép $\rightarrow$ Dự toán $\rightarrow$ Thanh toán $\rightarrow$ Tiến độ $\rightarrow$ KCS.
3. **Cơ chế Thẩm tra Độc lập Đóng gói (Autonomous Audit Guardrail):**
   - Tác tử thẩm tra độc lập (`aec_audit_verifier`) tự động quét toàn bộ cây công thức Excel và ma trận ngày KCS. Nếu phát hiện công thức gãy (`#REF!`, `#VALUE!`), số chết vô căn cứ hoặc biên bản bị đá ngày (nghiệm thu trước ngày thi công), tác tử sẽ hạ điểm và chặn xuất bản hồ sơ.

---

## 📁 3. Cấu trúc Thư mục Kho Mã Nguồn (Repository Layout)

```text
DONG_GOI_HETHONG_AEC/
│
├── aec_core/                     # ⚙️ LÕI XỬ LÝ PYTHON (DETERMINISTIC ENGINE)
│   ├── __init__.py               # Khởi tạo package
│   ├── audit_verifier.py         # Module thẩm tra kiểm toán độc lập 100/100
│   └── project_state.py          # Module quản trị dữ liệu tập trung (Blackboard State)
│
├── agents/                       # 🤖 ĐẶC TẢ TÁC TỬ & ĐIỀU PHỐI MULTI-AGENT
│   ├── HE_THONG_MULTI_AGENT_AEC.md            # Thiết kế vai trò 6 tác tử chuyên gia
│   ├── QUAN_LY_DIEU_PHOI_MULTI_AGENT_AEC.md   # Cơ chế điều phối Blackboard & State
│   ├── aec_audit_verifier.py                  # Script thẩm tra độc lập
│   ├── project_state_manager.py               # Quản lý vòng đời Single Source of Truth
│   ├── rag_method_statement_huggingface.py    # Pipeline RAG Hugging Face BGE-M3 + Qwen2.5
│   └── PROJECT_STATE.json                     # Snapshot trạng thái dự án mẫu
│
├── workflows/                    # 📋 CHUỖI 7 QUY TRÌNH CHUẨN AEC & HƯỚNG DẪN AI
│   ├── 00_TONG_QUAN_QUY_TRINH_KHEP_KIN_AEC.md          # Bản đồ chuỗi giá trị 7 bước
│   ├── 01_QUY_TRINH_BOC_TACH_HINH_HOC_TAKEOFF.md       # Quy trình 1: Bóc tách 100% công thức sống
│   ├── 02_QUY_TRINH_TO_HOP_CAT_THEP_1D.md              # Quy trình 2: Cắt thép 11.7m (< 1.5% đề-xê)
│   ├── 03_QUY_TRINH_DU_TOAN_GXD_TT11.md                # Quy trình 3: Dự toán G_XD Thông tư 11/2021
│   ├── 04_QUY_TRINH_THANH_TOAN_PHU_LUC_03A.md          # Quy trình 4: Thanh toán 03a Nghị định 99/2021
│   ├── 05_QUY_TRINH_TIEN_DO_CPM_MS_PROJECT.md          # Quy trình 5: Tiến độ WBS & MS Project XML
│   ├── 06_QUY_TRINH_KCS_LOGIC_CHEO_XUAT_WORD.md        # Quy trình 6: KCS Word & Ma trận ngày chéo
│   ├── 07_QUY_TRINH_THUYET_MINH_BIEN_PHAP_HUGGINGFACE.md # Quy trình 7: RAG Hugging Face BPTC
│   └── HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md  # Sổ tay vận hành Antigravity, Claude, GPT
│
├── prompts/                      # 🧠 MASTER SYSTEM PROMPTS CHUYÊN DỤNG
│   ├── 00_PROMPT_TONG_HOP_MULTI_AGENT_AEC.md           # Prompt tổng hợp điều phối 6-7 tác tử
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
│   ├── Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx       # Workbook 7 sheet liên kết động hoàn hảo
│   ├── Tien_Do_Thi_Cong_Cau_Km19+529.080.xml           # File MS Project XML (36 công tác, CPM)
│   ├── Tien_Do_Thi_Cong_Cau_Km19+529.080.mpp           # File Microsoft Project Native binary
│   ├── Ho_So_Bien_Ban_Nghiem_Thu_KCS_Cau_Km19+529.080.docx # Trọn bộ 22 Biên bản KCS chuẩn NĐ 207
│   ├── Thuyet_Minh_Bien_Phap_Thi_Cong_Cau_Km19+529.080.md  # Thuyết minh BPTC 8 chương TCVN
│   ├── BAO_CAO_THAM_TRA_AEC_AUDIT.md                   # Báo cáo thẩm tra độc lập Điểm 100/100
│   ├── PROJECT_STATE.json                              # Trạng thái dự án mẫu hoàn chỉnh
│   ├── Ho_So_KCS_QS_Cau_Khai_Hoang_2.xlsx              # File mẫu Cầu Khai Hoang 2
│   ├── Tien_Do_Thi_Cong_Cau_Khai_Hoang_2.xml           # File tiến độ Cầu Khai Hoang 2
│   ├── Ho_So_KCS_QS_TienDo_Nha_Dan_Dung.xlsx           # File mẫu Nhà Dân dụng cao tầng
│   └── Tien_Do_Thi_Cong_Dan_Dung.xml                   # File tiến độ Nhà Dân dụng cao tầng
│
├── examples/                     # 🚀 VÍ DỤ THỰC THI & SCRIPT CHẠY MẪU
│   ├── run_pipeline.py                                 # Pipeline runner kiểm tra & audit toàn bộ
│   ├── generate_sample_bridge_project.py               # Script tự tạo lại toàn bộ Workbook & XML Cầu
│   └── generate_kcs_word_package.py                    # Script tự xuất bộ 22 biên bản KCS Word
│
├── .gitignore                    # Bộ lọc file rác Python, OS và Office lock
├── LICENSE                       # Giấy phép bản quyền MIT
├── pyproject.toml                # Cấu hình đóng gói chuẩn PEP 621
├── requirements.txt              # Thư viện phụ thuộc chính (openpyxl, docx, ezdxf...)
└── README.md                     # Tài liệu giới thiệu chính của repository
```

---

## 🔄 4. Chuỗi 7 Bước Quy trình Kỹ thuật Khép kín

| Bước | Tên Quy trình | Tác tử Phụ trách | Chuẩn Pháp lý / Kỹ thuật | Sản phẩm Đầu ra |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Bóc tách Takeoff WBS** | `aec_vision_takeoff` | TCVN 11823:2017, TT 13/2021 | Sheet `QS_DIEN_GIAI_CHI_TIET` (100% công thức động Dài x Rộng x Cao x SL x Hệ số, CẤM SỐ CHẾT) |
| **02** | **Tối ưu Cắt thép 1D** | `aec_rebar_engineer` | TCVN 4453:1995, Cutting Stock | Sheet `TO_HOP_CAT_THEP_11M7` (Tổ hợp thanh trên cây 11.7m, phôi thừa đề-xê < 1.5%) |
| **03** | **Dự toán $G_{XD}$** | `aec_cost_engineer` | TT 11/2021/TT-BXD, TT 13/2021 | Sheet `TONG_HOP_DU_TOAN_GXD` ($G_{XD} = T + GT(7.3\%) + TL(5.5\%) + VAT(8\%)$) |
| **04** | **Thanh toán Kỳ 03a** | `aec_cost_engineer` | Nghị định 99/2021/NĐ-CP | Sheet `THANH_TOAN_KY_PHU_LUC_03A` (Lũy kế thực hiện, giữ lại bảo hành 5%) |
| **05** | **Tiến độ CPM & Gantt** | `aec_lead_scheduler` | TT 12/2021/TT-BXD, CPM Method | Sheet `TIEN_DO_THI_CONG_WBS` + Tệp `MS Project (.xml/.mpp)` (Critical Path, 36 tasks) |
| **06** | **Hồ sơ KCS Word** | `aec_qaqc_engineer` | Nghị định 207/2026/NĐ-CP | File Word `.docx` (22 Biên bản nghiệm thu KCS + Ma trận kiểm tra logic ngày chéo) |
| **07** | **Thuyết minh BPTC & Audit** | `aec_method_statement_agent` & `aec_audit_verifier` | RAG Hugging Face BGE-M3 + Qwen2.5 | File Thuyết minh BPTC 8 chương + Báo cáo thẩm tra độc lập Audit Score 100/100 |

---

## ⚡ 5. Cài đặt & Bắt đầu Nhanh (Quickstart)

### Yêu cầu Hệ thống
- Python 3.10 trở lên trên Windows, Linux hoặc macOS.
- Microsoft Excel 2016+ / LibreOffice Calc.
- Microsoft Project 2016+ (hoặc bất kỳ phần mềm tương thích file Project XML).
- Microsoft Word 2016+ / Google Docs.

### Cài đặt Thư viện
```bash
# 1. Clone kho lưu trữ
git clone https://github.com/your-org/AEC-MultiAgent-System.git
cd AEC-MultiAgent-System

# 2. Cài đặt các gói phụ thuộc Python
pip install -r requirements.txt
```

### Chạy Thử nghiệm Pipeline Mẫu
```bash
# Chạy chuỗi kiểm toán độc lập trên Workbook mẫu (Audit Score 100/100)
python examples/run_pipeline.py

# Sinh lại toàn bộ tệp Excel 7 Sheet sống và tệp MS Project XML từ đầu
python examples/generate_sample_bridge_project.py

# Xuất trọn bộ 22 Biên bản nghiệm thu KCS có ma trận logic ngày ra tệp Word (.docx)
python examples/generate_kcs_word_package.py
```

---

## 🤖 6. Hướng dẫn Vận hành trên 3 Nền tảng AI

Xem hướng dẫn chi tiết tại: **[HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md](workflows/HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md)**

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                        MA TRẬN HỖ TRỢ NỀN TẢNG AI                            │
├──────────────────────┬────────────────────────┬───────────────────────────────┤
│ Nền tảng AI          │ Môi trường Thực thi    │ Điểm mạnh Đặc thù             │
├──────────────────────┼────────────────────────┼───────────────────────────────┤
│ Google Antigravity   │ Terminal / Shell Máy   │ Trực tiếp ghi & chạy script, │
│ (Gemini 2.5 Flash/Pro)│ tính cục bộ (Native)   │ tích hợp sâu CAD MCP & Skills │
├──────────────────────┼────────────────────────┼───────────────────────────────┤
│ Claude (Anthropic)   │ Analysis Tool Python   │ Khả năng phân tích bản vẽ dài │
│ (Claude 3.5 Sonnet)  │ Sandbox trong Chat     │ và lập luận bóc tách sắc bén  │
├──────────────────────┼────────────────────────┼───────────────────────────────┤
│ ChatGPT (OpenAI)     │ Advanced Data Analysis │ Code Interpreter linh hoạt,   │
│ (GPT-4o / GPT-o1)    │ Sandbox trong Chat     │ hỗ trợ đóng gói Custom GPTs   │
└──────────────────────┴────────────────────────┴───────────────────────────────┘
```

### 1. Dành cho Google Antigravity (Gemini):
1. Copy 4 thư mục trong `skills/` vào `~/.gemini/config/skills/`.
2. Mở thư mục chứa hồ sơ bản vẽ công trình trong Antigravity.
3. Gửi lệnh kích hoạt từ file `prompts/00_PROMPT_TONG_HOP_MULTI_AGENT_AEC.md`. Hệ thống sẽ tự động phân tích và xuất file thẳng vào đĩa cứng.

### 2. Dành cho Claude (Anthropic):
1. Tạo một **Claude Project** mới.
2. Tải toàn bộ tài liệu trong thư mục `workflows/` và `prompts/` vào mục **Project Knowledge**.
3. Khi tải bản vẽ lên chat, yêu cầu Claude kích hoạt công cụ Python sinh file `.xlsx`, `.docx`, `.xml` để tải về.

### 3. Dành cho ChatGPT (OpenAI):
1. Đính kèm bản vẽ hoặc file bảng tính cần xử lý vào ô chat ChatGPT Plus / Team.
2. Dán đoạn Master Prompt trong file `workflows/HUONG_DAN_SU_DUNG_AI_ANTIGRAVITY_CLAUDE_GPT.md`.
3. ChatGPT sẽ dùng Python Code Interpreter để tính toán và cung cấp nút tải file trực tiếp.

---

## 🏆 7. Sản phẩm Mẫu Thực nghiệm (Production Deliverables)

Tất cả các sản phẩm mẫu trong thư mục `templates/` đã được kiểm toán thực tế và đạt độ tin cậy tuyệt đối:
- 📊 **[Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx](templates/Ho_So_KCS_QS_TienDo_Cau_Km19+529.080.xlsx)**: 7 Sheet tính toán liên thông:
  - `TO_HOP_CAT_THEP_11M7`: Thuật toán 1D Cutting Stock, tỷ lệ hao hụt phôi thừa **1.44%** (< 1.5%).
  - `KHOI_LUONG_DAO_DAP`: Tính đào đắp trắc ngang $V = \frac{F_1 + F_2}{2} \times L$.
  - `QS_DIEN_GIAI_CHI_TIET`: 100% công thức động Dài x Rộng x Cao x Số lượng x Hệ số.
  - `TONG_HOP_DU_TOAN_GXD`: Chuẩn Thông tư 11/2021/TT-BXD ($G_{XD} = 15.352$ tỷ VNĐ).
  - `THANH_TOAN_KY_PHU_LUC_03A`: Chuẩn Nghị định 99/2021/NĐ-CP (Kỳ thanh toán 01: 5.750 tỷ VNĐ).
  - `TIEN_DO_THI_CONG_WBS`: 36 công tác WBS, định mức nhân công TT 12/2021, biểu đồ Gantt CPM.
  - `HOSO_KCS_NGHIEM_THU`: 22 Biên bản KCS với ngày tháng nghiệm thu đồng bộ tuyệt đối.
- 📅 **[Tien_Do_Thi_Cong_Cau_Km19+529.080.xml](templates/Tien_Do_Thi_Cong_Cau_Km19+529.080.xml)** & **[.mpp](templates/Tien_Do_Thi_Cong_Cau_Km19+529.080.mpp)**: Khởi tạo trên Microsoft Project Schema chuẩn, liên kết quan hệ Finish-to-Start (FS), tự động tính đường găng Critical Path (270 ngày thi công).
- 📝 **[Ho_So_Bien_Ban_Nghiem_Thu_KCS_Cau_Km19+529.080.docx](templates/Ho_So_Bien_Ban_Nghiem_Thu_KCS_Cau_Km19+529.080.docx)**: Xuất trọn bộ 22 biên bản nghiệm thu KCS chuẩn Nghị định 207/2026/NĐ-CP kèm bảng ma trận đối soát ngày chéo.
- 📑 **[Thuyet_Minh_Bien_Phap_Thi_Cong_Cau_Km19+529.080.md](templates/Thuyet_Minh_Bien_Phap_Thi_Cong_Cau_Km19+529.080.md)**: 8 chương kỹ thuật chỉ dẫn thi công cọc khoan nhồi D1000, mố trụ đúc tại chỗ, đúc và lao lắp dầm Super-T 38.2m, phòng chống lũ quét miền núi.
- 🛡️ **[BAO_CAO_THAM_TRA_AEC_AUDIT.md](templates/BAO_CAO_THAM_TRA_AEC_AUDIT.md)**: Báo cáo kiểm định tự động với số điểm tuyệt đối **100/100**.

---

## ⚖️ 8. Giấy phép Bản quyền (License)

Dự án được phân phối dưới giấy phép mã nguồn mở **[MIT License](LICENSE)**. Bạn hoàn toàn có quyền tự do sử dụng, chỉnh sửa, tích hợp vào các dự án thương mại hoặc hệ thống nội bộ của doanh nghiệp xây dựng mà không phải trả phí bản quyền.

---

## 🤝 9. Đóng góp & Phát triển (Contributing)

Mọi đóng góp từ cộng đồng Kỹ sư Dự toán (QS), Kỹ sư Quản lý Chất lượng (QA/QC), Kỹ sư Hiện trường, Chỉ huy trưởng và các Chuyên gia AI/Data Science đều rất được trân trọng. Vui lòng mở **Issue** hoặc gửi **Pull Request** theo hướng dẫn chuẩn GitHub.

*Hệ thống được nghiên cứu, phát triển và đóng gói bởi Cộng đồng Kỹ sư Xây dựng Số hóa Việt Nam.*
