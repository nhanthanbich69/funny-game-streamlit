import random
import time
import streamlit as st

# Tiêu đề ứng dụng
st.title("🎮 **Game Tùy Chọn** (Đoán Số - Búa Kéo Bao - Tung Xúc Xắc - Tung Đồng Xu)")

# Thêm CSS để tạo hiệu ứng hover cho các nút và giữ màu cũ cho các phần khác
st.markdown("""
    <style>
        body {
            background-color: #fff;
            color: #000;
        }
        .stButton > button:hover {
            background-color: #FFD700;
            color: white;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        .stButton > button {
            background-color: #333;
            color: #FFD700;
            border: 2px solid #FFD700;
        }
        .stSlider > div > div {
            background-color: #fff;
            color: #000;
        }
        .stSelectbox > div {
            background-color: #fff;
            color: #000;
        }
        .stTextInput > div {
            background-color: #fff;
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)

# Tạo các tab
tabs = st.tabs(["📝 Hướng Dẫn", "🎯 Đoán Số", "🖐 Búa Kéo Bao", "🎲 Tung Xúc Xắc", "💰 Tung Đồng Xu"])

# 🎯 Các câu trả lời đúng & sai
correct_responses = [
    "🎉 Chính xác!",
    "✅ Ừ đúng rồi đó!",
    "🧠 Có vẻ bạn đang suy luận tốt!",
    "📈 Thông tin này đáng giá đấy!",
    "👌 Đúng thế!"
]

incorrect_responses = [
    "😅 Ôi không, sai rồi!",
    "😜 Không đúng, sai rồi liu liu",
    "🛑 Bạn lạc hướng rồi, nghĩ lại đi!",
    "🙃 Suýt nữa thì đoán đúng rồi, nhưng sai nhá!",
    "🚫 Cẩn thận, thông tin này sai đấy!",
    "💔 Không phải rồi, thử tiếp đi!"
]

# Tab Hướng Dẫn
with tabs[0]:
    st.header("📝 **Hướng dẫn chơi**")
    st.write("""
    - **Đoán Số**: Bạn sẽ đoán một số bí mật trong phạm vi cho trước. Có tối đa 10 lần hỏi để thu hẹp phạm vi.
    - **Búa Kéo Bao**: Bạn chọn giữa "Bao", "Búa", và "Kéo" và so kết quả với máy.
    - **Tung Xúc Xắc**: Chọn số lượng xúc xắc và loại xúc xắc rồi xem kết quả.
    - **Tung Đồng Xu**: Chọn số lượng đồng xu và xem kết quả tung (1, 2 hoặc 4 đồng xu).
    """)

# 🎯 Đoán Số
with tabs[1]:
    st.header("🎯 **Đoán Số Bí Mật (10 lượt hỏi)**")

    # Khởi tạo trạng thái
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = None
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'min_bound' not in st.session_state:
        st.session_state.min_bound = 0
    if 'max_bound' not in st.session_state:
        st.session_state.max_bound = 99
    if 'last_max_num' not in st.session_state:
        st.session_state.last_max_num = 99

    # 🎮 Chọn độ khó
    level = st.selectbox("⚡️ Chọn chế độ chơi", ["Thường (0~99)", "Khó (0~300)", "Bậc thầy (0~1000)"])
    max_num = {"Thường (0~99)": 99, "Khó (0~300)": 300, "Bậc thầy (0~1000)": 1000}[level]

    # 🎰 Reset khi đổi độ khó hoặc mới vào
    if st.session_state.secret_number is None or st.session_state.last_max_num != max_num:
        st.session_state.secret_number = random.randint(0, max_num)
        st.session_state.last_max_num = max_num
        st.session_state.min_bound = 0
        st.session_state.max_bound = max_num
        st.session_state.attempts = 0
        st.session_state.question_count = 0

    # ❓ Nếu còn lượt hỏi
    if st.session_state.attempts < 10:
        question_type = st.radio("❓ **Bạn muốn hỏi gì về số bí mật?**",
                                 ("Số đó lớn hơn hoặc bằng...", "Số đó bé hơn hoặc bằng..."),
                                 index=0, horizontal=True)
        number = st.slider("🔍 Hãy chọn khoảng bạn muốn hỏi", 0, max_num)

        if st.button("🕵️‍♂️ **Hỏi ngay!**"):
            st.session_state.attempts += 1
            st.session_state.question_count += 1

            response = ""
            clue = ""

            secret = st.session_state.secret_number
            min_b = st.session_state.min_bound
            max_b = st.session_state.max_bound

            # Trả lời & cập nhật giới hạn
            if question_type == "Số đó lớn hơn hoặc bằng...":
                if secret >= number:
                    response = random.choice(correct_responses)
                    clue = f"Số đó lớn hơn hoặc bằng {number}."
                    st.session_state.min_bound = max(min_b, number)
                else:
                    response = random.choice(incorrect_responses)
                    clue = f"Số đó bé hơn {number}."
                    st.session_state.max_bound = min(max_b, number - 1)

            elif question_type == "Số đó bé hơn hoặc bằng...":
                if secret <= number:
                    response = random.choice(correct_responses)
                    clue = f"Số đó bé hơn hoặc bằng {number}."
                    st.session_state.max_bound = min(max_b, number)
                else:
                    response = random.choice(incorrect_responses)
                    clue = f"Số đó lớn hơn {number}."
                    st.session_state.min_bound = max(min_b, number + 1)

            # Hiển thị
            st.write(f"**Câu hỏi:** {question_type} {number}?")
            st.write(f"**Trả lời:** {response}")
            st.success(f"🧩 {clue}")

        # 🎯 Hiển thị các manh mối quan trọng nhất (không thừa)
        st.subheader("🧠 **Manh mối bạn đã rút ra:**")
        
        clues = []
        
        if st.session_state.min_bound > 0:
            clues.append(f"Số đó lớn hơn hoặc bằng {st.session_state.min_bound}.")
        
        if st.session_state.max_bound < max_num:
            clues.append(f"Số đó bé hơn hoặc bằng {st.session_state.max_bound}.")
        
        if clues:
            for clue in clues:
                st.write(f"- {clue}")
        else:
            st.info("Bạn chưa có manh mối nào rõ ràng để đoán cả! Bắt đầu đặt câu hỏi thôi nào!")

    else:
        st.warning("🚨 **Hết lượt hỏi rồi má! Mau cho tôi câu trả lời đi.**")

    # 🔒 Đoán số
    if 0 < st.session_state.attempts <= 10:
        st.subheader(f"🔒 **Chốt số** (Câu hỏi {st.session_state.question_count}/10)")
        user_guess = st.number_input(f"Bạn nghĩ số bí mật là (0 - {max_num}):", min_value=0, max_value=max_num, step=1)

        if st.button("🎯 **Chốt số ngay!**"):
            secret = st.session_state.secret_number
            if user_guess == secret:
                st.success(f"🎉 **Wao, thật đẹp trai!** Bạn đoán đúng số {secret}! Quá đỉnh luôn!")
            else:
                st.error(f"😞 **Rất tiếc!** Số bí mật là {secret}. Bạn đã thua! 😭")

            # Tính độ lệch giữa số dự đoán và số bí mật
            difference = abs(user_guess - st.session_state.secret_number)

            # Tính tỷ lệ lệch với phạm vi
            max_diff = max_num  # Phạm vi tối đa tùy vào độ khó
            score_percentage = max(0, 100 - (difference / max_diff) * 100)

            # Tính điểm: điểm càng cao nếu số đoán gần đúng
            remaining_questions = 10 - st.session_state.attempts
            score = int(score_percentage * ((11 + remaining_questions) / 9))
            st.write(f"🎯 **Điểm của bạn**: {score:.2f}")

            # Reset toàn bộ
            st.session_state.secret_number = random.randint(0, max_num)
            st.session_state.min_bound = 0
            st.session_state.max_bound = max_num
            st.session_state.attempts = 0
            st.session_state.question_count = 0
            st.session_state.last_max_num = max_num
            
# 🖐 Búa Kéo Bao
with tabs[2]:
    st.header("🖐 **Búa Kéo Bao**")
    col1, col2, col3 = st.columns(3)

    # Initialize player choice and computer's last move
    if 'player_choice' not in st.session_state:
        st.session_state.player_choice = None
    if 'computer_choice' not in st.session_state:
        st.session_state.computer_choice = None
    if 'previous_result' not in st.session_state:
        st.session_state.previous_result = None

    try:
        # Player choices
        with col1:
            if st.button("✊ Búa", key="bua", help="Búa thắng Kéo", on_click=lambda: setattr(st.session_state, 'player_choice', "Búa")):
                pass
        with col2:
            if st.button("✋ Bao", key="bao", help="Bao thắng Búa", on_click=lambda: setattr(st.session_state, 'player_choice', "Bao")):
                pass
        with col3:
            if st.button("✌️ Kéo", key="keo", help="Kéo thắng Bao", on_click=lambda: setattr(st.session_state, 'player_choice', "Kéo")):
                pass
    except Exception as e:
        st.error(f"⚠️ Lỗi khi chọn Búa, Bao, Kéo: {e}")

    # Máy tính chọn ngẫu nhiên Búa, Bao hoặc Kéo
    if st.session_state.previous_result == 'win':
        computer_choice = st.session_state.computer_choice
    elif st.session_state.previous_result == 'lose':
        if st.session_state.computer_choice == "Búa":
            computer_choice = "Bao"
        elif st.session_state.computer_choice == "Bao":
            computer_choice = "Kéo"
        elif st.session_state.computer_choice == "Kéo":
            computer_choice = "Búa"
    else:
        computer_choice = random.choice(["Búa", "Bao", "Kéo"])

    st.session_state.computer_choice = computer_choice

    if st.button("💥 **Kết quả**"):
        try:
            with st.spinner("Kết quả chính là... 🕹️"):
                time.sleep(1)

            if st.session_state.player_choice:
                if st.session_state.player_choice == computer_choice:
                    st.session_state.previous_result = 'draw'
                    st.write(f"Máy chọn {computer_choice}. **Hòa rồi!** 😎 Thử lại xem!")
                elif (st.session_state.player_choice == "Búa" and computer_choice == "Kéo") or \
                     (st.session_state.player_choice == "Kéo" and computer_choice == "Bao") or \
                     (st.session_state.player_choice == "Bao" and computer_choice == "Búa"):
                    st.session_state.previous_result = 'win'
                    st.write(f"Máy chọn {computer_choice}. **Bạn thắng rồi!** 🎉 Chúc mừng bạn!")
                else:
                    st.session_state.previous_result = 'lose'
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
                time.sleep(2)

            results = [random.randint(1, sides) for _ in range(num_dice)]
            
            st.subheader("🎲 **Kết quả tung xúc xắc**:")
            for i, result in enumerate(results, 1):
                st.write(f"🎲 **Xúc xắc {i}:** Tung được {result} điểm")

            total_score = sum(results)
            avg_score = total_score / num_dice
            st.write(f"🎯 **Tổng điểm**: {total_score}")
            st.write(f"🎯 **Điểm trung bình**: {avg_score:.2f}")
        except Exception as e:
            st.error(f"⚠️ Lỗi khi tung xúc xắc: {e}")

# 💰 Tung Đồng Xu
with tabs[4]:
    st.header("💰 **Tung Đồng Xu**")

    num_coins = st.selectbox("🍀 **Chọn số lượng đồng xu**", [1, 2, 4])

    if st.button("💰 **Tung Đồng Xu**"):
        try:
            with st.spinner("Đang tung đồng xu... "):
                time.sleep(1)

            results = ["Mặt Sấp" if random.choice([True, False]) else "Mặt Ngửa" for _ in range(num_coins)]
            
            st.subheader("💰 **Kết quả tung đồng xu**:")
            for i, result in enumerate(results, 1):
                st.write(f"🔹 **Đồng xu thứ {i}:** {result}")

            if 'coin_history' not in st.session_state:
                st.session_state.coin_history = []
            st.session_state.coin_history.append(results)

            st.subheader("📜 **Lịch sử tung đồng xu**:")
            for i, history in enumerate(st.session_state.coin_history, 1):
                st.write(f"🔹 **Lượt {i}:** {history}")

        except Exception as e:
            st.error(f"⚠️ Lỗi khi tung đồng xu: {e}")
