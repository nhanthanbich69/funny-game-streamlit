import streamlit as st
import random
import time

# Tiêu đề ứng dụng
st.title("🎮 **Game Tùy Chọn** (Đoán Số - Búa Kéo Bao - Tung Xúc Xắc - Tung Đồng Xu)")

# Tạo các tab
tabs = st.tabs(["🎯 Đoán Số", "🖐 Búa Kéo Bao", "🎲 Tung Xúc Xắc", "🪙 Tung Đồng Xu", "📝 Hướng Dẫn", "📊 Kết Quả"])

import random
import streamlit as st

# 🎯 Các câu trả lời đúng & sai
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

# 🎲 Khởi tạo trạng thái ban đầu
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'clues' not in st.session_state:
    st.session_state.clues = []
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = None

st.header("🎯 **Đoán Số Bí Mật (10 lượt đoán)**")

# 🎮 Chọn độ khó
level = st.selectbox("⚡️ Chọn chế độ chơi", ["Dễ (0~30)", "Trung Bình (0~100)", "Khó (0~500)"])
max_num = {"Dễ (0~30)": 30, "Trung Bình (0~100)": 100, "Khó (0~500)": 500}[level]

# 🎰 Random số bí mật khi bắt đầu hoặc sau khi đổi độ khó
if st.session_state.secret_number is None or st.session_state.get('last_max_num') != max_num:
    st.session_state.secret_number = random.randint(0, max_num)
    st.session_state.last_max_num = max_num

# ❓ Chọn loại câu hỏi
question_type = st.radio("❓ **Bạn muốn hỏi về số bí mật thế nào?**",
                         ("Số đó có lớn hơn một con số?", "Số đó có bé hơn một con số?"),
                         index=0, horizontal=True)

number = st.slider("🔍 Chọn số bạn muốn hỏi", 0, max_num)

# 👇 Hỏi số
if st.button("🕵️‍♂️ **Hỏi ngay!**"):
    st.session_state.attempts += 1
    if st.session_state.attempts > 10:
        st.error(f"😞 **Bạn đã hết lượt đoán rồi!** Số bí mật là {st.session_state.secret_number}. Bạn thua rồi! 😭")
        st.session_state.secret_number = random.randint(0, max_num)
        st.session_state.attempts = 0
        st.session_state.clues = []
    else:
        if question_type == "Số đó có lớn hơn một con số?":
            if st.session_state.secret_number > number:
                response = random.choice(correct_responses)
                clue = f"Số đó lớn hơn {number}."
            else:
                response = random.choice(incorrect_responses)
                clue = f"Số đó bé hơn hoặc bằng {number}."
        else:
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

# 🔒 Chốt số với nút bấm
if 0 < st.session_state.attempts <= 10:
    st.subheader("🔒 **Chốt số**")
    user_guess = st.number_input(f"Bạn nghĩ số bí mật là (0 - {max_num}):", min_value=0, max_value=max_num, step=1)
    if st.button("🎯 **Chốt số ngay!**"):
        if user_guess == st.session_state.secret_number:
            st.success(f"🎉 **Wao, thật đẹp trai!** Bạn đoán đúng số {st.session_state.secret_number}! Quá đỉnh luôn!")
        else:
            st.error(f"😞 **Rất tiếc!** Số bí mật là {st.session_state.secret_number}. Bạn đã thua! 😭")
        # Reset sau khi chốt
        st.session_state.secret_number = random.randint(0, max_num)
        st.session_state.attempts = 0
        st.session_state.clues = []

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
