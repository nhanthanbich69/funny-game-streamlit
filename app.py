import random
import time
import streamlit as st
import difflib
import streamlit.components.v1 as components

# Tiêu đề ứng dụng
st.title("🎮 **Game Tùy Chọn** (Đoán Số - Búa Kéo Bao - Tung Xúc Xắc - Tung Đồng Xu - Nối Từ - Tính nhẩm siêu tốc)")

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

# 🎮 Tạo các tab (thêm Nối Từ ở vị trí tab 5)
tabs = st.tabs([
    "📝 Hướng Dẫn", 
    "🎯 Đoán Số", 
    "🖐 Búa Kéo Bao", 
    "🎲 Tung Xúc Xắc", 
    "💰 Tung Đồng Xu", 
    "🧩 Nối Từ",
    "🧠 Tính nhẩm siêu tốc"
])

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
            
            # Nếu đoán đúng thì cộng thêm điểm từ số lượt hỏi còn lại
            if user_guess == st.session_state.secret_number:
                remaining_questions = 10 - st.session_state.attempts
                score = int(score_percentage * ((11 + remaining_questions) / 9))  # Cộng điểm nếu đoán đúng
            else:
                score = int(score_percentage)  # Giảm điểm tùy theo độ lệch nếu đoán sai
            
            st.write(f"🎯 **Điểm của bạn**: {score}")

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

with tabs[5]:
    st.header("💣 **Nối Từ** 🤘🔥")

    def load_word_list():
        file_paths = [
    "data/tudien.txt",
    "data/tudien1.txt",
    "data/tudien2.txt",
    "data/tudien-master/danhtu.txt",
    "data/tudien-master/danhtunhanxung.txt",
    "data/tudien-master/dongtu.txt",
    "data/tudien-master/lientu.txt",
    "data/tudien-master/photu.txt",
    "data/tudien-master/tagged-1.txt",
    "data/tudien-master/tagged-2.txt",
    "data/tudien-master/tenrieng.txt",
    "data/tudien-master/tinhtu.txt",
    "data/tudien-master/trotu.txt",
    "data/tudien-master/tudien-ast.txt",
    "data/tudien-master/tudien-khongdau.txt"
]
        word_set = set()
        for path in file_paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        word = line.strip().lower()
                        if word:
                            word_set.add(word)
            except FileNotFoundError:
                continue
        return sorted(list(word_set))

    def random_line(lines):
        return random.choice(lines)

    def suggest_similar(word, dictionary):
        prefix = word.split()[0] if ' ' in word else word
        candidates = [w for w in dictionary if w.startswith(prefix[:3])]
        matches = difflib.get_close_matches(word, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    if 'word_dict' not in st.session_state:
        st.session_state.word_dict = load_word_list()
    if 'used_words' not in st.session_state:
        st.session_state.used_words = set()
    if 'word_chain_history' not in st.session_state:
        st.session_state.word_chain_history = []
    if 'invalid_total_count' not in st.session_state:
        st.session_state.invalid_total_count = 0
    if 'invalid_consecutive_in_turn' not in st.session_state:
        st.session_state.invalid_consecutive_in_turn = 0
    if 'last_input' not in st.session_state:
        st.session_state.last_input = ""

    word_dict = st.session_state.word_dict
    used_words = st.session_state.used_words
    history = st.session_state.word_chain_history

    if not word_dict:
        st.error("🚫 Từ điển trống trơn. Upload lẹ lẹ bạn ơi 😤")
        st.stop()

    user_input = st.text_input("💬 **Gõ từ đi idol (nhưng đừng bịa!):**", "").strip().lower()

    if user_input != st.session_state.last_input:
        st.session_state.invalid_consecutive_in_turn = 0
    st.session_state.last_input = user_input

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔁 Chơi lại luôn nè"):
            st.session_state.word_chain_history = []
            st.session_state.used_words = set()
            st.session_state.invalid_total_count = 0
            st.session_state.invalid_consecutive_in_turn = 0
            st.session_state.last_input = ""
            st.rerun()

    with col2:
        if st.button("🚀 Gửi liền tay"):
            if not user_input:
                st.warning(random_line([
                    "😴 Gõ cái gì đi bạn, đừng ngủ gật!",
                    "🤨 Còn trống kìa, viết lẹ đi!",
                    "⛔ Gõ trống là chơi chi?!"
                ]))
            elif user_input in used_words:
                st.error(random_line([
                    "♻️ Từ này xài rồi nha, đừng spam!",
                    "⚠️ Đừng recycle từ cũ chứ!",
                    "😒 Chơi dơ quá, từ đó dùng rồi!"
                ]))
            elif user_input not in word_dict:
                st.session_state.invalid_total_count += 1
                st.session_state.invalid_consecutive_in_turn += 1

                suggestion = suggest_similar(user_input, word_dict)
                if suggestion:
                    st.warning(random_line([
                        f"🤔 Ý bạn là **'{suggestion}'** không? Gõ sai tè le zậy?",
                        f"🧐 Hmm... gần giống **'{suggestion}'**, đánh cho chuẩn nào!",
                        f"🔍 Định viết **'{suggestion}'** hả? Đánh đúng tên đi bạn êi!"
                    ]))
                else:
                    st.error(random_line([
                        f"❌ **'{user_input}'** nghe lạ lắm bạn ơi 😅",
                        f"📕 Từ gì mà không có luôn trong từ điển, bạn chơi chiêu hả?",
                        f"🙃 **'{user_input}'** là hàng fake à? Bot không nhận đâu nha!"
                    ]))

                if st.session_state.invalid_total_count >= 3:
                    turns = len(history) // 2
                    score = int(10 * (1.35 ** max(0, turns - 1)))
                    st.error(random_line([
                        "💀 Ba lần sai là đi luôn nha! Bot nghỉ chơi!",
                        "😵 Quá tam ba bận rồi nha! Bạn out!",
                        "🚫 Sai miết ai chơi nữa! Xử thua!"
                    ]))
                    st.info(f"📉 Điểm an ủi: **{score}** điểm. Tập luyện thêm nhé!")
                    st.stop()
                elif st.session_state.invalid_consecutive_in_turn >= 2:
                    turns = len(history) // 2
                    score = int(10 * (1.35 ** max(0, turns - 1)))
                    st.error(random_line([
                        "📉 Hai lần fail liên tục... buông bàn phím đi bạn 😵",
                        "🤧 2 lần liên tiếp là trượt sấp mặt rồi. Thua nha!",
                        "🙅‍♂️ Trượt 2 lần không cứu được! Game over!"
                    ]))
                    st.info(f"📉 Điểm của bạn: **{score}** điểm.")
                    st.stop()

            elif history:
                st.session_state.invalid_consecutive_in_turn = 0
                last_word = history[-1].split()[-1]
                next_first_word = user_input.split()[0]
                if next_first_word != last_word:
                    st.error(random_line([
                        f"🚫 Phải bắt đầu bằng **'{last_word}'** chứ không phải **'{next_first_word}'**!",
                        f"📛 Gõ sai từ đầu rồi nha. Luật là bắt đầu bằng **'{last_word}'**!",
                        f"⛔ Trật tự rồi! Từ trước là **'{last_word}'**, bạn nhập gì vậy?"
                    ]))
                else:
                    history.append(user_input)
                    used_words.add(user_input)

                    bot_candidates = [w for w in word_dict if w.split()[0] == user_input.split()[-1] and w not in used_words]
                    if bot_candidates:
                        bot_word = random.choice(bot_candidates)
                        history.append(bot_word)
                        used_words.add(bot_word)
                        st.success(random_line([
                            f"🤖 Bot đáp: **{bot_word}**. Vào mood chiến luôn!",
                            f"🔥 Bot gài chiêu: **{bot_word}**. Dám đỡ không?",
                            f"⚡ Bot bắn thẳng: **{bot_word}**. Né không kịp!"
                        ]))
                    else:
                        st.balloons()
                        if len(history) <= 2:
                            st.warning("😒 Mới vô bạn win luôn à? Không vui! Đánh lại từ đầu đi.")
                            history.clear()
                            used_words.clear()
                            st.stop()
                        turns = len(history) // 2
                        score = int(1000 * (0.85 ** (turns - 2)))
                        st.success(random_line([
                            f"🎉 Bot cạn lời! Bạn thắng sau {turns} lượt!",
                            f"🏆 Easy win sau {turns} lượt chơi. Quá đỉnh!",
                            f"💥 Bot out sau {turns} turns. Đỉnh của chóp!"
                        ]))
                        st.info(f"💯 Điểm của bạn: **{score}** điểm")
            else:
                st.session_state.invalid_consecutive_in_turn = 0
                history.append(user_input)
                used_words.add(user_input)

                bot_candidates = [w for w in word_dict if w.split()[0] == user_input.split()[-1] and w not in used_words]
                if bot_candidates:
                    bot_word = random.choice(bot_candidates)
                    history.append(bot_word)
                    used_words.add(bot_word)
                    st.success(random_line([
                        f"🤖 Bot mở hàng bằng: **{bot_word}**. Vô lẹ đi!",
                        f"🎯 Bot quăng nhẹ: **{bot_word}**. Bắt được không?",
                        f"💥 Bot khởi động với: **{bot_word}**. Tới bạn rồi đó!"
                    ]))
                else:
                    st.balloons()
                    st.warning("🤨 Win luôn round đầu là sao trời? Cho bot chơi cái đã chớ!")
                    history.clear()
                    used_words.clear()
                    st.stop()

    if history:
        st.subheader("📜 **Lịch sử đấu khẩu cực gắt:**")
        for i, word in enumerate(history):
            speaker = "🧑‍💻 Bạn" if i % 2 == 0 else "🤖 Bot"
            st.write(f"{i+1}. {speaker}: **{word}**")

    st.caption("📌 *Luật chơi:* Từ mới phải bắt đầu bằng **từ cuối** của từ trước. 3 lần sai là rớt đài, 2 lần sai liên tiếp là auto thua. Bot không tha ai đâu 😈")

with tabs[6]:
    st.header("🧠 **Tính Nhẩm Siêu Tốc** 😤")
    # ---------------- INIT STATE ----------------
    default_state = {
        'math_started': False,
        'math_correct': 0,
        'math_wrong': 0,
        'math_start_time': None,
        'math_time_limit': 15,
        'math_question': "",
        'math_answer': 0,
        'question_index': 0,
        'score_math': 0,
        'math_game_over': False,
        'math_wrong_this_question': 0
    }
    for k, v in default_state.items():
        st.session_state.setdefault(k, v)

    # ---------------- GEN QUESTION ----------------
    def generate_question(index):
        level = index // 10
        index_in_level = index % 10

        def digit_range(d):
            return 10**(d - 1), 10**d - 1

        def increasing_rand_digit(d, step=2):
            base_min, base_max = digit_range(d)
            shift = index_in_level * step
            min_val = base_min + shift
            max_val = min(base_max, base_min + shift + step * 3)
            if min_val > max_val:
                min_val, max_val = base_min, base_max
            return random.randint(min_val, max_val)

        def get_add_digits(level):
            if level == 0:
                return 1, 1
            elif level == 1:
                return 1, 2
            elif level == 2:
                return 2, 2
            elif level == 3:
                return 2, 3
            else:
                return min(3, 1 + level), min(3, 1 + level)

        def get_mul_digits(level):
            if level == 0:
                return None
            elif level == 1:
                return 1, 1
            elif level == 2:
                return 1, 2
            elif level == 3:
                return 2, 2
            else:
                return min(3, level), min(3, level + 1)

        op_pool = (
            ["+"] * 35 + ["-"] * 25 +
            (["*"] * 25 + ["/"] * 15 if level >= 1 else [])
        )
        op = random.choice(op_pool)

        if op in ["+", "-"]:
            d1, d2 = get_add_digits(level)
            a, b = increasing_rand_digit(d1), increasing_rand_digit(d2)
            if op == "+":
                return f"{a} + {b}", a + b
            else:
                return f"{max(a, b)} - {min(a, b)}", abs(a - b)

        elif op == "*":
            d1, d2 = get_mul_digits(level)
            if not d1 or not d2:
                return generate_question(index)
            a, b = increasing_rand_digit(d1), increasing_rand_digit(d2)
            return f"{a} x {b}", a * b

        elif op == "/":
            d1, d2 = get_mul_digits(level)
            if not d1 or not d2:
                return generate_question(index)
            b = increasing_rand_digit(d2)
            result = increasing_rand_digit(d1)
            a = b * result
            return f"{a} : {b}", result

    # ---------------- RESET GAME ----------------
    def reset_game():
        for k in default_state:
            st.session_state[k] = default_state[k]
        st.session_state.math_question, st.session_state.math_answer = generate_question(0)
        st.session_state.math_started = True
        st.session_state.math_start_time = time.time()
        st.rerun()

    # ---------------- TĂNG ĐỘ KHÓ ----------------
    def adjust_difficulty():
        if st.session_state.question_index % 15 == 0:
            st.session_state.math_time_limit = max(3, st.session_state.math_time_limit - 5)
            st.toast(f"🔥 Tăng độ khó! Mỗi câu còn {st.session_state.math_time_limit}s")

    # ---------------- TIMER ----------------
    now = time.time()
    elapsed = now - st.session_state.math_start_time if st.session_state.math_start_time else 0
    remaining = int(st.session_state.math_time_limit - elapsed)

    if not st.session_state.math_game_over and remaining <= 0:
        st.session_state.math_game_over = True

    # ---------------- GAME OVER ----------------
    if st.session_state.math_game_over:
        st.error("💥 Dừng tay! Game over!")
        st.markdown(f"### 🎯 Số câu đúng: **{st.session_state.math_correct}**")
        st.markdown(f"### 🏆 Tổng điểm: **{st.session_state.score_math} điểm**")
        if st.button("🔁 Chơi lại từ đầu"):
            reset_game()
        st.stop()

    # ---------------- GAME START ----------------
    if not st.session_state.math_started:
        if st.button("🚀 Bắt đầu ngay"):
            reset_game()
        st.stop()

    # ---------------- HIỆN ĐỒNG HỒ ----------------
    if remaining <= 3:
        st.warning(f"⚠️ Còn {remaining} giây thôi! Căng rồi nha!!!")

    components.html(f"""
    <script>
    let seconds = {remaining};
    const countdown = setInterval(function() {{
        if (seconds <= 0) {{
            clearInterval(countdown);
        }}
        let clock = document.getElementById("clock");
        if(clock) clock.innerText = "⏳ Còn " + seconds + " giây!";
        seconds -= 1;
    }}, 1000);
    </script>
    <h2 id="clock">⏳ Còn {remaining} giây!</h2>
    """, height=70)

    # ---------------- GAME PLAY ----------------
    st.subheader(f"❓ Câu {st.session_state.question_index + 1}: {st.session_state.math_question}")
    answer = st.text_input("✍️ Nhập kết quả:", key=f"math_answer_{st.session_state.question_index}")

    if st.button("📨 Gửi đáp án"):
        if not answer.strip().isdigit():
            st.warning("🤨 Nhập số đi bạn ơi, đừng troll!")
        else:
            if int(answer.strip()) == st.session_state.math_answer:
                st.success("✅ Chính xác! Não vẫn mượt nha!")
                st.session_state.math_correct += 1
                st.session_state.score_math += 10
                st.session_state.question_index += 1
                adjust_difficulty()
                st.session_state.math_question, st.session_state.math_answer = generate_question(st.session_state.question_index)
                st.session_state.math_start_time = time.time()
                st.session_state.math_wrong_this_question = 0
                st.rerun()
            else:
                st.session_state.math_wrong_this_question += 1
                st.session_state.score_math = max(0, st.session_state.score_math - 4)
                if st.session_state.math_wrong_this_question >= 3:
                    st.session_state.math_game_over = True
                    st.rerun()
                else:
                    st.warning(f"❌ Sai rồi! Còn {3 - st.session_state.math_wrong_this_question} lần thử!")

    st.metric("✅ Số câu đúng", st.session_state.math_correct)
    st.metric("🏆 Tổng điểm", st.session_state.score_math)
