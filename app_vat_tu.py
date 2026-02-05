#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ỨNG DỤNG QUẢN LÝ VẬT TƯ KHO SƠN - PHÒNG DỊCH VỤ SƠN
Tháng 01/2026 | Version 1.0
Gradio Web App | 4 Tab chính
"""

import gradio as gr
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
from export_report import ReportExporter

# ═══════════════════════════════════════════════════════════════════════════
# 1. LOAD DỮ LIỆU DANH MỤC & PHÂN BỔ
# ═══════════════════════════════════════════════════════════════════════════

def load_catalog():
    """Load danh mục 30 vật tư từ JSON"""
    try:
        with open('catalog_complete.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('catalog', [])
    except FileNotFoundError:
        gr.Warning("⚠️ Không tìm thấy file catalog_complete.json")
        return []

def load_phan_bo():
    """Load phân bổ vật tư theo 4 tổ từ JSON"""
    try:
        with open('phan_bo_bo_phan.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('phan_bo', {})
    except FileNotFoundError:
        gr.Warning("⚠️ Không tìm thấy file phan_bo_bo_phan.json")
        return {}

# Load dữ liệu
CATALOG = load_catalog()
PHAN_BO = load_phan_bo()

# Tạo dict mã hàng -> giá cho lookup nhanh
PRICE_MAP = {item['ma_hang']: item['don_gia'] for item in CATALOG}
UNIT_MAP = {item['ma_hang']: item['don_vi_tinh'] for item in CATALOG}

# ═══════════════════════════════════════════════════════════════════════════
# 2. HÀM TỪ TÍNH TOÁN
# ═══════════════════════════════════════════════════════════════════════════

def get_ma_hang_list():
    """Lấy danh sách mã hàng cho dropdown"""
    return [f"{item['ma_hang']} - {item['ten_hang']}" for item in CATALOG]

def get_don_gia(ma_hang_full):
    """Lấy đơn giá từ mã hàng (parse từ format: MA - TÊN)"""
    if not ma_hang_full:
        return ""
    try:
        ma_hang = ma_hang_full.split(' - ')[0]
        return PRICE_MAP.get(ma_hang, "")
    except:
        return ""

def tinh_thanh_tien(so_luong, don_gia):
    """Tính thành tiền = SL × Đơn giá"""
    try:
        if so_luong and don_gia:
            return float(so_luong) * float(don_gia)
        return ""
    except:
        return ""

def tinh_vat_tu_30(doanh_thu_bg):
    """Tính vật tư 30% = Doanh thu × 0.30"""
    try:
        if doanh_thu_bg:
            return float(doanh_thu_bg) * 0.30
        return ""
    except:
        return ""

# ═══════════════════════════════════════════════════════════════════════════
# 3. XỬ LÝ PHIẾU (Nhập, Thêm, Xóa)
# ═══════════════════════════════════════════════════════════════════════════

def xu_ly_them_dong_vat_tu(
    state_df,
    stt, cvdv, ngay_thang, so_bg, bks, hieu_xe,
    mau, khach_hang, ten_hang, ma_hang_full,
    so_luong, don_gia, ktv, to, ghi_chu, doanh_thu_bg
):
    """Thêm dòng vật tư vào phiếu"""

    # Validation
    if not all([stt, cvdv, ngay_thang, so_bg, bks, hieu_xe, mau, 
                khach_hang, ten_hang, ma_hang_full, so_luong, don_gia, 
                ktv, to, doanh_thu_bg]):
        return state_df, "❌ Vui lòng điền đầy đủ các trường bắt buộc!"

    try:
        # Parse mã hàng
        ma_hang = ma_hang_full.split(' - ')[0]

        # Tính toán
        thanh_tien = float(so_luong) * float(don_gia)
        vat_tu_30 = float(doanh_thu_bg) * 0.30

        # Tạo dòng mới
        new_row = {
            'STT': int(stt),
            'CVDV': cvdv,
            'Ngày tháng': ngay_thang,
            'Số BG': so_bg,
            'BKS': bks,
            'Hiệu xe': hieu_xe,
            'Màu': mau,
            'Khách hàng': khach_hang,
            'Tên hàng': ten_hang,
            'Mã hàng': ma_hang,
            'Số lượng': float(so_luong),
            'Đơn giá': float(don_gia),
            'Thành tiền': thanh_tien,
            'Vật tư 30%': vat_tu_30,
            'Doanh thu BG': float(doanh_thu_bg),
            'KTV': ktv,
            'Tổ': to,
            'Ghi chú': ghi_chu if ghi_chu else ''
        }

        # Thêm vào DataFrame
        if state_df is None or len(state_df) == 0:
            state_df = pd.DataFrame([new_row])
        else:
            state_df = pd.concat([state_df, pd.DataFrame([new_row])], ignore_index=True)

        msg = f"✅ Thêm thành công! Dòng {len(state_df)}"
        return state_df, msg

    except Exception as e:
        return state_df, f"❌ Lỗi: {str(e)}"

def xoa_dong_cuoi(state_df):
    """Xóa dòng cuối cùng"""
    if state_df is not None and len(state_df) > 0:
        state_df = state_df.iloc[:-1]
        return state_df, "✅ Xóa dòng cuối thành công!"
    return state_df, "❌ Không có dòng để xóa!"

def lam_moi_phieu(state_df):
    """Làm mới phiếu (xóa tất cả)"""
    return None, "✅ Phiếu đã làm mới!"

# ═══════════════════════════════════════════════════════════════════════════
# 4. THỐNG KÊ & BÁO CÁO
# ═══════════════════════════════════════════════════════════════════════════

def tong_hop_bao_cao(state_df):
    """Tổng hợp chỉ số tổng quát"""
    if state_df is None or len(state_df) == 0:
        return """
        | Chỉ số | Giá trị |
        |--------|---------|
        | Tổng vật tư xuất | 0 đ |
        | Tổng vật tư 30% | 0 đ |
        | Tổng doanh thu BG | 0 đ |
        | Số phiếu BG | 0 |
        | Số dòng vật tư | 0 |
        """

    tong_vat_tu = state_df['Thành tiền'].sum()
    tong_vat_tu_30 = state_df['Vật tư 30%'].sum()
    tong_doanh_thu = state_df['Doanh thu BG'].sum()
    so_phieu = state_df['Số BG'].nunique()
    so_dong = len(state_df)

    table = f"""
    | Chỉ số | Giá trị |
    |--------|---------|
    | Tổng vật tư xuất | {tong_vat_tu:,.0f} đ |
    | Tổng vật tư 30% | {tong_vat_tu_30:,.0f} đ |
    | Tổng doanh thu BG | {tong_doanh_thu:,.0f} đ |
    | Số phiếu BG | {so_phieu} |
    | Số dòng vật tư | {so_dong} |
    """
    return table

def thong_ke_theo_to(state_df):
    """Thống kê theo tổ"""
    if state_df is None or len(state_df) == 0:
        return pd.DataFrame()

    stats = state_df.groupby('Tổ').agg({
        'Thành tiền': 'sum',
        'STT': 'count'
    }).reset_index()
    stats.columns = ['Tổ', 'Tổng tiền (đ)', 'Số dòng']
    return stats

def thong_ke_theo_mat_hang(state_df):
    """Thống kê theo mặt hàng"""
    if state_df is None or len(state_df) == 0:
        return pd.DataFrame()

    stats = state_df.groupby(['Mã hàng', 'Tên hàng']).agg({
        'Số lượng': 'sum',
        'Thành tiền': 'sum'
    }).reset_index()
    stats.columns = ['Mã', 'Tên hàng', 'Tổng SL', 'Tổng tiền (đ)']
    return stats

# ═══════════════════════════════════════════════════════════════════════════
# 5. XUẤT FILE
# ═══════════════════════════════════════════════════════════════════════════

def xuat_csv(state_df):
    """Xuất CSV"""
    if state_df is None or len(state_df) == 0:
        return None, "❌ Không có dữ liệu để xuất!"

    try:
        filename = f"Phieu_xuat_VT_{datetime.now().strftime('%d_%m_%Y_%H%M%S')}.csv"
        state_df.to_csv(filename, index=False, encoding='utf-8')
        return filename, f"✅ Xuất CSV: {filename}"
    except Exception as e:
        return None, f"❌ Lỗi xuất CSV: {str(e)}"

def xuat_excel(state_df):
    """Xuất Excel 4 sheet"""
    if state_df is None or len(state_df) == 0:
        return None, "❌ Không có dữ liệu để xuất!"

    try:
        exporter = ReportExporter(state_df)
        filename = f"Phieu_xuat_VT_{datetime.now().strftime('%d_%m_%Y_%H%M%S')}.xlsx"
        exporter.xuat_phieu_excel(filename)
        return filename, f"✅ Xuất Excel: {filename}"
    except Exception as e:
        return None, f"❌ Lỗi xuất Excel: {str(e)}"

# ═══════════════════════════════════════════════════════════════════════════
# 6. DANH MỤC & PHÂN BỔ
# ═══════════════════════════════════════════════════════════════════════════

def get_catalog_table():
    """Bảng danh mục 30 vật tư"""
    if not CATALOG:
        return pd.DataFrame()

    df = pd.DataFrame(CATALOG)
    return df[['loai', 'ma_hang', 'ten_hang', 'don_gia', 'don_vi_tinh']]

def get_phan_bo_table():
    """Bảng phân bổ vật tư theo 4 tổ"""
    if not PHAN_BO:
        return "Không có dữ liệu phân bổ"

    result = "**PHÂN BỔ VẬT TƯ THEO 4 TỔ:**\n\n"
    for to_name, vt_list in PHAN_BO.items():
        result += f"**{to_name}:** {len(vt_list)} VT\n"
        result += f"{', '.join(vt_list)}\n\n"

    return result

# ═══════════════════════════════════════════════════════════════════════════
# 7. TẠO GIAO DIỆN GRADIO
# ═══════════════════════════════════════════════════════════════════════════

def tao_app():
    """Tạo ứng dụng Gradio"""

    # State lưu DataFrame phiếu
    state = gr.State(value=None)

    with gr.Blocks(title="Quản Lý Vật Tư Kho Sơn", theme=gr.themes.Soft()) as demo:

        gr.Markdown("""
        # 🎨 QUẢN LÝ VẬT TƯ KHO SƠN
        ## Phòng Dịch Vụ Sơn | Tháng 01/2026
        """)

        with gr.Tabs():

            # ═════════════════════════════════════════════════════════════
            # TAB 1: NHẬP PHIẾU XUẤT (18 FIELD)
            # ═════════════════════════════════════════════════════════════
            with gr.Tab("📝 Nhập Phiếu Xuất"):
                gr.Markdown("### Nhập thông tin phiếu xuất vật tư (18 trường)")

                with gr.Row():
                    stt = gr.Number(label="STT", value=1)
                    cvdv = gr.Textbox(label="CVDV")
                    ngay_thang = gr.Textbox(label="Ngày tháng")
                    so_bg = gr.Textbox(label="Số BG")

                with gr.Row():
                    bks = gr.Textbox(label="BKS")
                    hieu_xe = gr.Textbox(label="Hiệu xe")
                    mau = gr.Textbox(label="Màu")
                    khach_hang = gr.Textbox(label="Khách hàng")

                with gr.Row():
                    ten_hang = gr.Textbox(label="Tên hàng")
                    ma_hang_full = gr.Dropdown(
                        choices=get_ma_hang_list(),
                        label="Mã hàng (Dropdown)"
                    )

                with gr.Row():
                    so_luong = gr.Number(label="Số lượng")
                    don_gia = gr.Number(label="Đơn giá", interactive=False)
                    ktv = gr.Textbox(label="KTV")

                with gr.Row():
                    to = gr.Dropdown(
                        choices=list(PHAN_BO.keys()),
                        label="Tổ"
                    )
                    ghi_chu = gr.Textbox(label="Ghi chú")
                    doanh_thu_bg = gr.Number(label="Doanh thu BG")

                # Auto tính đơn giá khi chọn mã hàng
                ma_hang_full.change(
                    fn=get_don_gia,
                    inputs=ma_hang_full,
                    outputs=don_gia
                )

                with gr.Row():
                    btn_them = gr.Button("➕ Thêm vào phiếu", variant="primary")
                    btn_lammoi = gr.Button("🔄 Làm mới", variant="secondary")

                output_msg = gr.Textbox(label="Thông báo", interactive=False)

                btn_them.click(
                    fn=xu_ly_them_dong_vat_tu,
                    inputs=[state, stt, cvdv, ngay_thang, so_bg, bks, hieu_xe,
                           mau, khach_hang, ten_hang, ma_hang_full,
                           so_luong, don_gia, ktv, to, ghi_chu, doanh_thu_bg],
                    outputs=[state, output_msg]
                )

                btn_lammoi.click(
                    fn=lam_moi_phieu,
                    inputs=state,
                    outputs=[state, output_msg]
                )

            # ═════════════════════════════════════════════════════════════
            # TAB 2: DANH SÁCH PHIẾU
            # ═════════════════════════════════════════════════════════════
            with gr.Tab("📊 Danh Sách Phiếu"):
                gr.Markdown("### Danh sách tất cả phiếu xuất đã nhập")

                table_phieu = gr.Dataframe(label="Phiếu xuất vật tư")

                with gr.Row():
                    btn_refresh = gr.Button("🔄 Làm mới", variant="secondary")
                    btn_delete = gr.Button("🗑️ Xóa dòng cuối", variant="stop")
                    btn_csv = gr.Button("📥 Xuất CSV", variant="primary")
                    btn_excel = gr.Button("📊 Xuất Excel", variant="primary")

                output_file = gr.Textbox(label="Kết quả xuất file", interactive=False)

                def update_table(df):
                    if df is None or len(df) == 0:
                        return pd.DataFrame()
                    return df

                btn_refresh.click(
                    fn=update_table,
                    inputs=state,
                    outputs=table_phieu
                )

                btn_delete.click(
                    fn=xoa_dong_cuoi,
                    inputs=state,
                    outputs=[state, output_file]
                )

                btn_csv.click(
                    fn=xuat_csv,
                    inputs=state,
                    outputs=[gr.File(), output_file]
                )

                btn_excel.click(
                    fn=xuat_excel,
                    inputs=state,
                    outputs=[gr.File(), output_file]
                )

            # ═════════════════════════════════════════════════════════════
            # TAB 3: THỐNG KÊ & BÁO CÁO
            # ═════════════════════════════════════════════════════════════
            with gr.Tab("📈 Thống Kê & Báo Cáo"):
                gr.Markdown("### Báo cáo tổng hợp chỉ số")

                with gr.Row():
                    btn_thongke = gr.Button("🔄 Cập nhật thống kê", variant="primary")

                # Bảng tóm tắt
                summary_text = gr.Markdown(label="Tóm tắt chỉ số")

                # Bảng theo tổ
                gr.Markdown("#### Thống kê theo Tổ")
                table_to = gr.Dataframe(label="Theo Tổ")

                # Bảng theo mặt hàng
                gr.Markdown("#### Thống kê theo Mặt hàng")
                table_mh = gr.Dataframe(label="Theo Mặt hàng")

                def update_stats(df):
                    summary = tong_hop_bao_cao(df)
                    to_stats = thong_ke_theo_to(df)
                    mh_stats = thong_ke_theo_mat_hang(df)
                    return summary, to_stats, mh_stats

                btn_thongke.click(
                    fn=update_stats,
                    inputs=state,
                    outputs=[summary_text, table_to, table_mh]
                )

            # ═════════════════════════════════════════════════════════════
            # TAB 4: DANH MỤC & PHÂN BỔ
            # ═════════════════════════════════════════════════════════════
            with gr.Tab("📚 Danh Mục & Phân Bổ"):
                gr.Markdown("### Danh mục 30 vật tư & Phân bổ theo 4 tổ")

                gr.Markdown("#### Bảng Danh Mục (30 mặt hàng)")
                table_catalog = gr.Dataframe(
                    value=get_catalog_table(),
                    label="Danh mục vật tư",
                    interactive=False
                )

                gr.Markdown("#### Phân Bổ Vật Tư Theo Tổ")
                phan_bo_md = gr.Markdown(get_phan_bo_table())

    return demo

# ═══════════════════════════════════════════════════════════════════════════
# 8. CHẠY APP
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = tao_app()
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)
