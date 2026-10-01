import streamlit as st
from datetime import datetime
st.image("Trasua.jpg")

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

# Khởi tạo giỏ hàng trong session_state để lưu các món đã thêm
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- PHẦN NHẬP THÔNG TIN VÀ CHỌN MÓN ---
st.subheader("📝 Nhập thông tin đơn hàng")

# Nhập tên khách hàng
ten_khach = st.text_input("Tên khách hàng:", placeholder="Nhập tên của bạn...", key="input_ten")

st.write("---")
st.subheader("🧋 Chọn món trà sữa")

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
        # Sử dụng key động dựa trên tên topping để tránh lỗi xung đột widget
        if st.checkbox(f"{topping} (+{MENU_TOPPING[topping]:,}đ)", key=f"top_{topping}"):
            topping_duoc_chon.append(topping)

# Nút thêm món vào giỏ hàng
if st.button("➕ Thêm món này vào giỏ hàng", type="secondary"):
    # Tính tiền món vừa chọn
    gia_tra_sua = MENU_TRASUA[chon_tra_sua]
    tien_ts = gia_tra_sua * so_luong
    
    tien_top_1_ly = sum([MENU_TOPPING[t] for t in topping_duoc_chon])
    tien_top = tien_top_1_ly * so_luong
    
    thanh_tien_item = tien_ts + tien_top
    
    # Thêm vào giỏ hàng
    st.session_state.cart.append({
        "ten_mon": chon_tra_sua,
        "so_luong": so_luong,
        "muc_duong": muc_duong,
        "topping": topping_duoc_chon.copy(),
        "thanh_tien": thanh_tien_item
    })
    st.success(f"Đã thêm **{so_luong}x {chon_tra_sua}** vào giỏ hàng!")

st.write("---")

# --- HIỂN THỊ GIỎ HÀNG HIỆN TẠI ---
st.subheader(f"🛒 Giỏ hàng của bạn ({len(st.session_state.cart)} loại món)")

if len(st.session_state.cart) > 0:
    for idx, item in enumerate(st.session_state.cart):
        with st.container():
            st.markdown(f"**{idx + 1}. {item['ten_mon']}** (x{item['so_luong']})")
            st.write(f"- Đường: {item['muc_duong']}")
            st.write(f"- Topping: {', '.join(item['topping']) if item['topping'] else 'Không có'}")
            st.write(f"- Thành tiền: **{item['thanh_tien']:,}đ**")
            
            # Nút xóa từng món khỏi giỏ hàng
            if st.button(f"🗑️ Xóa món này", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
            st.write("---")
            
    if st.button("🗑️ Xóa toàn bộ giỏ hàng", type="tertiary"):
        st.session_state.cart = []
        st.rerun()
else:
    st.info("Giỏ hàng của bạn đang trống. Hãy chọn món và bấm 'Thêm món này vào giỏ hàng'.")

# --- XỬ LÝ THANH TOÁN VÀ XUẤT HÓA ĐƠN ---
if st.button("🖩 Tính Tiền và Xuất Hóa Đơn Chung", type="primary"):
    if not ten_khach.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước khi tính tiền!")
    elif len(st.session_state.cart) == 0:
        st.warning("⚠️ Giỏ hàng đang trống, vui lòng thêm ít nhất một món!")
    else:
        # Tính tổng thanh toán tất cả các món trong giỏ
        tong_thanh_toan = sum([item['thanh_tien'] for item in st.session_state.cart])
        thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # --- HIỂN THỊ KẾT QUẢ HÓA ĐƠN ---
        st.success("✅ Đã tạo hóa đơn thành công cho tất cả các món!")
        st.markdown("### 📋 KẾT QUẢ HÓA ĐƠN CHI TIẾT")
        
        # Tạo chuỗi HTML cho hóa đơn hiển thị trên giao diện
        danh_sach_html = ""
        for idx, item in enumerate(st.session_state.cart, 1):
            topping_str = ', '.join(item['topping']) if item['topping'] else 'Không có'
            danh_sach_html += f"""
            <p><b>{idx}. {item['ten_mon']}</b> (x{item['so_luong']})<br>
            &nbsp;&nbsp;&nbsp;&nbsp;+ Đường: {item['muc_duong']}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;+ Topping: {topping_str}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<b>Thành tiền: {item['thanh_tien']:,}đ</b></p>
            """

        hoa_don_html = f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd; color: #333;">
            <h3 style="text-align: center; color: #e83e8c; margin-bottom: 5px;">QUÁN TRÀ SỮA HAPPY</h3>
            <p style="text-align: center; font-size: 12px; color: #666;">Địa chỉ: 123 Đường Sữa, TP. Hồ Chí Minh<br>Thời gian: {thoi_gian}</p>
            <hr style="border: 0.5px dashed #ccc;">
            <p><b>Tên khách hàng:</b> {ten_khach}</p>
            <p><b>Danh sách các món đã đặt:</b></p>
            {danh_sach_html}
            <hr style="border: 0.5px dashed #ccc;">
            <h2 style="text-align: right; color: #d63384;">TỔNG THANH TOÁN: {tong_thanh_toan:,}đ</h2>
            <hr style="border: 0.5px dashed #ccc;">
            <p style="text-align: center; font-style: italic; font-size: 13px;">Cảm ơn quý khách và hẹn gặp lại!</p>
        </div>
        """
        st.markdown(hoa_don_html, unsafe_allow_html=True)

        # --- TẠO NỘI DUNG FILE TXT ĐỂ XUẤT ---
        noi_dung_file = f"""========================================
           QUÁN TRÀ SỮA HAPPY
========================================
Thời gian: {thoi_gian}
Tên khách hàng: {ten_khach}
----------------------------------------
DANH SÁCH MÓN ĐÃ ĐẶT:
"""
        for idx, item in enumerate(st.session_state.cart, 1):
            topping_str = ', '.join(item['topping']) if item['topping'] else 'Không có'
            noi_dung_file += f"""
{idx}. {item['ten_mon']} (Số lượng: {item['so_luong']})
   - Đường: {item['muc_duong']}
   - Topping: {topping_str}
   - Thành tiền: {item['thanh_tien']:,} VNĐ
----------------------------------------"""

        noi_dung_file += f"""
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
