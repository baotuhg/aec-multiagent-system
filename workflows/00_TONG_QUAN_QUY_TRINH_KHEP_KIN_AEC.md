# TỔNG QUAN QUY TRÌNH QUẢN TRỊ KỸ THUẬT & DỰ ÁN AEC KHÉP KÍN (8 BƯỚC)
## HỆ THỐNG VĂN PHÒNG KỸ THUẬT SỐ HÓA & BAN CHỈ HUY CÔNG TRƯỜNG THÔNG MINH

---

### SƠ ĐỒ CHUỖI GIÁ TRỊ DỮ LIỆU KHÉP KÍN (END-TO-END PIPELINE)

```mermaid
flowchart TD
    In["HỒ SƠ BẢN VẼ THIẾT KẾ (PDF / CAD DWG / THUYẾT MINH)"] --> S1["BƯỚC 1: BÓC TÁCH HÌNH HOC & WBS\n(CẤM 100% SỐ CHẾT: Dài x Rộng x Cao x Số lượng x Hệ số)"]
    
    S1 --> S2["BƯỚC 2: TỔ HỢP CẮT THÉP 1D\n(Ghép cây 11.7m, phôi thừa đề-xê < 1.5%)"]
    S1 --> S3["BƯỚC 3: PHÂN TÍCH ĐỊNH MỨC & TỔNG HỢP VẬT TƯ (BOM)\n(Sắt thép từng loại Ø, Xi măng, Cát, Đá, Cáp DƯL, Phụ gia...)"]
    
    S1 & S3 --> S4["BƯỚC 4: DỰ TOÁN G_XD CHUẨN TT 11/2021\n(Chi phí trực tiếp T, GT = 7.3%, TL = 5.5%, VAT = 8%)"]
    
    S4 --> S5["BƯỚC 5: BẢNG THANH TOÁN KỲ PHỤ LỤC 03a\n(Chuẩn NĐ 99/2021: Lũy kế, Khấu trừ tạm ứng, Bảo hành)"]
    S4 & S3 --> S6["BƯỚC 6: TIẾN ĐỘ THI CÔNG CPM & MS PROJECT\n(Định mức TT 12, phân bổ 12 tổ đội, Gantt CPM, file .xml / .mpp)"]
    
    S6 --> S7["BƯỚC 7: HỒ SƠ KCS & MA TRẬN LOGIC CHÉO NGÀY\n(Chuẩn NĐ 207/2026: Không bị đá ngày, xuất Word .docx)"]
    S6 --> S8["BƯỚC 8: THUYẾT MINH BPTC & KIỂM TOÁN AUDIT\n(RAG Hugging Face: BGE-M3 + Qwen2.5-7B tra cứu TCVN, Audit 100/100)"]
    
    subgraph KET_QUA["BỘ SẢN PHẨM HOÀN CHỈNH BẮT BUỘC BÀN GIAO"]
        Out1["1. File Excel 9 Sheet liên kết động 100%"]
        Out2["2. File Tiến độ MS Project (.xml / .mpp)"]
        Out3["3. Trọn bộ Biên bản KCS Word (.docx)"]
        Out4["4. Thuyết minh Biện pháp thi công chi tiết (.docx/.md)"]
        Out5["5. Báo cáo Thẩm tra Độc lập Điểm 100/100 (.md)"]
    end

    S5 & S6 & S7 & S8 --> KET_QUA
```

---

### DANH MỤC 8 BƯỚC QUY TRÌNH CHUẨN

| Bước | Tên quy trình | Căn cứ pháp lý & Tiêu chuẩn | Đầu ra kỹ thuật | Nguyên tắc cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Bóc tách Takeoff & WBS** | TCVN thiết kế, Chỉ dẫn kỹ thuật | Bảng diễn giải hình học | **Tuyệt đối cấm số chết**, dòng con $= E \times F \times G \times H \times I$, dòng cha $= \text{SUM}$. |
| **02** | **Tổ hợp Cắt thép 1D** | TCVN 1651:2018 | Bảng cắt thép cây 11.7m | Thuật toán 1D Cutting Stock, ép phôi thừa đề-xê $< 1.5\%$. |
| **03** | **Phân tích & Tổng hợp Vật tư (BOM)** | Thông tư 12/2021/TT-BXD | Bảng phân rã WBS & Tổng hợp vật tư toàn cầu | Hao phí xi măng, cát, đá, sắt thép từng loại $\varnothing$, cáp DƯL; 100% công thức động trỏ từ Sheet QS. |
| **04** | **Dự toán tổng hợp $G_{XD}$** | Thông tư 11/2021/TT-BXD | Bảng tổng hợp chi phí $G_{XD}$ | Trỏ link trực tiếp từ Sheet QS: $GT = 7.3\% \times T$, $TL = 5.5\%$, $VAT = 8\%$. |
| **05** | **Thanh toán kỳ (Phụ lục 03a)** | Nghị định 99/2021/NĐ-CP | Bảng xác định khối lượng kỳ | Lũy kế kỳ trước, thực hiện kỳ này, khấu trừ tạm ứng $20\%$, bảo hành $5\%$. |
| **06** | **Tiến độ CPM & MS Project** | Thông tư 12/2021/TT-BXD | File tiến độ `.xml` / `.mpp` | Định mức ngày công, phân bổ tổ đội thợ, xác định đường găng Critical Path. |
| **07** | **Hồ sơ KCS & Logic chéo** | Nghị định 207/2026/NĐ-CP | Trọn bộ biên bản Word `.docx` | Ma trận logic ngày tháng không đá ngày (Cọc $\rightarrow$ Thí nghiệm $\rightarrow$ Bệ $\rightarrow$ Thân $\rightarrow$ Dầm). |
| **08** | **Thuyết minh BPTC & Audit** | QCVN 18:2021/BXD, TCVN | Thuyết minh 8 chương & Báo cáo Audit | RAG Hugging Face (`BAAI/bge-m3` + `Qwen2.5-7B`), Thẩm tra độc lập đạt điểm 100/100. |

---

### TÍNH LIÊN KẾT TOÀN VẸN (ZERO BROKEN LINKS)
- Khi một thông số kích thước cấu kiện thay đổi (ví dụ chiều dài cọc, chiều cao thân mố trụ):
  1. Sheet QS tự nhảy khối lượng.
  2. Bảng phân tích và tổng hợp vật tư tự động cập nhật khối lượng xi măng, cát, đá, sắt thép từng loại $\varnothing$.
  3. Bảng tổng hợp dự toán $G_{XD}$ tự nhảy giá trị.
  4. Bảng tiến độ tự tính lại số ngày công và thời gian thi công.
  5. Khối lượng nghiệm thu trong Biên bản KCS tự động cập nhật.
  6. Giá trị thanh toán kỳ Phụ lục 03a tự động cập nhật.
- Không bao giờ cần phải chỉnh sửa thủ công rời rạc từng tài liệu!
