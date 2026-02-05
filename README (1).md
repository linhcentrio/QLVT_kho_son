# 🎨 QUẢN LÝ VẬT TƯ KHO SƠN

## Phòng Dịch Vụ Sơn | Tháng 01/2026 | Version 1.0

---

## 📋 Giới Thiệu

Ứng dụng web quản lý vật tư kho sơn dành cho Phòng Dịch Vụ Sơn. Cung cấp giao diện thân thiện để:
- ✅ Nhập phiếu xuất vật tư (18 field)
- ✅ Quản lý danh sách phiếu
- ✅ Thống kê & báo cáo real-time
- ✅ Xuất Excel (4 sheet) & CSV
- ✅ Danh mục 30+ vật tư & Phân bổ 4 tổ

---

## 🚀 Cài Đặt & Chạy

### Bước 1: Tạo môi trường Python

```bash
# Tạo thư mục dự án
mkdir quan_ly_vat_tu
cd quan_ly_vat_tu

# Tạo virtual environment
python -m venv venv

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Hoặc Windows
venv\Scripts\activate
```

### Bước 2: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy App

```bash
python app_vat_tu.py
```

**Output:**
```
Running on http://localhost:7860
```

Mở trình duyệt và truy cập: **http://localhost:7860**

---

## 📖 Hướng Dẫn Sử Dụng

### 🎯 Tab 1: Nhập Phiếu Xuất

Nhập thông tin phiếu xuất với 18 field:

| Field | Mô Tả | Bắt Buộc |
|-------|-------|---------|
| STT | Số thứ tự | ✅ |
| CVDV | Công việc dịch vụ (Sơn, T, ...) | ✅ |
| Ngày tháng | Format: DD/MM/YYYY | ✅ |
| Số BG | Số biên giới | ✅ |
| BKS | Biển kiểm soát | ✅ |
| Hiệu xe | Loại xe | ✅ |
| Màu | Màu sơn | ✅ |
| Khách hàng | Tên khách hàng | ✅ |
| Tên hàng | Tên vật tư | ✅ |
| Mã hàng | Chọn từ dropdown (auto lấy giá) | ✅ |
| Số lượng | Số lượng xuất | ✅ |
| Đơn giá | Auto tính từ danh mục | ✅ |
| KTV | Kỹ thuật viên | ✅ |
| Tổ | Chọn: Tổ sơn, T, VTDC/ĐB, Khoán | ✅ |
| Ghi chú | Ghi chú thêm | ❌ |
| Doanh thu BG | Doanh thu buổi giao | ✅ |

**Auto Tính:**
- Đơn giá: Lấy từ danh mục khi chọn Mã hàng
- Thành tiền = Số lượng × Đơn giá
- Vật tư 30% = Doanh thu BG × 0.30

### 📊 Tab 2: Danh Sách Phiếu

- Xem tất cả phiếu đã nhập
- Làm mới dữ liệu: **🔄 Làm mới**
- Xóa dòng cuối: **🗑️ Xóa dòng cuối**
- Xuất CSV: **📥 Xuất CSV** (file tên: `Phieu_xuat_VT_DD_MM_YYYY_HHMMSS.csv`)
- Xuất Excel: **📊 Xuất Excel** (file tên: `Phieu_xuat_VT_DD_MM_YYYY_HHMMSS.xlsx`)

### 📈 Tab 3: Thống Kê & Báo Cáo

**Hiển thị 3 bảng:**

**1. Tóm Tắt Chỉ Số**
- Tổng vật tư xuất (đ)
- Tổng vật tư 30% (đ)
- Tổng doanh thu BG (đ)
- Số phiếu BG
- Số dòng vật tư

**2. Thống Kê Theo Tổ**
- Tổ sơn: 12 vật tư
- T: 9 vật tư
- VTDC/ĐB: 6 vật tư
- Khoán: 12 vật tư

**3. Thống Kê Theo Mặt Hàng**
- Mã hàng, Tên hàng, Tổng SL, Tổng tiền

Nhấn **🔄 Cập nhật thống kê** để refresh.

### 📚 Tab 4: Danh Mục & Phân Bổ

**Bảng 1: Danh Mục 30 Vật Tư**

6 loại:
1. **Sơn lót** (3): 410-48248, D8046, SL
2. **Đóng rắn** (4): D863, P210-926, ĐC, P210-6901
3. **Dầu bóng** (4): D8112, P190-625, PLĐ, P190-6970
4. **Màu sơn** (6): GB0, DO, TRANG, DENA, GUN, 1C0
5. **Nhám** (7): P80v, P120v, P240x, P320, P80, P400, P1000
6. **Băng dính** (3): BDT, 2600A, 2600B

**Bảng 2: Phân Bổ 4 Tổ**
- Tổ sơn: 12 vật tư
- T: 9 vật tư
- VTDC/ĐB: 6 vật tư
- Khoán: 12 vật tư

---

## ⚙️ Công Thức Tính Toán

### 1️⃣ Thành Tiền
```
Thành tiền = Số lượng × Đơn giá
```
**Ví dụ:** 242 g × 448.38 đ/g = 108,508 đ

### 2️⃣ Vật Tư 30%
```
Vật tư 30% = Doanh thu BG × 0.30
```
**Ví dụ:** 5,000,000 đ × 0.30 = 1,500,000 đ

### 3️⃣ Tổng Cộng
```
Tổng vật tư = SUM(Thành tiền)
Tổng VT 30% = SUM(Vật tư 30%)
Tổng doanh thu = SUM(Doanh thu BG)
```

---

## 💾 Xuất Báo Cáo

### Format Excel (4 Sheet)

**Sheet 1: Chi tiết**
- Tất cả 18 field phiếu xuất
- Sắp xếp theo STT

**Sheet 2: Tóm tắt**
- 5 chỉ số tổng quát
- Dễ xem nhanh

**Sheet 3: Theo Tổ**
- Tổng tiền & số dòng từng tổ
- So sánh công việc giữa các tổ

**Sheet 4: Theo Mặt hàng**
- Tổng SL & tổng tiền từng vật tư
- Phân tích chi phí vật tư

### Format CSV

- Encoding: UTF-8
- Delimiter: `,`
- Dễ import vào Excel, Google Sheets, Database

---

## 📁 Cấu Trúc File

```
quan_ly_vat_tu/
├── app_vat_tu.py              # App chính (456 dòng)
├── export_report.py           # Module xuất báo cáo (234 dòng)
├── requirements.txt           # Dependencies
├── catalog_complete.json      # Danh mục 30 vật tư
├── phan_bo_bo_phan.json       # Phân bổ 4 tổ
├── README.md                  # Hướng dẫn này
├── USAGE_GUIDE.md             # Hướng dẫn export module
└── INTEGRATION.md             # Tích hợp export vào app
```

---

## 🌐 Deploy Lên Cloud (Optional)

### Hugging Face Spaces (Miễn phí)

1. Tạo repo trên https://huggingface.co/spaces
2. Upload file: `app_vat_tu.py`, `export_report.py`, `requirements.txt`
3. Tạo file `app.py`:

```python
if __name__ == "__main__":
    from app_vat_tu import tao_app
    app = tao_app()
    app.launch()
```

4. Setting: App file = `app.py`, Base image = `python:3.10`
5. Auto deploy ✅

Truy cập: `https://huggingface.co/spaces/your-username/your-space`

---

## ❓ Troubleshooting

**Q: Lỗi "FileNotFoundError: catalog_complete.json"**
- A: Đảm bảo file `catalog_complete.json` nằm cùng thư mục với `app_vat_tu.py`

**Q: App không khởi động**
- A: Kiểm tra: `pip install -r requirements.txt`
- A: Kiểm tra port 7860 không bị chiếm

**Q: Xuất Excel bị lỗi encoding**
- A: Kiểm tra: `pip install openpyxl>=3.10.0`

**Q: Dropdown mã hàng rỗng**
- A: Kiểm tra file `catalog_complete.json` có dữ liệu

---

## 📞 Hỗ Trợ

Liên hệ: support@phongdichvuson.vn
Email: info@phongdichvuson.vn

---

## 📝 License

© 2026 Phòng Dịch Vụ Sơn. All rights reserved.

---

**Happy tracking! 🚀**
