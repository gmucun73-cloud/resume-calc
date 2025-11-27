import streamlit as st
from datetime import date
import time

# ==========================================
# 0. シニア・アクセシビリティ設定 (UI/UX)
# ==========================================
st.set_page_config(page_title="福祉職の履歴書メーカー 完全版", layout="centered")

# 要件定義 6.1: フォントサイズ16px以上、コントラスト確保、ボタンサイズ拡大
st.markdown("""
    <style>
    /* ベースの文字サイズ拡大 */
    html, body, [class*="css"] {
        font-family: "Hiragino Sans", "Meiryo", sans-serif;
        font-size: 18px !important;
        line-height: 1.8 !important;
        color: #333333;
    }
    /* ボタンを指で押しやすく巨大化 (44px以上確保) */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        font-weight: bold;
        background-color: #E8F5E9;
        border: 2px solid #2E7D32;
        color: #2E7D32;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .stButton > button:hover {
        background-color: #2E7D32;
        color: white;
    }
    /* 見出しのデザイン */
    h1, h2, h3 {
        color: #2E7D32 !important;
    }
    /* 進行バーの色 */
    .stProgress > div > div > div > div {
        background-color: #2E7D32;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 福祉職のための履歴書作成")
st.markdown("**質問に答えるだけで、プロ品質の「志望動機」と「職務経歴書」が完成します。**")

# セッション管理（ステップ進行）
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {}

# 進捗バー (要件定義 6.2: 認知的負荷軽減)
progress = (st.session_state.step / 4) * 100
st.progress(int(progress))
st.caption(f"ステップ {st.session_state.step} / 4")

# ==========================================
# STEP 1: きっかけ・背景 (Component A)
# ==========================================
if st.session_state.step == 1:
    st.header("1. 介護・福祉を目指したきっかけ")
    st.write("あなたの状況に最も近いものを選んでください")

    # 要件定義 5.1: コンポーネントAの選択肢
    trigger_options = {
        "未経験・異業種": [
            "A-1. 家族の介護を経験し、専門技術を身につけて役に立ちたいと思った",
            "A-2. ボランティアで利用者様の笑顔と「ありがとう」にやりがいを感じた",
            "A-3. 接客業の経験を活かし、一人ひとりと深く関わる仕事がしたい",
            "A-4. 高齢化社会を支える仕事で、手に職をつけて安定して働きたい",
            "A-5. AIにはできない、人と人との触れ合いこそが価値を生む仕事がしたい"
        ],
        "経験者・キャリアアップ": [
            "A-6. 訪問介護の経験から、在宅生活を支える重要性を学んだ",
            "A-7. 認知症ケア等のより専門的なスキルを貴施設で磨きたい",
            "A-8. リーダー経験を活かし、マネジメントや人材育成に携わりたい",
            "A-9. 「自立支援」という貴法人の理念に深く共感した"
        ],
        "ブランク・復職": [
            "A-10. 子育てが一段落し、大好きな介護の仕事に復帰したい",
            "A-11. 親の介護経験を経て、以前より利用者に寄り添えると考えた",
            "A-12. ブランクはあるが、最新の知識を学び直し戦力になりたい"
        ]
    }

    # カテゴリ選択でフィルタリング
    trigger_cat = st.radio("現在の状況は？", list(trigger_options.keys()))
    selected_trigger = st.selectbox("具体的な理由は？", trigger_options[trigger_cat])

    # 資格入力（要件定義 4.1: 正式名称マッピング用）
    st.markdown("---")
    st.subheader("保有資格")
    qualifications = st.multiselect("お持ちの資格を選んでください（略称でOK）", [
        "なし", "ヘルパー2級", "初任者研修", "ヘルパー1級", "実務者研修",
        "介護福祉士", "社会福祉士", "精神保健福祉士", "ケアマネ",
        "普通免許(AT)", "認知症ケア専門士", "喀痰吸引研修"
    ])

    if st.button("次へ進む（強みを選ぶ）"):
        st.session_state.data["trigger"] = selected_trigger
        st.session_state.data["qualifications"] = qualifications
        st.session_state.step = 2
        st.rerun()

# ==========================================
# STEP 2: 性格・ソフトスキル (Component B-1)
# ==========================================
elif st.session_state.step == 2:
    st.header("2. あなたの性格・強み")
    st.write("アピールしたい長所を選んでください")

    # 要件定義 5.2: コンポーネントB-1
    strength_options = {
        "傾聴力": "B-1. 言葉にならない思いや表情の変化を汲み取る「傾聴力」",
        "協調性": "B-2. チームケアを重視し、報告・連絡・相談を徹底する「協調性」",
        "忍耐力": "B-3. 認知症の方などにも粘り強く受容的に関わる「忍耐力」",
        "明るさ": "B-4. 挨拶や声掛けで職場を明るくする「ムードメーカー」",
        "責任感": "B-5. 事故防止や体調変化に気づき、任された業務を全うする「責任感」",
        "向上心": "B-6. 新しい技術や知識を積極的に学ぶ「向上心」"
    }
    
    selected_strength_key = st.radio("一番自信があるのは？", list(strength_options.keys()))
    
    # 貢献・目標 (Component C) もここで聞く
    st.markdown("---")
    st.subheader("入社後の目標")
    goal_options = [
        "C-1. 即戦力として、利用者様の顔と名前を早く覚えたい",
        "C-2. 体力を活かし、夜勤や変則勤務にも柔軟に対応したい",
        "C-3. 資格取得を目指し、将来的にはリーダーとして貢献したい",
        "C-4. 利用者様にとって「会うと元気になる」存在になりたい",
        "C-5. 業務改善や効率化にも取り組み、働きやすい環境を作りたい"
    ]
    selected_goal = st.selectbox("目指す姿は？", goal_options)

    if st.button("次へ進む（業務経験チェック）"):
        st.session_state.data["strength_desc"] = strength_options[selected_strength_key]
        st.session_state.data["goal"] = selected_goal
        st.session_state.step = 3
        st.rerun()

# ==========================================
# STEP 3: 具体的業務タスク (Component B-2)
# ==========================================
elif st.session_state.step == 3:
    st.header("3. 経験した業務")
    st.write("これまで経験したことがある業務にチェックを入れてください。")
    st.caption("※未経験の方はチェック不要です")

    # 要件定義 5.4: 職務経歴書用タスクリスト
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 身体介護")
        t_meal = st.checkbox("食事介助（全介助・見守り）")
        t_bath = st.checkbox("入浴介助（一般・機械浴）")
        t_excretion = st.checkbox("排泄介助（オムツ・トイレ）")
        t_transfer = st.checkbox("移乗・移動介助")
        t_night = st.checkbox("夜勤業務・巡視")
    
    with col2:
        st.markdown("#### 生活・その他")
        t_dementia = st.checkbox("認知症ケア・BPSD対応")
        t_rec = st.checkbox("レクリエーション企画運営")
        t_record = st.checkbox("記録作成（PC・タブレット）")
        t_drive = st.checkbox("送迎業務・運転")
        t_terminal = st.checkbox("看取りケア・ターミナル")

    if st.button("履歴書を生成する！"):
        st.session_state.data["tasks"] = {
            "食事介助": t_meal, "入浴介助": t_bath, "排泄介助": t_excretion,
            "移乗介助": t_transfer, "夜勤業務": t_night, "認知症ケア": t_dementia,
            "レク運営": t_rec, "記録業務": t_record, "送迎": t_drive, "看取り": t_terminal
        }
        st.session_state.step = 4
        st.rerun()

# ==========================================
# STEP 4: 生成結果・出力
# ==========================================
elif st.session_state.step == 4:
    st.header("🎉 完成しました！")
    d = st.session_state.data
    
    # --- 1. 志望動機生成ロジック ---
    motivation_text = "【志望動機】\n"
    
    # きっかけ (A) の文章化
    trigger_text = d["trigger"].split(". ")[1] # 番号除去
    if "家族の介護" in trigger_text:
        motivation_text += "家族の介護を経験し、専門的な知識と技術を身につけて社会の役に立ちたいと強く思い、志望いたしました。"
    elif "ボランティア" in trigger_text:
        motivation_text += "以前ボランティア活動に参加した際、利用者様の笑顔に深いやりがいを感じ、これを生涯の仕事にしたいと考えました。"
    elif "接客業" in trigger_text:
        motivation_text += "これまで接客業で培ったコミュニケーション能力を活かし、より一人ひとりのお客様と深く関わる仕事がしたいと考え、介護職を志望しました。"
    elif "手に職" in trigger_text:
        motivation_text += "高齢化社会を支える不可欠な存在である介護業界で、専門性を磨きながら長く安定して働きたいと考えました。"
    elif "ブランク" in trigger_text:
        motivation_text += "一度現場を離れましたが、やはり利用者様と触れ合う介護の仕事のやりがいが忘れられず、復職を決意いたしました。"
    else:
        motivation_text += f"{trigger_text}と考え、志望いたしました。" # 汎用

    # 強み (B) の接続
    strength_key = d["strength_desc"].split(". ")[1].split("「")[1].split("」")[0]
    motivation_text += f"\n\n私の強みは「{strength_key}」です。"
    
    if "傾聴" in strength_key:
        motivation_text += "利用者様の言葉にならない思いや、些細な表情の変化を汲み取ることを常に心がけています。"
    elif "協調" in strength_key:
        motivation_text += "チームケアを重視し、他職種との連携をスムーズに行うための報告・連絡・相談を徹底します。"
    elif "忍耐" in strength_key:
        motivation_text += "認知症の方の繰り返しの訴えにも、否定せず受容と共感を持って粘り強く対応することができます。"
    elif "ムードメーカー" in strength_key:
        motivation_text += "職場のムードメーカーとして、挨拶や声掛けを大切にし、利用者様や職員が明るくなれる雰囲気作りを行います。"
    elif "責任感" in strength_key:
        motivation_text += "任された業務を最後までやり遂げることはもちろん、プラスアルファの気配りで利用者様の満足度を高めます。"
    elif "向上心" in strength_key:
        motivation_text += "研修や勉強会には積極的に参加し、新しい介護技術や知識を現場に取り入れる努力を惜しみません。"

    # 目標 (C) の接続
    goal_text = d["goal"].split(". ")[1]
    motivation_text += f"\n\n入社後は、{goal_text}と考えております。貴施設の理念実現に貢献できるよう尽力いたします。"

    # --- 2. 職務要約生成ロジック ---
    summary_text = "【職務要約・経験業務】\n"
    active_tasks = [k for k, v in d["tasks"].items() if v]
    
    if not active_tasks:
        summary_text += "未経験ではありますが、研修を通じて基本的な介護技術を積極的に習得し、早期に戦力となれるよう努力いたします。"
    else:
        summary_text += "これまでの経験において、以下の業務に従事してまいりました。\n"
        if "食事介助" in active_tasks: summary_text += "・身体介護：食事・入浴・排泄の三大介助（自立支援を意識したケアの実践）\n"
        if "夜勤業務" in active_tasks: summary_text += "・夜勤業務：巡視、安否確認、緊急時対応\n"
        if "認知症ケア" in active_tasks: summary_text += "・認知症対応：BPSDへの対応、受容的コミュニケーション\n"
        if "レク運営" in active_tasks: summary_text += "・生活支援：レクリエーションの企画・運営、記録作成\n"
        if "看取り" in active_tasks: summary_text += "・その他：ターミナルケア（看取り）、ご家族への精神的ケア\n"

    # --- 3. 資格の正式名称変換 (要件定義 4.1) ---
    qual_text = ""
    if d["qualifications"] and "なし" not in d["qualifications"]:
        qual_list = []
        mapping = {
            "ヘルパー2級": "介護職員初任者研修 修了（旧ヘルパー2級）",
            "初任者研修": "介護職員初任者研修 修了",
            "ヘルパー1級": "介護職員実務者研修 修了（旧ヘルパー1級）",
            "実務者研修": "介護職員実務者研修 修了",
            "介護福祉士": "介護福祉士 登録",
            "社会福祉士": "社会福祉士 登録",
            "精神保健福祉士": "精神保健福祉士 登録",
            "ケアマネ": "介護支援専門員（ケアマネジャー）",
            "普通免許(AT)": "普通自動車第一種運転免許（AT限定）",
            "認知症ケア専門士": "認知症ケア専門士 認定",
            "喀痰吸引研修": "喀痰吸引等研修 修了"
        }
        for q in d["qualifications"]:
            qual_list.append(mapping.get(q, q))
        qual_text = "\n".join(qual_list)

    # --- 出力エリア ---
    st.success("以下のテキストをコピーして、履歴書に貼り付けてください")
    
    st.subheader("志望動機")
    st.text_area("志望動機_copy", motivation_text, height=300)
    
    st.subheader("職務の要約")
    st.text_area("職務要約_copy", summary_text, height=200)

    if qual_text:
        st.subheader("資格（正式名称）")
        st.text_area("資格_copy", qual_text, height=150)

    # --- マネタイズ導線 (人材紹介アフィリエイト) ---
    st.markdown("---")
    st.markdown("### 📢 あなたの経験を高く評価する求人があります")
    
    # ユーザーの属性に合わせてオファーを変える（要件定義 5.2.3: 動的ターゲティング）
    affiliate_msg = "好条件の非公開求人を見てみる"
    if "介護福祉士" in d["qualifications"]:
        affiliate_msg = "【介護福祉士優遇】月給30万円以上の求人を見る"
    elif "夜勤業務" in active_tasks:
        affiliate_msg = "【夜勤専従あり】1回2.5万円〜の高単価夜勤求人を見る"
    elif "未経験" in str(d["trigger"]):
        affiliate_msg = "【未経験OK】研修充実・資格取得支援ありの求人を見る"

    st.markdown(f"""
        <a href="#" style="
            display: block;
            width: 100%;
            padding: 20px;
            background-color: #FF9800;
            color: white;
            text-align: center;
            text-decoration: none;
            font-weight: bold;
            border-radius: 10px;
            font-size: 22px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;
        ">
            👉 {affiliate_msg}
        </a>
    """, unsafe_allow_html=True)
    st.caption("※登録は無料です。あなたの市場価値を確かめてみましょう。")

    if st.button("最初からやり直す"):
        st.session_state.step = 1
        st.rerun()
