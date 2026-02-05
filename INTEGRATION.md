# 🔗 INTEGRATION GUIDE - TÍH HỢP EXPORT VỚI APP

## Giới Thiệu

Hướng dẫn tích hợp module `export_report.py` vào Gradio app `app_vat_tu.py`.

---

## 🎯 Kiến Trúc Tích Hợp

```
┌────────────────────────────────┐
│   Gradio UI (4 Tabs)           │
├────────────────────────────────┤
│ Tab 1: Nhập phiếu              │
│ Tab 2: Danh sách phiếu         │
│ Tab 3: Thống kê & báo cáo      │
│ Tab 4: Danh mục & phân bổ      │
└────────────────────────────────┘
          ↓
┌────────────────────────────────┐
│   state (gr.State)             │ ← Lưu DataFrame phiếu
│   Update & Validation          │
└────────────────────────────────┘
          ↓
┌────────────────────────────────┐
│   export_report.ReportExporter │
├────────────────────────────────┤
│ xuat_phieu_excel()             │ → Excel file
│ xuat_csv()                     │ → CSV file
│ xuat_text_report()             │ → Text string
└────────────────────────────────┘
          ↓
┌────────────────────────────────┐
│   Output Files                 │
├────────────────────────────────┤
│ phieu_xuat_DD_MM_YYYY_HH.xlsx  │
│ phieu_xuat_DD_MM_YYYY_HH.csv   │
│ report.txt                     │
└────────────────────────────────┘
```

---

## 📝 Các Bước Tích Hợp

### Bước 1: Import

```python
from export_report import ReportExporter
```

### Bước 2: Tạo State

```python
state = gr.State(value=None)  # Lưu DataFrame phiếu
```

### Bước 3: Hàm Xuất CSV

```python
def xuat_csv(state_df):
    """Xuất CSV"""
    if state_df is None or len(state_df) == 0:
        return None, "❌ Không có dữ liệu!"

    try:
        filename = f"Phieu_xuat_VT_{datetime.now().strftime('%d_%m_%Y_%H%M%S')}.csv"
        state_df.to_csv(filename, index=False, encoding='utf-8')
        return filename, f"✅ Xuất CSV: {filename}"
    except Exception as e:
        return None, f"❌ Lỗi: {str(e)}"
```

### Bước 4: Hàm Xuất Excel

```python
def xuat_excel(state_df):
    """Xuất Excel 4 sheet"""
    if state_df is None or len(state_df) == 0:
        return None, "❌ Không có dữ liệu!"

    try:
        exporter = ReportExporter(state_df)
        filename = f"Phieu_xuat_VT_{datetime.now().strftime('%d_%m_%Y_%H%M%S')}.xlsx"
        exporter.xuat_phieu_excel(filename)
        return filename, f"✅ Xuất Excel: {filename}"
    except Exception as e:
        return None, f"❌ Lỗi: {str(e)}"
```

### Bước 5: Nút Xuất Trong Gradio

```python
with gr.Tab("📊 Danh Sách Phiếu"):
    # ... UI elements ...

    btn_csv = gr.Button("📥 Xuất CSV")
    btn_excel = gr.Button("📊 Xuất Excel")

    btn_csv.click(
        fn=xuat_csv,
        inputs=state,
        outputs=[gr.File(), output_msg]
    )

    btn_excel.click(
        fn=xuat_excel,
        inputs=state,
        outputs=[gr.File(), output_msg]
    )
```

---

## 🔄 Flow: Nhập → Tính → Xuất

```
┌─────────────────────────────────────────────────────────────┐
│ USER NHẬP THÔNG TIN PHIẾU (18 FIELD)                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ CLICK "➕ THÊM VÀO PHIẾU"                                    │
│ • Validation dữ liệu                                        │
│ • Tính Thành tiền = SL × Đơn giá                            │
│ • Tính VT 30% = Doanh thu × 0.30                            │
│ • Thêm vào state (DataFrame)                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STATE ĐƯỢC UPDATE                                           │
│ state = pd.concat([state, new_row], ignore_index=True)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ VIEW TAB 2: DANH SÁCH PHIẾU                                 │
│ • Hiển thị tất cả dòng trong state                          │
│ • Có thể xóa dòng, làm mới                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ CLICK "📥 XUẤT CSV" HOẶC "📊 XUẤT EXCEL"                   │
│ • ReportExporter nhận state                                 │
│ • Tính toán thống kê                                        │
│ • Tạo file (.xlsx hoặc .csv)                                │
│ • Trả về file path & message                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ FILE ĐƯỢC TẢI VỀ                                            │
│ Phieu_xuat_VT_05_02_2026_153045.xlsx                        │
│ Phieu_xuat_VT_05_02_2026_153045.csv                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 State Management

### Khởi Tạo
```python
state = gr.State(value=None)
```

### Update State
```python
# Thêm dòng
state_df = pd.concat([state_df, pd.DataFrame([new_row])], ignore_index=True)

# Xóa dòng cuối
state_df = state_df.iloc[:-1]

# Làm mới
state_df = None
```

### Truy Cập State
```python
# Trong Gradio function
def my_function(state_df):
    if state_df is None:
        return "Không có dữ liệu"
    return len(state_df)  # Số dòng
```

---

## ✅ Testing

### Test Xuất CSV
```python
df_test = pd.DataFrame({...})  # 18 columns
exporter = ReportExporter(df_test)
exporter.xuat_csv('test.csv')
assert Path('test.csv').exists()
print("✅ CSV export OK")
```

### Test Xuất Excel
```python
df_test = pd.DataFrame({...})  # 18 columns
exporter = ReportExporter(df_test)
exporter.xuat_phieu_excel('test.xlsx')
assert Path('test.xlsx').exists()

from openpyxl import load_workbook
wb = load_workbook('test.xlsx')
assert len(wb.sheetnames) == 4
print("✅ Excel export OK")
```

---

## 🐛 Troubleshooting

**Q: File không download**
- A: Kiểm tra: `gr.File()` output binding
- A: Kiểm tra file path trả về

**Q: Excel lỗi encoding**
- A: Dùng: `openpyxl>=3.10.0`
- A: Kiểm tra unicode characters

**Q: State bị null**
- A: Kiểm tra: Nhập phiếu thành công trước?
- A: Kiểm tra: Button click binding

---

**Happy integrating! 🚀**
