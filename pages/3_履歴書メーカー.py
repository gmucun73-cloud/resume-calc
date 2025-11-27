import streamlit as st
from datetime import date
import time

# --- 6.1 シニア・アクセシビリティ対応（CSS注入） ---
# 文字サイズ、ボタンの大きさ、配色のコントラスト比を調整
st.markdown("""
    <style>
    /* 全体の文字サイズを拡大 (18px) */
    html, body, [class*="css"] {
        font-family: "Hiragino Sans", "Meiryo", sans-serif;
        font-size: 18px !important;
        line-height: 1.8 !important;
        color: #333333;
    }
    /* ボタンを指で押しやすく巨大化 (高さ50px以上) */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        font-weight: bold;
        background-color: #E8F5E9; /* 目に優しい薄緑 */
        border: 2px solid #2E7D32;
        color: #2E7D32;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background-color: #2E7D32;
        color: white;
    }
    /* 入力エリアの強調 */
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 15px;
    }
    /* 見出しのデザイン */
    h1, h2, h3 {
        color: #2E7D32 !important; /* 濃い緑で視認性確保 */
    }
    </style>
    """, unsafe_allow_html=True)

# ページ設定
st.title("かんたん履歴書メーカー")
st.markdown("**文字を打つ必要はありません。ボタンを選ぶだけで、立派な書類が完成します。**")

# --- セッション管理（画面遷移してもデータを保持） ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}

# --- 進捗バー（4.2 認知的負荷軽減） ---
progress = (st.session_state.step / 3) * 100
st.progress(int(progress))
st.caption(f"ステップ {st.session_state.step} / 3")

# ==========================================
# STEP 1: 基本情報と状況確認
# ==========================================
if st.session_state.step == 1:
    st.header("1. あなたの状況を教えてください")
    
    # 5.1 コンポーネントA：きっかけ・背景
    trigger = st.radio("介護・福祉の仕事をしようと思った理由は？", [
        "A-1. 家族の介護経験があり、役に立ちたいと思った",
        "A-2. 以前のボランティアで「ありがとう」と言われて嬉しかった",
        "A-3. 接客業の経験を活かして、人と深く関わる仕事がしたい",
        "A-4. 手に職をつけて、長く安定して働きたい",
        "A-5. ブランクがあるが、やっぱり介護の仕事が好きで戻りたい"
    ])
    
    # 4.2 施設形態
    facility = st.selectbox("働きたい、または経験のある場所は？", [
        "特別養護老人ホーム（特養）",
        "老人保健施設（老健）",
        "デイサービス（通所介護）",
        "訪問介護（ホームヘルプ）",
        "グループホーム",
        "障害者支援施設（就労支援など）"
    ])

    # 4.1 資格（略称→正式名称変換用）
    qualifications = st.multiselect("持っている資格（複数選べます）", [
        "なし",
        "ヘルパー2級・初任者研修",
        "実務者研修・ヘルパー1級",
        "介護福祉士",
        "社会福祉士",
        "精神保健福祉士",
        "普通自動車免許（AT限定可）"
    ])

    if st.button("次へ進む（強みを選ぶ）"):
        st.session_state.resume_data["trigger"] = trigger
        st.session_state.resume_data["facility"] = facility
        st.session_state.resume_data["qualifications"] = qualifications
        st.session_state.step = 2
        st.rerun()

# ==========================================
# STEP 2: 強みと業務経験（5.2 & 5.4）
# ==========================================
elif st.session_state.step == 2:
    st.header("2. あなたの得意なこと")
    
    # 5.2 コンポーネントB：性格・強み
    strength = st.selectbox("自分の性格に近いものは？", [
        "B-1. 傾聴力（じっくり話を聞くのが得意）",
        "B-2. 協調性（チームワークを大切にする）",
        "B-3. 明るさ（職場のムードメーカーになれる）",
        "B-4. 忍耐力（粘り強く対応できる）",
        "B-5. 責任感（任された仕事は最後までやり遂げる）"
    ])
    
    # 5.4 具体的タスク（チェックボックス）
    st.subheader("できること・経験したこと（チェックしてください）")
    col1, col2 = st.columns(2)
    with col1:
        task_physical = st.checkbox("入浴・排泄・食事の介助")
        task_night = st.checkbox("夜勤・見守り")
        task_dementia = st.checkbox("認知症の方の対応")
    with col2:
        task_rec = st.checkbox("レクリエーション企画")
        task_record = st.checkbox("記録・パソコン入力")
        task_drive = st.checkbox("送迎・運転")

    if st.button("次へ進む（文章を作成）"):
        st.session_state.resume_data["strength"] = strength
        st.session_state.resume_data["tasks"] = {
            "physical": task_physical,
            "night": task_night,
            "dementia": task_dementia,
            "rec": task_rec,
            "record": task_record,
            "drive": task_drive
        }
        st.session_state.step = 3
        st.rerun()

# ==========================================
# STEP 3: 生成と確認（5.3 & 出力）
# ==========================================
elif st.session_state.step == 3:
    st.header("3. 文章ができました！")
    
    # --- ロジック実装（マトリクス生成） ---
    data = st.session_state.resume_data
    
    # 志望動機生成
    motivation = "【志望動機】\n"
    
    # Aパーツ（きっかけ）の変換
    if "家族の介護" in data["trigger"]:
        motivation += "家族の介護を経験し、専門的な知識と技術を身につけて社会の役に立ちたいと強く思い、志望いたしました。"
    elif "ボランティア" in data["trigger"]:
        motivation += "以前ボランティア活動に参加した際、利用者様の笑顔に深いやりがいを感じ、これを仕事にしたいと考えました。"
    elif "接客業" in data["trigger"]:
        motivation += "これまで培ったコミュニケーション能力を活かし、一人ひとりと深く関わる福祉の仕事に挑戦したいと考えております。"
    elif "手に職" in data["trigger"]:
        motivation += "高齢化社会を支える介護業界で、専門資格を取得しながら長く腰を据えて働きたいと考え、貴法人を志望しました。"
    elif "ブランク" in data["trigger"]:
        motivation += "一度現場を離れましたが、やはり利用者様と触れ合う介護の仕事のやりがいが忘れられず、復職を決意いたしました。"

    # Bパーツ（強み）の接続
    motivation += "\n\n私の強みは「" + data["strength"].split("（")[0].replace("B-.", "") + "」です。"
    if "傾聴力" in data["strength"]:
        motivation += "利用者様の言葉にならない思いや、些細な表情の変化を汲み取ることを常に心がけています。"
    elif "協調性" in data["strength"]:
        motivation += "チームケアを重視し、多職種との連携をスムーズに行うための報告・連絡・相談を徹底します。"
    elif "明るさ" in data["strength"]:
        motivation += "朝の挨拶や声掛けを大切にし、利用者様や職員が明るくなれる雰囲気作りを行います。"

    # Cパーツ（貢献・まとめ）
    motivation += "\n\n"
    if data["tasks"]["night"]:
        motivation += "体力には自信があり、夜勤業務も含めて柔軟に対応可能です。"
    elif data["tasks"]["drive"]:
        motivation += "送迎業務も安全第一で行い、利用者様の通所をサポートいたします。"
    else:
        motivation += f"貴施設（{data['facility']}）の理念である利用者本位のケアを実践し、一日も早く戦力となれるよう尽力いたします。"

    # 職務要約の生成（タスクに基づく）
    summary = "【職務要約・得意分野】\n"
    tasks_list = []
    if data["tasks"]["physical"]: tasks_list.append("・身体介護（入浴・排泄・食事）による自立支援")
    if data["tasks"]["dementia"]: tasks_list.append("・認知症利用者への受容的・共感的ケアの実践")
    if data["tasks"]["rec"]: tasks_list.append("・季節行事やレクリエーションの企画・運営")
    if data["tasks"]["record"]: tasks_list.append("・PC/タブレットを使用した正確な記録業務")
    
    if not tasks_list:
        summary += "・未経験ですが、研修を通じて基本的な介護技術を積極的に習得します。"
    else:
        summary += "\n".join(tasks_list)

    # 画面表示
    st.success("以下の文章をコピーして使ってください")
    
    st.text_area("志望動機", motivation, height=250)
    st.text_area("職務要約・自己PR", summary, height=150)

    # 資格の正式名称表示（4.1）
    if data["qualifications"] and "なし" not in data["qualifications"]:
        st.info("💡 資格は正式名称で書きましょう：")
        formal_names = []
        for q in data["qualifications"]:
            if "ヘルパー2級" in q: formal_names.append("・介護職員初任者研修 修了（旧ヘルパー2級）")
            elif "実務者" in q: formal_names.append("・介護福祉士実務者研修 修了")
            elif "普通自動車" in q: formal_names.append("・普通自動車第一種運転免許（AT限定）")
            else: formal_names.append(f"・{q} 登録") # 国家資格系
        st.write("\n".join(formal_names))

    # --- アフィリエイト導線 ---
    st.markdown("---")
    st.markdown(f"### 準備ができたら、求人を見てみましょう")
    st.write("作成した志望動機を使って、好条件の職場を探しませんか？")
    # ここにアフィリエイトリンク
    st.markdown("""
        <a href="#" style="
            display: block;
            width: 100%;
            padding: 15px;
            background-color: #FF9800;
            color: white;
            text-align: center;
            text-decoration: none;
            font-weight: bold;
            border-radius: 10px;
            font-size: 20px;">
            👉 {facility} の求人を見る（登録無料）
        </a>
    """, unsafe_allow_html=True)
    
    if st.button("最初からやり直す"):
        st.session_state.step = 1
        st.rerun()
