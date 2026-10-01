import streamlit as st
from datetime import datetime
from openai import OpenAI

# --- CẤU HÌNH TRANG (PHẢI ĐẶT Ở DÒNG ĐẦU TIÊN CỦA STREAMLIT) ---
st.set_page_config(
    page_title="Hóa Đơn Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# Hiển thị ảnh (nếu có file Trasua.jpg cùng thư mục, nếu không có Streamlit sẽ bỏ qua)
try:
    st.image("Trasua.jpg", use_column_width=True)
except:
    pass

# Tiêu đề ứng dụng
st.markdown("<h1 style='text-align: center; color: #d63384;'>🧋 HÓA ĐƠN TRÀ SỮA & TRỢ LÝ TƯ VẤN AI 🧋</h1>", unsafe_allow_html=True)
st.write("---")

# Định nghĩa bảng giá
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

# Khởi tạo giỏ hàng trong session_state
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Khởi tạo lịch sử chat cho Chatbot trong session_state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Mình là trợ lý AI thông minh của Quán Trà Sữa Happy. Bạn muốn mình tư vấn loại trà sữa hay topping nào phù hợp khẩu vị không?"}
    ]


# ==========================================
# PHẦN 1: TÍCH HỢP CHATBOT DÙNG API KEY
# ==========================================
with st.expander("💬 Trò chuyện với Trợ lý AI tư vấn trà sữa", expanded=False):
    st.write("Hỏi trợ lý AI bất cứ điều gì về menu, công thức hoặc gợi ý món ngon:")
    
    # Cấu hình Client API (Sử dụng OpenRouter / OpenAI API key đã cung cấp)
    # Lưu ý: Nếu dùng khóa OpenRouter, bạn có thể truyền base_url="https://openrouter.ai/api/v1" và dùng model phù hợp như "openai/gpt-4o-mini" hoặc giữ nguyên chuẩn OpenAI nếu là key chính hãng.
    API_KEY = "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"
    
    # Khởi tạo OpenAI client (Hỗ trợ cả OpenRouter hoặc OpenAI)
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://openrouter.ai/api/v1" # Đổi base_url nếu dùng OpenRouter, xóa dòng này nếu dùng key OpenAI trực tiếp
        )
        using_ai = True
    except Exception as e:
        using_ai = False
        st.error(f"Lỗi khởi tạo API: {e}")

    # Hiển thị lịch sử hội thoại
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Nhận câu hỏi từ người dùng qua chat input
    if user_prompt := st.chat_input("Nhập câu hỏi cho AI (VD: Tôi thích uống béo ngọt thì chọn món nào?)..."):
        # Thêm câu hỏi người dùng vào lịch sử hiển thị
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Gọi API lấy câu trả lời từ AI
        with st.chat_message("assistant"):
            with st.spinner("AI đang suy nghĩ..."):
                try:
                    # Thiết lập ngữ cảnh (System prompt) cho nhân viên bán trà sữa AI
                    system_prompt = """Bạn là trợ lý AI thân thiện chuyên tư vấn tại quán 'Quán Trà Sữa Happy'. 
                    Menu trà sữa của quán gồm: 
                    - Trà sữa truyền thống (25,000đ)
                    - Trà sữa chân châu đường đen (35,000đ - Best seller)
                    - Trà sữa matcha (30,000đ)
                    - Trà sữa khoai môn (30,000đ)
                    - Trà sữa ô long (28,000đ)
                    - Hồng trà sữa (25,000đ)
                    
                    Các loại topping (5,000đ - 8,000đ): Trân châu đen, trân châu trắng, thạch phô mai, pudding trứng, trân châu hoàng kim, sương sáo.
                    Mức độ đường tùy chọn: 100%, 70%, 0% (không đường).
                    Hãy tư vấn nhiệt tình, ngắn gọn, lịch sự và phù hợp với khách hàng Việt Nam."""

                    # Chuyển đổi định dạng lịch sử chat gửi lên API
                    messages_payload = [{"role": "system", "content": system_prompt}]
                    for msg in st.session_state.messages:
                        messages_payload.append({"role": msg["role"], "content": msg["content"]})

                    # Gọi model (Sử dụng model mặc định phù hợp với OpenRouter/OpenAI)
                    response = client.chat.completions.create(
                        model="openai/gpt-4o-mini", # Hoặc "gpt-3.5-turbo" tùy thuộc vào key
                        messages=messages_payload,
                        temperature=0.7,
                        max_tokens=300
                    )
                    
                    bot_response = response.choices[0].message.content
                except Exception as e:
                    bot_response = f"⚠️ Không thể kết nối tới AI lúc này. Lỗi chi tiết: {e}"

                st.markdown(bot_response)
                # Lưu phản hồi của AI vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": bot_response})

st.write("---")


# ==========================================
# PHẦN 2: NHẬP THÔNG TIN VÀ CHỌN MÓN (ĐẶT HÀNG NHIỀU LOẠI)
# ==========================================
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
        if st.checkbox(f"{topping} (+{MENU_TOPPING[topping]:,}đ)", key=f"top_{topping}"):
            topping_duoc_chon.append(topping)

# Nút thêm món vào giỏ hàng
if st.button("➕ Thêm món này vào giỏ hàng", type="secondary"):
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


# ==========================================
# PHẦN 3: HIỂN THỊ GIỎ HÀNG HIỆN TẠI
# ==========================================
st.subheader(f"🛒 Giỏ hàng của bạn ({len(st.session_state.cart)} loại món)")

if len(st.session_state.cart) > 0:
    for idx, item in enumerate(st.session_state.cart):
        with st.container():
            st.markdown(f"**{idx + 1}. {item['ten_mon']}** (x{item['so_luong']})")
            st.write(f"- Đường: {item['muc_duong']}")
            st.write(f"- Topping: {', '.join(item['topping']) if item['topping'] else 'Không có'}")
            st.write(f"- Thành tiền: **{item['thanh_tien']:,}đ**")
            
            if st.button(f"🗑️ Xóa món này", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
            st.write("---")
            
    if st.button("🗑️ Xóa toàn bộ giỏ hàng", type="tertiary"):
        st.session_state.cart = []
        st.rerun()
else:
    st.info("Giỏ hàng của bạn đang trống. Hãy chọn món và bấm 'Thêm món này vào giỏ hàng'.")


# ==========================================
# PHẦN 4: XỬ LÝ THANH TOÁN VÀ XUẤT HÓA ĐƠN
# ==========================================
if st.button("🖩 Tính Tiền và Xuất Hóa Đơn Chung", type="primary"):
    if not ten_khach.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước khi tính tiền!")
    elif len(st.session_state.cart) == 0:
        st.warning("⚠️ Giỏ hàng đang trống, vui lòng thêm ít nhất một món!")
    else:
        tong_thanh_toan = sum([item['thanh_tien'] for item in st.session_state.cart])
        thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        st.success("✅ Đã tạo hóa đơn thành công cho tất cả các món!")
        st.markdown("### 📋 KẾT QUẢ HÓA ĐƠN CHI TIẾT")
        
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

        # Tạo nội dung file xuất TXT
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

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Tải xuống file hóa đơn (.txt)",
            data=noi_dung_file,
            file_name=f"HoaDon_{ten_khach.replace(' ', '_')}.txt",
            mime="text/plain"
        )
