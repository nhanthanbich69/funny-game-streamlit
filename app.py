import random
import time
import streamlit as st
import difflib
import json
import streamlit.components.v1 as components

# ⛳ Cấu hình page
st.set_page_config(
    page_title="Game Tùy Chọn",
    layout="wide",  # Hiển thị full màn hình
    initial_sidebar_state="collapsed"  
)

# 🎨 Tuỳ chỉnh CSS nhẹ nhàng để căn giữa trang
st.markdown("""
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .game-container {
            width: 90%;  /* Đặt chiều rộng của game */
            max-width: 1200px; /* Giới hạn chiều rộng tối đa */
            padding: 20px;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
        .stTextInput > div {
            background-color: #fff;
            color: #000;
        }
        .stRadio > div {
            display: flex;
            justify-content: center;
        }
        /* Đảm bảo rằng game sẽ căn giữa ngay cả trên màn hình nhỏ */
        @media (max-width: 768px) {
            .game-container {
                width: 95%;  /* Chiếm 95% màn hình trên điện thoại */
                padding: 10px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# 🌟 Tiêu đề chính
st.title("🎮 **Game Tùy Chọn**")

# 🌟 Hướng dẫn chuyển sang Main Layout (Không dùng Sidebar)
with st.container():
    st.header("📖 **Hướng Dẫn**")
    st.markdown("""
    #### 🎮 Game hiện có:

    - **🎯 Đoán Số** – Đoán số bí mật trong phạm vi 1–100, tối đa 10 lần.
    - **🖐 Búa Kéo Bao** – Chọn 1 trong 3 để đấu bot.
    - **🎲 Tung Xúc Xắc** – Chọn loại và số lượng, xem mặt nào ra.
    - **💰 Tung Đồng Xu** – 1, 2 hoặc 4 đồng xu, thử vận may.
    - **🧩 Nối Từ** – Mỗi từ mới bắt đầu bằng từ cuối trước đó.
    - **🎓 Đố Vui** – Câu hỏi về Việt Nam, mỗi câu 4 đáp án.
    - **🧠 Tính Nhẩm** – Giải nhanh phép tính trong thời gian giới hạn.
    --- 
    👉 Chọn 1 tab bên dưới để bắt đầu chơi!
    """)

# 🧩 Tabs game
tab_names = [
    "🎯 Đoán Số",
    "🖐 Búa Kéo Bao",
    "🎲 Tung Xúc Xắc",
    "💰 Tung Đồng Xu",
    "🧩 Nối Từ",
    "🎓 Đố Vui",
    "🧠 Tính Nhẩm"
]
tabs = st.tabs(tab_names)

# 🎯 Đoán Số
with tabs[0]:
    st.header("🎯 **Đoán Số Bí Mật (10 lượt hỏi)**")

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
with tabs[1]:
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
with tabs[2]:
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
with tabs[3]:
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

with tabs[4]:
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

    # Khởi tạo session state
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
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    word_dict = st.session_state.word_dict
    used_words = st.session_state.used_words
    history = st.session_state.word_chain_history

    if not word_dict:
        st.error("🚫 Từ điển trống trơn. Upload lẹ lẹ bạn ơi 😤")
        st.stop()

    if not st.session_state.game_over:
        user_input = st.text_input("💬 **Gõ từ đi idol (nhưng đừng bịa!):**", "").strip().lower()
        if user_input != st.session_state.last_input:
            st.session_state.invalid_consecutive_in_turn = 0
        st.session_state.last_input = user_input
    else:
        user_input = ""

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔁 Chơi lại luôn nè"):
            st.session_state.word_chain_history = []
            st.session_state.used_words = set()
            st.session_state.invalid_total_count = 0
            st.session_state.invalid_consecutive_in_turn = 0
            st.session_state.last_input = ""
            st.session_state.game_over = False
            st.rerun()

    with col2:
        if not st.session_state.game_over and st.button("🚀 Gửi liền tay"):
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

                if st.session_state.invalid_total_count >= 3 or st.session_state.invalid_consecutive_in_turn >= 2:
                    turns = len(history) // 2
                    score = int(10 * (1.35 ** max(0, turns - 1)))
                    st.error("💀 Bạn out cuộc chơi rồi!")
                    st.info(f"📉 Điểm an ủi: **{score}** điểm.")
                    st.session_state.game_over = True
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
                        turns = len(history) // 2
                        score = int(1000 * (0.85 ** (turns - 2)))
                        st.success(random_line([
                            f"🎉 Bot cạn lời! Bạn thắng sau {turns} lượt!",
                            f"🏆 Easy win sau {turns} lượt chơi. Quá đỉnh!",
                            f"💥 Bot out sau {turns} turns. Đỉnh của chóp!"
                        ]))
                        st.info(f"💯 Điểm của bạn: **{score}** điểm")
                        st.session_state.game_over = True
                        st.stop()
            else:
                # Lượt đầu: kiểm tra nếu từ này khiến bot không phản lại được thì không cho
                bot_candidates = [w for w in word_dict if w.split()[0] == user_input.split()[-1] and w not in used_words]
                if not bot_candidates:
                    st.warning("😑 Từ này dễ thắng quá, bot không phản được. Đánh từ khác đi bạn!")
                    st.stop()

                st.session_state.invalid_consecutive_in_turn = 0
                history.append(user_input)
                used_words.add(user_input)

                bot_word = random.choice(bot_candidates)
                history.append(bot_word)
                used_words.add(bot_word)
                st.success(random_line([
                    f"🤖 Bot mở hàng bằng: **{bot_word}**. Vô lẹ đi!",
                    f"🎯 Bot quăng nhẹ: **{bot_word}**. Bắt được không?",
                    f"💥 Bot khởi động với: **{bot_word}**. Tới bạn rồi đó!"
                ]))

    if history:
        st.subheader("📜 **Lịch sử đấu khẩu cực gắt:**")
        for i, word in enumerate(history):
            speaker = "🧑‍💻 Bạn" if i % 2 == 0 else "🤖 Bot"
            st.write(f"{i+1}. {speaker}: **{word}**")

    st.caption("📌 *Luật chơi:* Từ mới phải bắt đầu bằng **từ cuối** của từ trước. 3 lần sai là rớt đài, 2 lần sai liên tiếp là auto thua. Bot không tha ai đâu 😈")

with tabs[5]:
    st.header("🎓 **Đố Vui Siêu Tốc** ⏱️")

    # ---------------- INIT STATE ----------------
    default_state_quiz = {
        "quiz_data": [],
        "quiz_index": 0,
        "quiz_score": 0,
        "quiz_skipped": [],
        "quiz_finished": False,
        "answered": set()
    }

    for k, v in default_state_quiz.items():
        st.session_state.setdefault(f"quiz_{k}", v)

    # ---------------- LOAD QUESTIONS ----------------
    def load_quiz_data():
        all_questions = []
        filenames = [
            "data/dongvat.txt",
            "data/lichsudialy.txt",
            "data/thucpham.txt",
            "data/thucvat.txt"
        ]
        for filename in filenames:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    questions = json.load(f)
                    all_questions.extend(questions)
            except Exception as e:
                st.warning(f"⚠️ Không thể đọc {filename}: {e}")
        random.shuffle(all_questions)
        return all_questions

    # ---------------- RESET GAME ----------------
    def reset_quiz():
        st.session_state.quiz_data = load_quiz_data()
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_skipped = []
        st.session_state.quiz_finished = False
        st.session_state.answered = set()

    # ---------------- BẮT ĐẦU ----------------
    if not st.session_state.quiz_data:
        reset_quiz()
        st.stop()

    if st.button("🔁 Chơi lại"):
        reset_quiz()
        st.rerun()

    # ---------------- CÂU HỎI HIỆN TẠI ----------------
    questions = st.session_state.quiz_data
    index = st.session_state.quiz_index

    while index in st.session_state.answered and index < len(questions):
        index += 1

    if index >= len(questions):
        if st.session_state.quiz_skipped:
            index = st.session_state.quiz_skipped.pop(0)
        else:
            st.session_state.quiz_finished = True
            st.rerun()

    st.session_state.quiz_index = index
    q = questions[index]

    st.subheader(f"❓ Câu {index + 1}: {q['question']}")

    selected = st.radio(
        "Chọn đáp án:",
        options=["a", "b", "c", "d"],
        format_func=lambda opt: f"{opt.upper()}. {q['options'][opt]}",
        index=None,
        key=f"quiz_radio_{index}"
    )

    # ---------------- GỬI ĐÁP ÁN VÀ BỎ QUA ----------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📨 Gửi đáp án", key=f"submit_{index}"):
            if selected is None:
                st.warning("🤔 Chưa chọn đáp án mà bạn!")
            else:
                correct = q["answer"]
                if selected == correct:
                    st.success("✅ Chính xác! +10 điểm")
                    st.session_state.quiz_score += 10
                else:
                    st.error(f"❌ Sai rồi! Đáp án đúng là **{correct.upper()}. {q['options'][correct]}**")
                st.session_state.answered.add(index)
                st.session_state.quiz_index += 1
                st.rerun()

    with col2:
        if st.button("⏭️ Bỏ qua", key=f"skip_{index}"):
            if index not in st.session_state.quiz_skipped:
                st.session_state.quiz_skipped.append(index)
            st.session_state.quiz_index += 1
            st.rerun()

    # ---------------- GAME OVER ----------------
    if st.session_state.quiz_finished:
        st.error("💥 Hết thời gian!")
        st.markdown(f"### ✅ Số câu đúng: **{st.session_state.quiz_score // 10}**")
        st.markdown(f"### 🏆 Tổng điểm: **{st.session_state.quiz_score} điểm**")
        st.stop()
        
    # Hiển thị kết quả số câu đúng và điểm
    st.metric("✅ Số câu đúng", st.session_state.quiz_score // 10)
    st.metric("🏆 Tổng điểm", st.session_state.quiz_score)
    
with tabs[6]:
    st.header("🎓 **Đố Vui Siêu Tốc** ⏱️")

    # ---------------- INIT STATE ----------------
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = []  # Khởi tạo quiz_data nếu chưa có
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_skipped' not in st.session_state:
        st.session_state.quiz_skipped = []
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None
    if 'quiz_finished' not in st.session_state:
        st.session_state.quiz_finished = False
    if 'answered' not in st.session_state:
        st.session_state.answered = set()

    # ---------------- LOAD QUESTIONS ----------------
    def load_quiz_data():
        all_questions = []
        filenames = [
            "data/dongvat.txt",
            "data/lichsudialy.txt",
            "data/thucpham.txt",
            "data/thucvat.txt"
        ]
        for filename in filenames:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    questions = json.load(f)
                    all_questions.extend(questions)
            except Exception as e:
                st.warning(f"⚠️ Không thể đọc {filename}: {e}")
        random.shuffle(all_questions)
        return all_questions

    # ---------------- RESET GAME ----------------
    def reset_quiz():
        st.session_state.quiz_data = load_quiz_data()  # Đảm bảo quiz_data được load
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_skipped = []
        st.session_state.quiz_start_time = time.time()
        st.session_state.quiz_finished = False
        st.session_state.answered = set()

    # ---------------- BẮT ĐẦU ----------------
    if not st.session_state.quiz_data:
        reset_quiz()

    if st.button("🔁 Chơi lại"):
        reset_quiz()
        st.rerun()

    # ---------------- TIMER ----------------
    now = time.time()
    elapsed = now - st.session_state.quiz_start_time if st.session_state.quiz_start_time else 0
    remaining = int(60 - elapsed)

    if remaining <= 0 and not st.session_state.quiz_finished:
        st.session_state.quiz_finished = True
        st.rerun()

    if st.session_state.quiz_finished:
        st.error("💥 Hết giờ rồi!")
        st.markdown(f"### ✅ Số câu đúng: **{st.session_state.quiz_score // 10}**")
        st.markdown(f"### 🏆 Tổng điểm: **{st.session_state.quiz_score} điểm**")
        st.stop()

    if remaining <= 5:
        st.warning(f"⚠️ Còn {remaining} giây! Nhanh tay nào!!!")
    else:
        st.info(f"⏳ Thời gian còn lại: **{remaining} giây**")

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

    # ---------------- CÂU HỎI HIỆN TẠI ----------------
    questions = st.session_state.quiz_data
    index = st.session_state.quiz_index

    while index in st.session_state.answered and index < len(questions):
        index += 1

    if index >= len(questions):
        if st.session_state.quiz_skipped:
            index = st.session_state.quiz_skipped.pop(0)
        else:
            st.session_state.quiz_finished = True
            st.rerun()

    st.session_state.quiz_index = index
    q = questions[index]

    st.subheader(f"❓ Câu {index + 1}: {q['question']}")

    selected = st.radio(
        "Chọn đáp án:",
        options=["a", "b", "c", "d"],
        format_func=lambda opt: f"{opt.upper()}. {q['options'][opt]}",
        index=None,
        key=f"quiz_radio_{index}"
    )

    # ---------------- GỬI ĐÁP ÁN VÀ BỎ QUA ----------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📨 Gửi đáp án", key=f"submit_{index}"):
            if selected is None:
                st.warning("🤔 Chưa chọn đáp án mà bạn!")
            else:
                correct = q["answer"]
                if selected == correct:
                    st.success("✅ Chính xác! +10 điểm")
                    st.session_state.quiz_score += 10
                else:
                    st.error(f"❌ Sai rồi! Đáp án đúng là **{correct.upper()}. {q['options'][correct]}**")
                st.session_state.answered.add(index)
                st.session_state.quiz_index += 1
                st.rerun()

    with col2:
        if st.button("⏭️ Bỏ qua", key=f"skip_{index}"):
            if index not in st.session_state.quiz_skipped:
                st.session_state.quiz_skipped.append(index)
            st.session_state.quiz_index += 1
            st.rerun()
