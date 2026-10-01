import streamlit as st
from datetime import datetime
st.image("logo.jpg")

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Hóa Đơn Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# Tiêu đề ứng dụng
st.markdown("<h1 style='text-align: center; color: #d63384;'>🧋 HÓA ĐƠN TRÀ SỮA 🧋</h1>", unsafe_allow_html=True)
st.write("---")

# Định nghĩa bảng giá (có thể tùy chỉnh)
MENU_TRASUA = {
    "Trà sữa truyền thống": 25000,
    "Trà sữa chân châu đường đen": 35000,
    "Trà sữa matcha": 30000,
    "Trà sữa khoai môn": 30000,
    "Trà sữa ô long": 28000,
    "Hồng trà sữa": 25000
}

MENU_TOPPING = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch phô mai": 8000,
    "Pudding trứng": 8000,
    "Trân châu hoàng kim": 6000,
    "Sương sáo": 5000
}

# --- PHẦN NHẬP THÔNG TIN ---
st.subheader("📝 Thông tin đơn hàng")

# Nhập tên khách hàng
ten_khach = st.text_input("Tên khách hàng:", placeholder="Nhập tên của bạn...")

# Chọn loại trà sữa
chon_tra_sua = st.selectbox("Chọn loại trà sữa:", list(MENU_TRASUA.keys()))

# Nhập số lượng
so_luong = st.number_input("Số lượng:", min_value=1, max_value=100, value=1, step=1)

# Chọn mức độ đường
muc_duong = st.radio("Mức độ đường:", ["100% đường", "70% đường", "0% đường (Không đường)"], horizontal=True)

# Chọn Topping (nhiều lựa chọn)
st.write("Chọn Topping thêm (tùy chọn):")
topping_duoc_chon = []
cols = st.columns(2)
for i, topping in enumerate(MENU_TOPPING.keys()):
    with cols[i % 2]:
        if st.checkbox(f"{topping} (+{MENU_TOPPING[topping]:,}đ)", key=topping):
            topping_duoc_chon.append(topping)

st.write("---")

# --- XỬ LÝ TÍNH TOÁN ---
if st.button("🖩 Tính Tiền và Xuất Hóa Đơn", type="primary"):
    if not ten_khach.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước khi tính tiền!")
    else:
        # Tính tiền trà sữa
        gia_tra_sua = MENU_TRASUA[chon_tra_sua]
        tong_tien_tra_sua = gia_tra_sua * so_luong

        # Tính tiền topping (tính cho mỗi phần trà sữa hoặc tổng cộng tùy quy quán, 
        # ở đây tính tổng tiền topping cộng dồn theo số lượng ly)
        tong_tien_topping_1_ly = sum([MENU_TOPPING[t] for t in topping_duoc_chon])
        tong_tien_topping = tong_tien_topping_1_ly * so_luong

        # Tổng thanh toán
        tong_thanh_toan = tong_tien_tra_sua + tong_tien_topping

        # Thời gian hiện tại
        thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # --- HIỂN THỊ KẾT QUẢ ---
        st.success("✅ Đã tạo hóa đơn thành công!")
        
        # Khung hiển thị kết quả giống hóa đơn
        st.markdown("### 📋 KẾT QUẢ HÓA ĐƠN")
        
        hoa_don_html = f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd; color: #333;">
            <h3 style="text-align: center; color: #e83e8c; margin-bottom: 5px;">QUÁN TRÀ SỮA HAPPY</h3>
            <p style="text-align: center; font-size: 12px; color: #666;">Địa chỉ: 123 Đường Sữa, TP. Hồ Chí Minh<br>Thời gian: {thoi_gian}</p>
            <hr style="border: 0.5px dashed #ccc;">
            <p><b>Tên khách hàng:</b> {ten_khach}</p>
            <p><b>Món:</b> {chon_tra_sua} (x{so_luong})</p>
            <p><b>Mức độ đường:</b> {muc_duong}</p>
            <p><b>Topping:</b> {', '.join(topping_duoc_chon) if topping_duoc_chon else 'Không có'}</p>
            <hr style="border: 0.5px dashed #ccc;">
            <p style="text-align: right;"><b>Thành tiền trà sữa:</b> {tong_tien_tra_sua:,}đ</p>
            <p style="text-align: right;"><b>Thành tiền topping:</b> {tong_tien_topping:,}đ</p>
            <h2 style="text-align: right; color: #d63384;">TỔNG CỘNG: {tong_thanh_toan:,}đ</h2>
            <hr style="border: 0.5px dashed #ccc;">
            <p style="text-align: center; font-style: italic; font-size: 13px;">Cảm ơn quý khách và hẹn gặp lại!</p>
        </div>
        """
        st.markdown(hoa_don_html, unsafe_allow_html=True)

        # --- TẠO FILE ĐỂ XUẤT ---
        noi_dung_file = f"""========================================
           QUÁN TRÀ SỮA HAPPY
========================================
Thời gian: {thoi_gian}
Tên khách hàng: {ten_khach}
----------------------------------------
Sản phẩm: {chon_tra_sua}
Số lượng: {so_luong}
Mức độ đường: {muc_duong}
Topping: {', '.join(topping_duoc_chon) if topping_duoc_chon else 'Không có'}
----------------------------------------
Tiền trà sữa: {tong_tien_tra_sua:,} VNĐ
Tiền topping: {tong_tien_topping:,} VNĐ
========================================
TỔNG THANH TOÁN: {tong_thanh_toan:,} VNĐ
========================================
         Cảm ơn quý khách!
"""

        # Nút tải xuống file hóa đơn
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Tải xuống file hóa đơn (.txt)",
            data=noi_dung_file,
            file_name=f"HoaDon_{ten_khach.replace(' ', '_')}.txt",
            mime="text/plain"
        )
