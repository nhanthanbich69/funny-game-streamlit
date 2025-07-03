import random
import time
import streamlit as st

# Tiêu đề ứng dụng
st.title("🎮 **Game Tùy Chọn** (Đoán Số - Búa Kéo Bao - Tung Xúc Xắc - Tung Đồng Xu)")

# Thêm CSS để tạo hiệu ứng hover cho các nút
st.markdown("""
    <style>
        .stButton > button:hover {
            background-color: #FFD700;
            color: white;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Tạo các tab
tabs = st.tabs(["📝 Hướng Dẫn", "🎯 Đoán Số", "🖐 Búa Kéo Bao", "🎲 Tung Xúc Xắc", "🪙 Tung Đồng Xu", "📊 Kết Quả"])

# 🎯 Các câu trả lời đúng & sai
correct_responses = [
    "🎯 Đúng rồi! Đỉnh!",
    "🔥 Wow, chuẩn rồi!",
    "🚀 Đúng phết!",
    "😎 Chính xác!",
    "💥 Chính xác luôn!",
    "🎉 Đỉnh cao!",
    "🌟 Quá chuẩn!"
]

incorrect_responses = [
    "😅 Ôi không, sai rồi!",
    "🤔 Hơi sai rồi, thử lại đi!",
    "💔 Không phải rồi, tiếp đi!",
    "🙃 Cố lên, thử lại nhé!",
    "😜 Lại sai rồi, nhưng đừng bỏ cuộc!",
    "😞 Gần đúng rồi, thử lại lần nữa!",
    "😢 Sai rồi, tiếp tục cố gắng!"
]

# Tab Hướng Dẫn
with tabs[0]:
    st.header("📝 **Hướng dẫn chơi**")
    st.write("""
    - **Đoán Số**: Bạn sẽ đoán một số bí mật trong phạm vi cho trước.
    - **Búa Kéo Bao**: Bạn chọn giữa "Bao", "Búa", và "Kéo" và so kết quả với máy.
    - **Tung Xúc Xắc**: Chọn số lượng xúc xắc và loại xúc xắc rồi xem kết quả.
    - **Tung Đồng Xu**: Chọn số lượng đồng xu và xem kết quả tung (1, 2 hoặc 4 đồng xu).
    """)

# 🎯 Đoán Số
with tabs[1]:
    st.header("🎯 **Đoán Số Bí Mật (10 lượt đoán)**")
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'clues' not in st.session_state:
        st.session_state.clues = []
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = None
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0  # Biến đếm số câu hỏi đã hỏi

    # 🎮 Chọn độ khó
    level = st.selectbox("⚡️ Chọn chế độ chơi", ["Thường (0~99)", "Khó (0~300)", "Bậc thầy (0~1000)"])
    max_num = {"Thường (0~99)": 99, "Khó (0~300)": 300, "Bậc thầy (0~1000)": 1000}[level]

    # 🎰 Random số bí mật khi bắt đầu hoặc sau khi đổi độ khó
    if st.session_state.secret_number is None or st.session_state.get('last_max_num') != max_num:
        st.session_state.secret_number = random.randint(0, max_num)
        st.session_state.last_max_num = max_num

    # ❓ Chọn loại câu hỏi
    if st.session_state.attempts < 10:  # Chỉ hiển thị phần hỏi khi còn lượt hỏi
        question_type = st.radio("❓ **Bạn muốn hỏi về số bí mật thế nào?**",
                                 ("Số đó có lớn hơn một con số?", "Số đó có bé hơn một con số?"),
                                 index=0, horizontal=True)

        number = st.slider("🔍 Chọn số bạn muốn hỏi", 0, max_num)

        # 👇 Hỏi số
        if st.button("🕵️‍♂️ **Hỏi ngay!**"):
            st.session_state.attempts += 1
            st.session_state.question_count += 1  # Tăng số câu hỏi đã hỏi

            response = ""
            clue = ""
            
            if question_type == "Số đó có lớn hơn một con số?":
                if st.session_state.secret_number > number:
                    response = random.choice(correct_responses)
                    clue = f"Số đó lớn hơn {number}."
                else:
                    response = random.choice(incorrect_responses)
                    clue = f"Số đó bé hơn hoặc bằng {number}."
            elif question_type == "Số đó có bé hơn một con số?":
                if st.session_state.secret_number < number:
                    response = random.choice(correct_responses)
                    clue = f"Số đó bé hơn {number}."
                else:
                    response = random.choice(incorrect_responses)
                    clue = f"Số đó lớn hơn hoặc bằng {number}."

            st.write(f"**Câu hỏi:** {question_type} {number}?")
            st.write(f"**Trả lời:** {response}")
            st.write(f"**Manh mối:** {clue}")
            if clue not in st.session_state.clues:
                st.session_state.clues.append(clue)

        # 📜 Hiển thị manh mối đã thu thập
        if st.session_state.clues:
            st.subheader("🕵️‍♂️ **Các manh mối bạn đã rút ra:**")
            for clue in st.session_state.clues:
                st.write(f"- {clue}")

    else:
        st.warning("🚨 **Hết lượt hỏi! Bây giờ bạn chỉ có thể đoán số bí mật.**")

    # 🔒 Chốt số với nút bấm
    if 0 < st.session_state.attempts <= 10:
        st.subheader(f"🔒 **Chốt số** (Câu hỏi {st.session_state.question_count}/10)")
        user_guess = st.number_input(f"Bạn nghĩ số bí mật là (0 - {max_num}):", min_value=0, max_value=max_num, step=1)

        # Chốt kết quả
        if st.button("🎯 **Chốt số ngay!**"):
            if user_guess == st.session_state.secret_number:
                st.success(f"🎉 **Wao, thật đẹp trai!** Bạn đoán đúng số {st.session_state.secret_number}! Quá đỉnh luôn!")
            else:
                st.error(f"😞 **Rất tiếc!** Số bí mật là {st.session_state.secret_number}. Bạn đã thua! 😭")
            # Reset sau khi chốt
            st.session_state.secret_number = random.randint(0, max_num)
            st.session_state.attempts = 0
            st.session_state.clues = []
            st.session_state.question_count = 0  # Reset số câu hỏi
            
# 🖐 Búa Kéo Bao
with tabs[2]:
    st.header("🖐 **Búa Kéo Bao**")
    col1, col2, col3 = st.columns(3)

    if 'player_choice' not in st.session_state:
        st.session_state.player_choice = None

    try:
        with col1:
            if st.button("✊ Búa"):
                st.session_state.player_choice = "Búa"
        with col2:
            if st.button("✋ Bao"):
                st.session_state.player_choice = "Bao"
        with col3:
            if st.button("✌️ Kéo"):
                st.session_state.player_choice = "Kéo"
    except Exception as e:
        st.error(f"⚠️ Lỗi khi chọn Búa, Bao, Kéo: {e}")

    # Máy tính chọn ngẫu nhiên Búa, Bao hoặc Kéo
    computer_choice = random.choice(["Búa", "Bao", "Kéo"])

    if st.button("💥 **Kết quả**"):
        try:
            with st.spinner("Kết quả chính là... 🕹️"):
                time.sleep(3)

            if st.session_state.player_choice:
                # Kiểm tra kết quả
                if st.session_state.player_choice == computer_choice:
                    st.write(f"Máy chọn {computer_choice}. **Hòa rồi!** 😎 Thử lại xem!")
                elif (st.session_state.player_choice == "Búa" and computer_choice == "Kéo") or \
                     (st.session_state.player_choice == "Kéo" and computer_choice == "Bao") or \
                     (st.session_state.player_choice == "Bao" and computer_choice == "Búa"):
                    st.write(f"Máy chọn {computer_choice}. **Bạn thắng rồi!** 🎉 Chúc mừng bạn!")
                else:
                    st.write(f"Máy chọn {computer_choice}. **Bạn thua rồi!** 😭 Cố lên lần sau!")
            else:
                st.error("⚠️ Bạn chưa chọn Búa, Bao hoặc Kéo! Vui lòng chọn trước khi xem kết quả.")
        except Exception as e:
            st.error(f"⚠️ Lỗi khi tính kết quả: {e}")

# 🎲 Tung Xúc Xắc
with tabs[3]:
    st.header("🎲 **Tung Xúc Xắc**")

    num_dice = st.slider("🔢 Chọn số lượng xúc xắc", min_value=1, max_value=4, value=1)
    dice_type = st.selectbox("🎲 Chọn loại xúc xắc", ["4 mặt", "6 mặt", "8 mặt", "10 mặt", "12 mặt", "20 mặt", "100 mặt"])

    dice_faces = {"4 mặt": 4, "6 mặt": 6, "8 mặt": 8, "10 mặt": 10, "12 mặt": 12, "20 mặt": 20, "100 mặt": 100}
    sides = dice_faces[dice_type]

    if st.button("🎲 **Tung Xúc Xắc**"):
        try:
            with st.spinner("Đang tung xúc xắc... 🎰"):
                time.sleep(3)

            results = [random.randint(1, sides) for _ in range(num_dice)]
            st.write(f"Kết quả tung {num_dice} xúc xắc {sides} mặt: {results}")
        except Exception as e:
            st.error(f"⚠️ Lỗi khi tung xúc xắc: {e}")

# 🪙 Tung Đồng Xu
with tabs[4]:
    st.header("**Tung Đồng Xu**")

    num_coins = st.selectbox("🍀 **Chọn số lượng đồng xu**", [1, 2, 4])

    if st.button("**Tung Đồng Xu**"):
        try:
            with st.spinner("Đang tung đồng xu... "):
                time.sleep(3)

            results = ["Mặt Sấp" if random.choice([True, False]) else "Mặt Ngửa" for _ in range(num_coins)]
            st.write(f"Kết quả tung {num_coins} đồng xu: {results}")
        except Exception as e:
            st.error(f"⚠️ Lỗi khi tung đồng xu: {e}")
