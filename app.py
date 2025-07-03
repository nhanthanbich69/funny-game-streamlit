import streamlit as st
import random
import time

# Tiêu đề ứng dụng
st.title("🎮 **Game Tùy Chọn** (Đoán Số - Búa Kéo Bao - Tung Xúc Xắc - Tung Đồng Xu)")

# Tạo các tab
tabs = st.tabs(["🎯 Đoán Số", "🖐 Búa Kéo Bao", "🎲 Tung Xúc Xắc", "🪙 Tung Đồng Xu", "📝 Hướng Dẫn", "📊 Kết Quả"])

import random
import streamlit as st

# Khởi tạo các danh sách câu trả lời đúng và sai
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

# Tab Đoán Số
with st.container():
    st.header("🎯 **Đoán Số Bí Mật (10 lượt đoán)**", anchor="top")

    # Các chế độ chơi (dễ, trung bình, khó)
    level = st.selectbox("⚡️ Chọn chế độ chơi", ["Dễ (0~30)", "Trung Bình (0~100)", "Khó (0~500)"])

    max_num = {"Dễ (0~30)": 30, "Trung Bình (0~100)": 100, "Khó (0~500)": 500}[level]
    secret_number = random.randint(0, max_num)  # Cho phép chọn số 0

    # Biến lưu trữ số lần đoán
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'clues' not in st.session_state:
        st.session_state.clues = []  # Manh mối

    # Lựa chọn câu hỏi
    question_type = st.radio("❓ **Bạn muốn hỏi về số bí mật thế nào?**", 
                             ("Số đó có lớn hơn một con số?", "Số đó có bé hơn một con số?"),
                             index=0, horizontal=True)  # Horizontal layout for the options

    # Xử lý câu hỏi
    try:
        if question_type == "Số đó có lớn hơn một con số?":
            number = st.slider("🚀 Chọn một số bạn muốn hỏi", 0, max_num)  # Allow 0 as a valid number
            question = f"Số bí mật có phải lớn hơn {number} không?"
        elif question_type == "Số đó có bé hơn một con số?":
            number = st.slider("🌟 Chọn một số bạn muốn hỏi", 0, max_num)  # Allow 0 as a valid number
            question = f"Số bí mật có phải bé hơn {number} không?"
    except Exception as e:
        st.error(f"⚠️ Lỗi khi tạo câu hỏi: {e}")

    # Kiểm tra và phản hồi câu hỏi
    if st.button("🕵️‍♂️ **Hỏi**"): 
        st.session_state.attempts += 1

        if st.session_state.attempts > 10:
            st.error(f"😞 **Bạn đã hết lượt đoán rồi!** Số bí mật là {secret_number}. Bạn thua rồi! 😭")
            st.session_state.attempts = 0
            st.session_state.clues = []  # Reset manh mối
        else:
            response = ""
            clue = ""

            try:
                if "lớn hơn" in question:
                    number = int(''.join(filter(str.isdigit, question.split("lớn hơn")[1].strip())))
                    if secret_number > number:
                        response = random.choice(correct_responses)
                        clue = f"Số đó lớn hơn {number}."
                    else:
                        response = random.choice(incorrect_responses)
                        clue = f"Số đó bé hơn {number}."
                elif "bé hơn" in question:
                    number = int(''.join(filter(str.isdigit, question.split("bé hơn")[1].strip())))
                    if secret_number < number:
                        response = random.choice(correct_responses)
                        clue = f"Số đó bé hơn {number}."
                    else:
                        response = random.choice(incorrect_responses)
                        clue = f"Số đó lớn hơn {number}."
            except (IndexError, ValueError) as e:
                st.error(f"⚠️ Lỗi trong việc xử lý câu hỏi: {e}")

            if response:
                # Kiểm tra manh mối trùng lặp trước khi lưu
                if clue not in st.session_state.clues:
                    st.session_state.clues.append(clue)  # Lưu manh mối
                st.write(f"**Câu hỏi:** {question}")
                st.write(f"**Trả lời:** {response}")
                st.write(f"**Manh mối:** {clue}")  # Hiển thị manh mối

    # Hiển thị các manh mối đã rút ra
    if st.session_state.clues:
        st.subheader("🕵️‍♂️ **Các manh mối bạn đã rút ra:**")
        for clue in st.session_state.clues:
            st.write(f"- {clue}")

    # Hiển thị phần nhập số
    if st.session_state.attempts > 0 and st.session_state.attempts <= 10:
        st.subheader("🔒 **Chốt số**")

        user_guess = st.number_input(f"Bạn chắc số bí mật là (0-{max_num}) chưa? Nghĩ kỹ đi -))", min_value=0, max_value=max_num, step=1)

        # Khởi tạo confirm nếu chưa có
        confirm = None
        if user_guess is not None:
            confirm = st.radio(
                f"Bạn chắc chắn số bí mật là {user_guess} chưa?",
                ["✔️ Chắc chắn", "❌ Tôi cần suy nghĩ thêm"]
            )

        # Kiểm tra kết quả khi chọn "Chắc chắn"
        if confirm == "✔️ Chắc chắn":
            if user_guess == secret_number:
                st.success(f"🎉 **Wao, thật đẹp trai!** Bạn đoán đúng số {secret_number}! Quá đỉnh luôn!")
            else:
                st.error(f"😞 **Rất tiếc!** Số bí mật là {secret_number}. Bạn đã thua! 😭")
        elif confirm == "❌ Tôi cần suy nghĩ thêm":
            st.info("Bạn có thể tiếp tục trò chơi và thử lại!")

    # Reset lại sau khi kết thúc trò chơi
    if st.session_state.attempts > 10 or confirm == "✔️ Chắc chắn":
        st.session_state.attempts = 0
        st.session_state.clues = []
        
# Tab Búa Kéo Bao
with tabs[1]:
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

# Tab Tung Xúc Xắc
with tabs[2]:
    st.header("🎲 **Tung Xúc Xắc**")

    num_dice = st.slider("🔢 Chọn số lượng xúc xắc", min_value=1, max_value=5, value=1)
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

# Tab Tung Đồng Xu
with tabs[3]:
    st.header("🪙 **Tung Đồng Xu**")

    num_coins = st.selectbox("🍀 **Chọn số lượng đồng xu**", [1, 2, 4])

    if st.button("🪙 **Tung Đồng Xu**"):
        try:
            with st.spinner("Đang tung đồng xu... 🪙"):
                time.sleep(3)

            results = ["Mặt Sấp" if random.choice([True, False]) else "Mặt Ngửa" for _ in range(num_coins)]
            st.write(f"Kết quả tung {num_coins} đồng xu: {results}")
        except Exception as e:
            st.error(f"⚠️ Lỗi khi tung đồng xu: {e}")

# Tab Hướng Dẫn
with tabs[4]:
    st.header("📝 **Hướng dẫn chơi**")
    st.write("""
    - **Đoán Số**: Bạn sẽ đoán một số bí mật trong phạm vi cho trước.
    - **Búa Kéo Bao**: Bạn chọn giữa "Bao", "Búa", và "Kéo" và so kết quả với máy.
    - **Tung Xúc Xắc**: Chọn số lượng xúc xắc và loại xúc xắc rồi xem kết quả.
    - **Tung Đồng Xu**: Chọn số lượng đồng xu và xem kết quả tung (1, 2 hoặc 4 đồng xu).
    """)
