---
name: aec-cad-automation
description: Tự động hóa điều khiển AutoCAD/CAD trực tiếp qua giao thức MCP (autocad-mcp và cad-mcp), vẽ hình học, trích xuất thuộc tính bản vẽ DWG, đọc tọa độ mặt cắt ngang (cross-sections), tính toán diện tích hình học và khối lượng đào đắp (san nền, giao thông, kè đá) mà không cần xuất file trung gian. Hỗ trợ cơ chế tự sửa lỗi lệnh CAD (Self-Evolution).
---

# Tự động hóa CAD & Đo bóc Khối lượng Mặt cắt ngang (AEC-CAD)

## 1. Mục tiêu & Kiến Trúc Hệ Thống MCP 3 Thành Phần

```text
[ Giao diện AI: Claude Desktop / Windsurf / Cursor / Antigravity ]
                               │
                               ▼ (Giao thức MCP: cad-mcp / autocad-mcp)
               [ MCP Server điều khiển AutoCAD (Local) ]
                               │
                               ▼ (API / COM Interop: win32com / ezdxf)
      [ Bản vẽ DWG trong AutoCAD ] <───> [ Hồ sơ thiết kế (Excel/PDF) ]
```

Cung cấp khả năng cho AI Agent tương tác trực tiếp 2 chiều với phần mềm AutoCAD (AutoCAD 2026/GstarCAD) thông qua giao thức MCP:
- Đọc thông tin bản vẽ đang mở: Danh sách layer, blocks, text (giải mã TCVN3 sang Unicode), dim, polyline.
- Quét hàng loạt bản vẽ DWG trong thư mục hồ sơ: Tự động phân loại cấu kiện theo Modular WBS (Cọc, Mố, Trụ, Dầm, Bản mặt cầu, Lan can, Đào đắp).
- Đối soát 2 chiều: So khớp dữ liệu kích thước hình học từ CAD với bảng tiên lượng khối lượng Excel BoQ và thuyết minh Markdown.
- Vẽ trực tiếp hình học (đường nét, hình học phức tạp, trích xuất mặt cắt, chi tiết cấu kiện) lên viewport AutoCAD.
- Đo bóc khối lượng hình học: Tự động tính diện tích khép kín (Shoelace), bóc tách mặt cắt ngang đào/đắp nền đường, móng kè, công trình cống.

## 2. Công cụ MCP khả dụng

Agent có thể sử dụng các công cụ từ 2 kênh MCP:

### A. Kênh `cad-mcp` (GsLc API)
- `smart_cad_command`: Lệnh chính để thực thi từng thao tác CAD (vẽ circle, line, polyline, move, query layer, zoom...).
  - Cú pháp tham số: camelCase (ví dụ: `startPoint: [x, y, z]`, `endPoint: [x, y, z]`).
  - Điểm tọa độ: Mảng `[x, y, z]` (mặc định z=0).
- `batch_execute`: Thực thi chuỗi lệnh phụ thuộc liên tiếp để tăng tốc độ.
- `query_api_commands`: Tra cứu cú pháp lệnh API trước khi gọi.

### B. Kênh `autocad-mcp` (Slacker-LLC)
- `autocad_status`: Kiểm tra trạng thái kết nối với phiên bản AutoCAD đang mở.
- `list_open_drawings`: Liệt kê các bản vẽ DWG đang mở.
- `list_layers`: Đọc danh sách tất cả các layer trong bản vẽ.
- `draw_geometry` / `query_geometry`: Vẽ và trích xuất hình học 2D/3D.

## 3. Quy trình Đo bóc Khối lượng Mặt cắt ngang

Khi người dùng yêu cầu: *"Đo bóc khối lượng từ các mặt cắt ngang trong bản vẽ"* hoặc *"Vẽ lại các nét cắt để lấy khối lượng"*:

### Bước 1: Khảo sát hiện trạng bản vẽ
1. Kiểm tra kết nối CAD: Xác nhận AutoCAD đang mở bản vẽ hợp lệ.
2. Quét danh sách Layer: Tìm các layer chứa tim tuyến, đường tự nhiên, đường thiết kế, ranh giới taluy, nét cắt ngang (ví dụ: nét màu xanh, layer `MAT_CAT`, `DIA_CHAT`, `THIET_KE`).

### Bước 2: Trích xuất tọa độ mặt cắt ngang
1. Truy vấn các polyline đại diện cho vùng đào (Cut) và vùng đắp (Fill) tại từng mặt cắt ngang theo lý trình $Km$.
2. Đọc tọa độ danh sách đỉnh $[(x_1, y_1), (x_2, y_2), ..., (x_n, y_n)]$.

### Bước 3: Tính diện tích hình học mặt cắt
Sử dụng công thức Shoelace để tính diện tích thực tế:
$$A = \frac{1}{2} \left| \sum_{i=1}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) + (x_n y_1 - x_1 y_n) \right|$$

Hoặc gọi script hỗ trợ:
```bash
python .openspace/skills/aec-cad-automation/scripts/calculate_cross_section.py --json-input data_sections.json
```

### Bước 4: Tính khối lượng đào đắp giữa các lý trình
Áp dụng phương pháp diện tích trung bình 2 đầu:
$$V = \frac{A_1 + A_2}{2} \times L$$
Trong đó:
- $A_1, A_2$: Diện tích đào (hoặc đắp) tại 2 mặt cắt liên tiếp ($m^2$).
- $L$: Khoảng cách giữa 2 mặt cắt theo tim tuyến ($m$).

### Bước 5: Phản hồi và Cập nhật bản vẽ
1. Xuất bảng tổng hợp khối lượng đào, đắp chi tiết theo từng cọc/lý trình.
2. Nếu được yêu cầu: Vẽ trực tiếp nhãn ghi chú (Text/MText) diện tích và khối lượng lên ngay bên cạnh từng mặt cắt trong AutoCAD.

## 4. Xử lý Lỗi & Cơ chế Tự tiến hóa (Self-Evolution)
- **Lỗi UIPI (User Interface Privilege Isolation):** Đảm bảo tiến trình CAD và MCP Agent cùng cấp quyền (Elevation level).
- **Lỗi Handle không hợp lệ:** Khi một đối tượng bị xóa hoặc Undo, handle cũ sẽ mất hiệu lực; Agent phải truy vấn lại đối tượng mới nhất thay vì dùng handle cũ.
- **Tự động vá lỗi (FIX):** Khi một lệnh vẽ bị từ chối do trùng tên block hoặc sai kiểu dữ liệu tọa độ, OpenSpace ghi nhận trace và tự động chuyển đổi định dạng tham số.
