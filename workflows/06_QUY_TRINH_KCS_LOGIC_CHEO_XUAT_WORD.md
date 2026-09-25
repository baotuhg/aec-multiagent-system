# QUY TRÌNH 06: QUẢN LÝ CHẤT LƯỢNG KCS, LOGIC NGÀY CHÉO & XUẤT WORD
## CĂN CỨ PHÁP LÝ: NGHỊ ĐỊNH SỐ 207/2026/NĐ-CP & LUẬT XÂY DỰNG SỐ 135/2025/QH15

---

### I. NGUYÊN TẮC CỐT LÕI
1. **Kiểm soát tính hợp pháp của hồ sơ KCS:** Biên bản nghiệm thu là căn cứ pháp lý để thanh quyết toán và bàn giao công trình. Bất kỳ sự mâu thuẫn nào về ngày tháng giữa Biên bản nghiệm thu, Phiếu kết quả thí nghiệm và Nhật ký thi công đều là lỗi nghiêm trọng bị xuất toán khi kiểm toán.
2. **Nguyên tắc "Không được đá ngày":**
   - Nghiệm thu công tác sau bắt buộc phải diễn ra sau khi công tác trước đã được nghiệm thu đạt yêu cầu.
   - Các công tác bê tông bắt buộc phải có kết quả thử độ sụt cùng ngày và kết quả nén mẫu R7 / R28 hợp chuẩn trước khi cho phép chịu lực hoặc chuyển bước thi công kết cấu bên trên.

### II. MA TRẬN KIỂM SOÁT LOGIC CHÉO NGÀY THÁNG (DATE CROSS-CHECK MATRIX)
1. **Chuỗi thi công Cọc khoan nhồi:**
   - Ngày hạ lồng thép cọc nhồi $\rightarrow$ Ngày đổ bê tông cọc nhồi (cùng ngày hoặc hôm sau).
   - Ngày đổ bê tông cọc $\rightarrow$ Tối thiểu sau $7 - 14$ ngày mới làm **Siêu âm cọc** và **Thử tải động PDA**.
   - Có kết quả siêu âm và PDA đạt yêu cầu mới được nghiệm thu công tác **Đập đầu cọc nhồi** và **Đổ bê tông lót đáy bệ**.
2. **Chuỗi thi công Bệ và Thân mố trụ:**
   - Ngày đổ bê tông bệ $\rightarrow$ Tối thiểu sau 7 ngày (đạt R7) mới cho phép lắp dựng cốt thép và ván khuôn thân mố/thân trụ.
   - Thân đặc trụ cao ($11.4\text{m} - 14.5\text{m}$) đổ bê tông xong $\rightarrow$ Đạt R14 mới cho phép thi công xà mũ trụ và đá kê gối.
3. **Chuỗi thi công Dầm Super-T:**
   - Đúc dầm tại bãi $\rightarrow$ Đạt $100\%$ cường độ R28 (hoặc tối thiểu $85\%$ nếu bảo dưỡng hơi nước) mới được **Căng kéo cáp DUL $\Phi 15.2\text{mm}$**.
   - Căng cáp xong $\rightarrow$ Bơm vữa ống gen kín khít $\rightarrow$ Sau 24-48h vữa đông cứng mới được vận chuyển và cẩu lao dầm.
   - Lao dầm vào nhịp $\rightarrow$ Yên vị trên gối chậu $\rightarrow$ Mới thi công dầm ngang, bản liên tục nhiệt và bản mặt cầu C35.
4. **Chuỗi hoàn thiện mặt cầu:**
   - Bản mặt cầu đổ bê tông xong $\rightarrow$ Đạt R14 $\rightarrow$ Mới phun màng chống thấm và thảm bê tông nhựa chặt C16.
   - Toàn bộ kết cấu hoàn thành $\rightarrow$ Bê tông đạt R28 $\rightarrow$ Mới thực hiện **Thử tải tĩnh và động toàn cầu**.

### III. TỰ ĐỘNG XUẤT TRỌN BỘ BIÊN BẢN RA FILE WORD (.DOCX)
- Viết script Python sử dụng thư viện `python-docx` để sinh ra tài liệu Word chuẩn thể thức:
  + Quốc hiệu, Tiêu ngữ, Tên Ban QLDA, Tên Nhà thầu.
  + Số hiệu biên bản chuẩn hóa (`BBNT-01` đến `BBNT-22/NT-GXD`).
  + Thành phần ký kết: Tư vấn giám sát trưởng, Kỹ sư giám sát, Chỉ huy trưởng công trường, Kỹ sư KCS.
  + Nội dung nghiệm thu: Kích thước hình học, cao độ, tọa độ, chứng chỉ vật liệu, phiếu thí nghiệm.
  + Cột khối lượng nghiệm thu: Lấy tự động từ Sheet QS.
  + Bảng ký tên đóng dấu ở cuối mỗi biên bản.
