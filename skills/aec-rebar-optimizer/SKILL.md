---
name: aec-rebar-optimizer
description: Tự động hóa giải bài toán tổ hợp cắt thép 1 chiều (1D Cutting Stock Problem) từ bảng thống kê cốt thép xây dựng. Ghép tối ưu các đoạn cắt vào cây thép nguyên 11.7m nhằm giảm thiểu tối đa hao hụt đề-xê (< 1.5 - 3%), xuất sơ đồ cắt chi tiết và bảng tổng hợp vật tư cho công trường.
---

# Tối ưu hóa Tổ hợp Cắt Thép Xây dựng (AEC-Rebar-Optimizer)

## 1. Mục tiêu
Giải quyết triệt để bài toán hao hụt cốt thép tại công trường:
- Tiêu chuẩn cây thép thương mại tại Việt Nam dài cố định: $11.7\text{m} = 11700\text{mm}$.
- Bản vẽ kết cấu yêu cầu nhiều thanh có chiều dài khác nhau ($L_i$).
- Kỹ năng này tự động tính toán cách tổ hợp (ghép đoạn) thông minh nhất để số cây thép nguyên cần mua là ít nhất và đoạn mẩu vụn (đề-xê) là nhỏ nhất.

## 2. Quy trình xử lý
Khi nhận bảng thống kê cốt thép hoặc yêu cầu cắt thép:

### Bước 1: Chuẩn hóa dữ liệu đầu vào
- Thu thập danh mục thanh theo từng đường kính ($\Phi10, \Phi12, \Phi14, \Phi16, \Phi18, \Phi20, \Phi22, \Phi25...$).
- Mỗi bản ghi bao gồm:
  - Tên/ký hiệu thanh (Mark ID).
  - Chiều dài cắt sau khi đã tính uốn móc/nối chồng ($L_i \le 11700\text{mm}$).
  - Số lượng thanh cần cắt ($N_i$).

### Bước 2: Chạy thuật toán tối ưu hóa
Chạy script thuật toán:
```bash
python .openspace/skills/aec-rebar-optimizer/scripts/optimize_rebar.py --json-file duong_dan_danh_sach_thep.json
```

Thuật toán áp dụng nguyên lý:
1. Sắp xếp các đoạn thép theo chiều dài giảm dần.
2. Ưu tiên ghép thanh lớn trước, lấp đầy khoảng trống còn lại bằng các thanh nhỏ (Best-Fit Decreasing).
3. Đánh giá tỷ lệ đề-xê tổng thể: Mục tiêu $\le 2\%$. Các đoạn thừa $> 1.5\text{m}$ được đánh dấu để tái sử dụng làm thép neo, thép đai, hoặc cọc định vị.

### Bước 3: Xuất kết quả sơ đồ cắt
Xuất ra bảng hướng dẫn cho đội gia công cốt thép tại hiện trường:
- Cây số 1: Cắt đoạn $A$ ($5200\text{mm}$) + đoạn $B$ ($3600\text{mm}$) + đoạn $C$ ($1800\text{mm}$) $\rightarrow$ Thừa $1100\text{mm}$ (làm thép đai).
- Tổng số cây nguyên cần xuất kho.
- Tổng khối lượng phế liệu dự kiến.
