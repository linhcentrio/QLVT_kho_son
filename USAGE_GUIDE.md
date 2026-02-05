# 📖 USAGE GUIDE - MODULE EXPORT_REPORT.PY

## Giới Thiệu

Module `export_report.py` cung cấp class `ReportExporter` để xuất báo cáo từ DataFrame phiếu.

---

## 🎯 Cách Sử Dụng

### 1. Import & Khởi Tạo

```python
from export_report import ReportExporter
import pandas as pd

# Tạo DataFrame phiếu (18 columns)
df_phieu = pd.DataFrame({
    'STT': [1, 2],
    'CVDV': ['Sơn', 'Sơn'],
    # ... 16 columns khác
})

# Khởi tạo exporter
exporter = ReportExporter(df_phieu)
```

### 2. Xuất Excel (4 Sheet)

```python
exporter.xuat_phieu_excel('phieu_xuat.xlsx')
```

**Output: Excel file với 4 sheet:**
- Sheet 1: Chi tiết (tất cả dòng)
- Sheet 2: Tóm tắt (5 chỉ số chính)
- Sheet 3: Theo Tổ (phân tích theo tổ)
- Sheet 4: Theo Mặt hàng (phân tích theo mặt hàng)

### 3. Xuất CSV

```python
exporter.xuat_csv('phieu_xuat.csv')
```

**Output: CSV file (UTF-8 encoding)**

### 4. Xuất Text Report

```python
report = exporter.xuat_text_report()
print(report)
```

**Output:**
```
╔════════════════════════════════════════════════════════════════════╗
║          BÁO CÁO XUẤT VẬT TƯ - 05/02/2026          ║
╚════════════════════════════════════════════════════════════════════╝

TỔNG HỢP CHỈ SỐ:
─────────────────────────────────────────────────────────────────────
Tổng vật tư xuất     : 612,824.00 đ
Tổng vật tư 30%      : 12,090,000.00 đ
Tổng doanh thu BG    : 40,300,000.00 đ
Số phiếu BG          : 10
Số dòng vật tư       : 10
─────────────────────────────────────────────────────────────────────

Báo cáo được tạo lúc: 05/02/2026 15:30:45
```

---

## 📊 Class Methods

### `__init__(df_phieu)`
Khởi tạo với DataFrame phiếu 18 columns

### `_tinh_thong_ke()`
Tính toán 5 chỉ số: tổng vật tư, tổng VT 30%, tổng doanh thu, số phiếu, số dòng

### `_them_sheet_chi_tiet(wb)`
Thêm sheet chi tiết vào workbook Excel

### `_them_sheet_tom_tat(wb)`
Thêm sheet tóm tắt (5 chỉ số) vào workbook

### `_them_sheet_theo_to(wb)`
Thêm sheet thống kê theo tổ vào workbook

### `_them_sheet_theo_mat_hang(wb)`
Thêm sheet thống kê theo mặt hàng vào workbook

### `xuat_phieu_excel(file_path)`
Xuất file Excel 4 sheet

### `xuat_csv(file_path)`
Xuất file CSV

### `xuat_text_report()`
Trả về string report dạng text

---

## 💻 Ví Dụ Hoàn Chỉnh

```python
#!/usr/bin/env python3
from export_report import ReportExporter
import pandas as pd

# Tạo dữ liệu mẫu
data = {
    'STT': [1, 2, 3],
    'CVDV': ['Sơn', 'Sơn', 'T'],
    'Ngày tháng': ['01/01/2026', '01/01/2026', '02/01/2026'],
    'Số BG': ['BG001', 'BG001', 'BG002'],
    'BKS': ['37C12345', '37C12345', '37C67890'],
    'Hiệu xe': ['VF3 Fadil', 'VF3 Fadil', 'Kia Cerato'],
    'Màu': ['Đen', 'Xanh', 'Trắng'],
    'Khách hàng': ['Khách 1', 'Khách 1', 'Khách 2'],
    'Tên hàng': ['Màu đen', 'Màu xanh', 'Sơn lót'],
    'Mã hàng': ['GB0', 'GUN', 'SL'],
    'Số lượng': [100, 150, 200],
    'Đơn giá': [734, 655, 234],
    'Thành tiền': [73400, 98250, 46800],
    'Vật tư 30%': [1200000, 1350000, 1100000],
    'Doanh thu BG': [4000000, 4500000, 3667000],
    'KTV': ['KTV1', 'KTV2', 'KTV3'],
    'Tổ': ['Tổ sơn', 'Tổ sơn', 'T'],
    'Ghi chú': ['Ghi chú 1', '', 'Ghi chú 3']
}

df = pd.DataFrame(data)

# Khởi tạo exporter
exporter = ReportExporter(df)

# Xuất báo cáo
print("=== TEXT REPORT ===")
print(exporter.xuat_text_report())

print("\n=== EXCEL EXPORT ===")
exporter.xuat_phieu_excel('report_2026_01.xlsx')
print("✅ Xuất Excel xong!")

print("\n=== CSV EXPORT ===")
exporter.xuat_csv('report_2026_01.csv')
print("✅ Xuất CSV xong!")
```

---

## 📝 18 Columns Bắt Buộc

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | STT | int | Số thứ tự |
| 2 | CVDV | str | Công việc dịch vụ |
| 3 | Ngày tháng | str | Format DD/MM/YYYY |
| 4 | Số BG | str | Số biên giới |
| 5 | BKS | str | Biển kiểm soát |
| 6 | Hiệu xe | str | Loại xe |
| 7 | Màu | str | Màu sơn |
| 8 | Khách hàng | str | Tên khách hàng |
| 9 | Tên hàng | str | Tên vật tư |
| 10 | Mã hàng | str | Mã vật tư |
| 11 | Số lượng | float | Số lượng xuất |
| 12 | Đơn giá | float | Đơn giá (đ) |
| 13 | Thành tiền | float | = SL × Đơn giá |
| 14 | Vật tư 30% | float | = Doanh thu × 0.30 |
| 15 | Doanh thu BG | float | Doanh thu buổi giao |
| 16 | KTV | str | Kỹ thuật viên |
| 17 | Tổ | str | Tổ làm việc |
| 18 | Ghi chú | str | Ghi chú thêm |

---

## ✅ Kiểm Tra & Validation

```python
# Kiểm tra số columns
assert len(df.columns) == 18, "DataFrame phải có 18 columns!"

# Kiểm tra không có NaN
assert df.isnull().sum().sum() == 0, "Không được có giá trị rỗng!"

# Kiểm tra kiểu dữ liệu
assert df['Số lượng'].dtype in ['float64', 'int64'], "Số lượng phải là số!"
```

---

**Happy exporting! 🚀**
