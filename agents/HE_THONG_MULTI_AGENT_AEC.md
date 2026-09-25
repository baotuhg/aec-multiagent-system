# HỆ THỐNG MẠNG LƯỚI MULTI-AGENT AEC TINH HOA (ELITE AEC AGENT NETWORK)
## KIẾN TRÚC BAN CHỈ HUY CÔNG TRƯỜNG & VĂN PHÒNG KỸ THUẬT DỰ ÁN SỐ HÓA

Hệ thống được thiết kế lại toàn diện, lựa chọn những **mô hình AI và công nghệ tốt nhất thế giới hiện nay** cho từng chuyên môn ngành Xây dựng:

```mermaid
flowchart TD
    User["Chủ đầu tư / Ban Giám đốc"] --> MasterDirector["1. aec_master_director\n(Giám đốc Dự án & Tổng chỉ huy)"]
    
    subgraph "VĂN PHÒNG KỸ THUẬT SỐ HÓA (DIGITAL OFFICE)"
        VisionTakeoff["2. aec_vision_takeoff\n(VLM Qwen2.5-VL / Gemini Vision\nĐọc bản vẽ PDF/DWG & Đếm cấu kiện)"]
        RebarEng["3. aec_rebar_engineer\n(1D Cutting Stock Engine\nCắt thép 11.7m đề-xê < 1.5%)"]
        CostEng["4. aec_cost_engineer\n(QS & Dự toán G_XD TT 11, 12, 13\nCẤM 100% SỐ CHẾT)"]
        Scheduler["5. aec_lead_scheduler\n(Tiến độ MS Project & CPM Engine\nĐịnh mức ngày công TT 12)"]
        QAQCEng["6. aec_qaqc_engineer\n(RAG Tiêu chuẩn TCVN & NĐ 207\n24 Biên bản nghiệm thu KCS)"]
    end
    
    subgraph "GIÁM SÁT THỰC ĐỊA HIỆN TRƯỜNG (SITE MONITORING)"
        SiteInspector["7. aec_site_inspector\n(YOLOv11 Vision AI Engine\nAn toàn HSE & Soi nứt bê tông)"]
    end

    MasterDirector --> VisionTakeoff & RebarEng & CostEng & Scheduler & QAQCEng & SiteInspector
    
    VisionTakeoff -.->|Dài x Rộng x Cao & Số lượng| CostEng
    RebarEng -.->|Tổng khối lượng thép tấn| CostEng
    CostEng -.->|Khối lượng chi tiết| Scheduler
    CostEng -.->|Khối lượng nghiệm thu| QAQCEng
    Scheduler -.->|Trình tự thi công| QAQCEng
    
    MasterDirector --> Deliverables["SẢN PHẨM HOÀN CHỈNH:\n1. Excel đa sheet liên kết động 100%\n2. Tiến độ MS Project .xml / .mpp\n3. Sơ đồ cắt thép 11.7m tối ưu\n4. Biên bản nghiệm thu KCS & HSE"]
```

---

## BẢNG TUYỂN CHỌN MÔ HÌNH TỐT NHẤT CHO TỪNG AGENT

| Agent ID | Tên chuyên môn | Công nghệ / Mô hình AI tuyển chọn tốt nhất | Vai trò cốt lõi trong hệ thống |
| :--- | :--- | :--- | :--- |
| **`aec_master_director`** | **Giám đốc Dự án & Tổng Chỉ huy** | Mô hình suy luận cấp cao (Reasoning LLM) | Lập kế hoạch Modular WBS, phân công tác tử, kiểm duyệt chéo chống số chết. |
| **`aec_vision_takeoff`** | **Kỹ sư Thị giác Bản vẽ (Takeoff)** | **Qwen2.5-VL / Gemini Vision** + `PyMuPDF` + `pdfplumber` + CAD MCP | "Mắt thần" đọc bản vẽ PDF/Ảnh/DWG, quét lưới trục, tự động đếm cột, dầm, cửa và trích xuất kích thước $L \times W \times H$. |
| **`aec_cost_engineer`** | **Kỹ sư Trưởng Dự toán BoQ** | **Qwen 2.5 72B-Instruct** + RAG Định mức BXD | Lập dự toán $G_{XD}$ theo Thông tư 11, 12, 13/2021/TT-BXD, bảo đảm **100% công thức động Dài x Rộng x Cao x Số lượng x Hệ số**. |
| **`aec_lead_scheduler`** | **Kỹ sư Trưởng Tiến độ** | Thuật toán đường găng CPM + MS Project XML Engine | Tra định mức nhân công TT 12, phân bổ tổ đội thợ, xác định đường găng và xuất tệp tiến độ Microsoft Project `.xml / .mpp`. |
| **`aec_qaqc_engineer`** | **Kỹ sư Quản lý Chất lượng KCS** | RAG Tiêu chuẩn TCVN + Luật XD 135 & NĐ 207 | Thiết lập danh mục 18 - 25 biên bản nghiệm thu chuyển bước, trỏ công thức khối lượng trực tiếp từ Sheet QS sang KCS. |
| **`aec_rebar_engineer`** | **Kỹ sư Cốt thép Tối ưu** | Thuật toán Integer Linear Programming (1D Cutting Stock) | Tối ưu hóa cắt ghép thép thanh trên cây nguyên chuẩn **11.7m**, ép tỷ lệ đề-xê $< 1.5\%$. |
| **`aec_site_inspector`** | **Kỹ sư Giám sát Hiện trường & HSE** | **YOLOv11** (`ppe-detection`, `concrete-crack-detection`) | Soi ảnh camera/drone hiện trường: phạt vi phạm an toàn lao động (mũ, áo, dây an toàn) và phát hiện nứt/rỗ bê tông. |

---

## CÁCH GỌI MẠNG LƯỚI TRONG ANTIGRAVITY IDE

1. **Gọi toàn bộ mạng lưới xử lý hồ sơ trọn gói:**
   > *"Hãy gọi `aec_master_director` kích hoạt mạng lưới kỹ sư xử lý hồ sơ [tên_file], bóc tách bản vẽ bằng VLM, tính dự toán G_XD, cắt thép 11.7m, lập tiến độ MS Project và danh mục KCS cho tôi."*

2. **Gọi Kỹ sư Thị giác Bản vẽ (VLM):**
   > *"Gọi `aec_vision_takeoff` đọc bản vẽ mặt bằng [file_anh hoặc PDF], đếm số lượng cửa, cột và trích xuất kích thước các phòng."*

3. **Gọi Kỹ sư Giám sát Hiện trường (HSE & Nứt bê tông):**
   > *"Gọi `aec_site_inspector` kiểm tra bức ảnh chụp công trường này xem công nhân có vi phạm an toàn không và kiểm tra vết nứt trên dầm bê tông."*
