import streamlit as st
import random
import time

# Tiêu đề ứng dụng
st.title("🎮 **Game Tùy Chọn** (Đoán Số - Oẳn Tù Tì - Tung Xúc Xắc - Tung Đồng Xu)")

# Tạo các tab
tabs = st.tabs(["🎯 Đoán Số", "🖐 Oẳn Tù Tì", "🎲 Tung Xúc Xắc", "🪙 Tung Đồng Xu", "📝 Hướng Dẫn", "📊 Kết Quả"])

# Tab Đoán Số
with tabs[0]:
    st.header("🎯 **Đoán Số Bí Mật (10 lượt đoán)**") 

    # Các chế độ chơi (dễ, trung bình, khó)
    level = st.selectbox("⚡️ Chọn chế độ chơi", ["Dễ (0~30)", "Trung Bình (0~100)", "Khó (0~500)"])

    # Xác định phạm vi số cần đoán
    if level == "Dễ (0~30)":
        max_num = 30
    elif level == "Trung Bình (0~100)":
        max_num = 100
    else:
        max_num = 500

    # Tạo một số ngẫu nhiên
    secret_number = random.randint(1, max_num)

    # Biến để lưu trữ số lần đoán và câu hỏi
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []

    # Tạo các lựa chọn câu hỏi với button
    question_type = st.radio(
        "❓ **Bạn muốn hỏi về số bí mật thế nào?**",
        ("Số đó có lớn hơn một con số?", "Số đó có bé hơn một con số?", "Số đó có nằm trong một khoảng số nào đó?")
    )

    # Tạo giao diện câu hỏi
    if question_type == "Số đó có lớn hơn một con số?":
        number = st.slider("🚀 Chọn một số bạn muốn hỏi", 1, max_num)
        question = f"Số bí mật có phải lớn hơn {number} không?"
    elif question_type == "Số đó có bé hơn một con số?":
        number = st.slider("🌟 Chọn một số bạn muốn hỏi", 1, max_num)
        question = f"Số bí mật có phải bé hơn {number} không?"
    elif question_type == "Số đó có nằm trong một khoảng số nào đó?":
        start = st.slider("🔥 Chọn số bắt đầu", 1, max_num - 1)
        end = st.slider("⚡️ Chọn số kết thúc", start + 1, max_num)
        question = f"Số bí mật có nằm trong khoảng từ **{start} đến {end}** không?"

    # Các câu phản hồi đúng và sai
    correct_responses = [
        "🎯 Đúng rồi! Bạn đích thị là thám tử tài ba đấy! 🔥", 
        "🔥 Wow! Bạn đã nhìn ra manh mối rồi! 🎉", 
        "🚀 Chuẩn òi! Bạn quá đẹp trai! 💪", 
        "🧠 Chính nó đó! Sắp win đến nơi rồi! 😎", 
        "💥 Đúng thế! You like siêu nhân giải đố! 💣", 
        "🎉 Chính xác! Bạn đúng là cao thủ! 🌟", 
        "🎯 Bạn khôn đấy -)) Đúng hướng rồi! 🔥" 
    ]
    
    incorrect_responses = [
        "😅 Sai rồi! Câu trả lời không đúng đâu, thử lại nhé!",
        "😢 Sai rồi! Bạn chắc chắn chưa biết số bí mật đâu! 🤷‍♂️",
        "💔 Câu trả lời sai rồi! Đừng lo, thử lại lần sau!",
        "🤔 Sai rồi! Có vẻ bạn đang đi sai hướng, thử lần nữa nhé!",
        "😜 Ôi không, không phải rồi! Số bí mật đâu có thế!",
        "🙃 Sai rồi! Bạn có chắc chưa? Hãy thử thêm lần nữa!",
        "😞 Sai rồi! Đoán lại xem nào, bạn gần hơn rồi đấy!"
    ]

    # Kiểm tra câu hỏi và trả lời
    if st.button("🕵️‍♂️ Hỏi câu"):
        st.session_state.attempts += 1

        if st.session_state.attempts > 10:
            st.error(f"😞 **Bạn đã hết lượt đoán rồi!** Số bí mật là {secret_number}. Bạn thua rồi! 😭")
            # Reset sau khi thua
            st.session_state.attempts = 0
            st.session_state.questions = []
        else:
            response = ""
            # Kiểm tra câu hỏi
            if "lớn hơn" in question:
                number = int(question.split("lớn hơn")[1].strip())
                if secret_number > number:
                    response = random.choice(correct_responses)
                else:
                    response = random.choice(incorrect_responses)
            elif "bé hơn" in question:
                number = int(question.split("bé hơn")[1].strip())
                if secret_number < number:
                    response = random.choice(correct_responses)
                else:
                    response = random.choice(incorrect_responses)
            elif "nằm trong khoảng" in question:
                parts = question.split("nằm trong khoảng")[1].strip()
                start, end = map(int, parts.split("đến"))
                if start <= secret_number <= end:
                    response = random.choice(correct_responses)
                else:
                    response = random.choice(incorrect_responses)

            # Hiển thị câu hỏi và câu trả lời
            st.session_state.questions.append((question, response))
            st.write(f"**Câu hỏi:** {question}")
            st.write(f"**Trả lời:** {response}")
    
    # Hiển thị lịch sử các câu hỏi và câu trả lời
    if st.session_state.questions:
        st.subheader("📜 **Lịch sử các câu hỏi:**")
        for q, r in st.session_state.questions:
            st.write(f"{q} -> {r}")

    # Chốt lại số
    if st.button("🔒 **Chốt số**"):
        user_guess = st.number_input(f"Bạn chắc số bí mật là (1-{max_num}) chưa? Nghĩ kĩ đi -))", min_value=1, max_value=max_num) 
        if user_guess == secret_number:
            st.success(f"🎉 **Wao, thật đẹp trai!** Không ngờ thông minh như bạn mà cũng đoán đúng số {secret_number}! Quá đỉnh luôn!") 
        else:
            st.error(f"😞 **Rất tiếc!** Số bí mật là {secret_number}. Bạn đã thua, chúc bro may mắn lần sau nhá! 😭") 
        # Reset lại sau khi kết thúc trò chơi
        st.session_state.attempts = 0
        st.session_state.questions = []

# Tab Oẳn Tù Tì
with tabs[1]:
    st.header("🖐 **Oẳn Tù Tì**") 

    # Các lựa chọn của người chơi
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✊ Búa"):
            player_choice = "Búa"
    with col2:
        if st.button("✋ Bao"):
            player_choice = "Bao"
    with col3:
        if st.button("✌️ Kéo"):
            player_choice = "Kéo"
    
    # Máy chọn
    computer_choice = random.choice(["Búa", "Bao", "Kéo"])

    # Kết quả
    if st.button("💥 **Kết quả**"): 
        # Hiển thị spinner để loading
        with st.spinner("Kết quả chính là... 🕹️"): 
            time.sleep(3)  # Delay 3 giây

        if player_choice == computer_choice:
            st.write(f"Máy chọn {computer_choice}. **Hòa rồi!** 😎 Thử lại xem!")
        elif (player_choice == "Bao" and computer_choice == "Kéo") or \
             (player_choice == "Búa" and computer_choice == "Bao") or \
             (player_choice == "Kéo" and computer_choice == "Búa"):
            st.write(f"Máy chọn {computer_choice}. **Bạn thắng rồi!** 🎉 Chúc mừng bạn!")
        else:
            st.write(f"Máy chọn {computer_choice}. **Bạn thua rồi!** 😭 Cố lên lần sau!")

# Tab Tung Xúc Xắc
with tabs[2]:
    st.header("🎲 **Tung Xúc Xắc - Chơi là phải chơi lớn!**")

    # Số lượng xúc xắc và loại xúc xắc
    num_dice = st.slider("🔢 Chọn số lượng xúc xắc", min_value=1, max_value=5, value=1)
    dice_type = st.selectbox("🎲 Chọn loại xúc xắc", ["4 mặt", "6 mặt", "8 mặt", "10 mặt", "12 mặt", "20 mặt", "100 mặt"])

    # Đặt số mặt của xúc xắc tương ứng
    dice_faces = {
        "4 mặt": 4,
        "6 mặt": 6,
        "8 mặt": 8,
        "10 mặt": 10,
        "12 mặt": 12,
        "20 mặt": 20,
        "100 mặt": 100
    }
    sides = dice_faces[dice_type]

    # Tung xúc xắc
    if st.button("🎲 **Tung Xúc Xắc**"):
        # Hiển thị spinner để loading
        with st.spinner("Đang tung xúc xắc... 🎰"):
            time.sleep(3)  # Delay 3 giây

        results = [random.randint(1, sides) for _ in range(num_dice)]
        st.write(f"Kết quả tung {num_dice} xúc xắc {sides} mặt: {results}")

# Tab Tung Đồng Xu
with tabs[3]:
    st.header("🪙 **Tung Đồng Xu - Coi chừng đổ rồi đó!**")

    # Chọn số lượng đồng xu
    num_coins = st.selectbox("🍀 **Chọn số lượng đồng xu**", [1, 2, 4])

    # Tung đồng xu
    if st.button("🪙 **Tung Đồng Xu**"):
        # Hiển thị spinner để loading
        with st.spinner("Đang tung đồng xu... 🪙"):
            time.sleep(3)  # Delay 3 giây

        results = ["Mặt Sấp" if random.choice([True, False]) else "Mặt Ngửa" for _ in range(num_coins)]
        st.write(f"Kết quả tung {num_coins} đồng xu: {results}")

# Tab Hướng Dẫn
with tabs[4]:
    st.header("📝 **Hướng dẫn chơi**")
    st.write("""
    - **Đoán Số**: Bạn sẽ đoán một số bí mật trong phạm vi cho trước. Chọn chế độ để thay đổi phạm vi số cần đoán.
    - **Oẳn Tù Tì**: Bạn chọn giữa "Bao", "Búa", và "Kéo" và so kết quả với máy.
    - **Tung Xúc Xắc**: Chọn số lượng xúc xắc và loại xúc xắc (4 mặt, 6 mặt, 8 mặt, 10 mặt, 12 mặt, 20 mặt, 100 mặt...) rồi xem kết quả.
    - **Tung Đồng Xu**: Chọn số lượng đồng xu và xem kết quả tung (1, 2 hoặc 4 đồng xu).
    """)
