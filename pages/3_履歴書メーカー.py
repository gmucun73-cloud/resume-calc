import streamlit as st
from datetime import date
import time

# ==========================================
# 0. デザイン設定：シニア・アクセシビリティ対応
# ==========================================
st.set_page_config(page_title="福祉職の履歴書メーカー", layout="centered")

# CSS注入：文字サイズ18px以上、ボタン巨大化、配色調整
st.markdown("""
    <style>
    /* ベース文字サイズ拡大 (老眼対策) */
    html, body, [class*="css"] {
        font-family: "Hiragino Sans", "Meiryo", sans-serif;
        font-size: 18px !important;
        line-height: 1.8 !important;
        color: #333333;
    }
    /* ボタンを指で押しやすく巨大化 (高さ60px) */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        font-weight: bold;
        background-color: #F1F8E9; /* 薄い緑 */
        border: 2px solid #558B2F;
        color: #558B2F;
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .stButton > button:hover {
        background-color: #558B2F;
        color: white;
    }
    /* 入力フォームを見やすく */
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 15px;
    }
    /* 見出しの色 */
    h1, h2, h3 {
        color: #2E7D32 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("履歴書・職務経歴書メーカー")
st.markdown("**質問に答えるだけで、あなたの経験を「採用される文章」に変換します。**")

# セッション管理（ステップ進行）
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {}

# 進捗バー
progress = (st.session_state.step / 4) * 100
st.progress(int(progress))
st.caption(f"ステップ {st.session_state.step} / 4")

# ==========================================
# STEP 1: 動機と背景 (Trigger)
# ==========================================
if st.session_state.step == 1:
    st.header("1. 今回、なぜ作ろうと思いましたか？")
    st.write("あなたの気持ちに一番近いものを選んでください")

    trigger_options = {
        "未経験・異業種から": [
            "A-1. 家族の介護を経験し、役に立ちたいと思った",
            "A-2. ボランティアで「ありがとう」と言われ感動した",
            "A-3. 接客経験を活かし、人と深く関わる仕事がしたい",
            "A-4. 手に職をつけて、長く安定して働きたい",
            "A-5. AIにはできない、人の温かみがある仕事がしたい"
        ],
        "経験者・キャリアアップ": [
            "A-6. 訪問介護の経験から、在宅支援を深めたい",
            "A-7. 認知症ケアなど、より専門的なスキルを磨きたい",
            "A-8. リーダー経験を活かし、人材育成に携わりたい",
            "A-9. 「自立支援」という理念に共感した"
        ],
        "今の職場を離れたい・復職": [
            "A-10. 流れ作業ではなく、一人ひとりに寄り添いたい",
            "A-11. 人間関係が良好な環境で、ケアに集中したい",
            "A-12. ブランクがあるが、やっぱり介護の仕事が好き",
            "A-13. 子育てが一段落したので復帰したい"
        ]
    }

    # カテゴリ選択
    trigger_cat = st.radio("現在の状況", list(trigger_options.keys()))
    selected_trigger = st.selectbox("具体的な理由", trigger_options[trigger_cat])

    # 資格入力（正式名称変換用）
    st.markdown("---")
    st.subheader("お持ちの資格（略称でOK）")
    qualifications = st.multiselect("複数選択可", [
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
# STEP 2: 強み・ソフトスキル (Strength)
# ==========================================
elif st.session_state.step == 2:
    st.header("2. あなたの長所")
    st.write("アピールしたいポイントを選んでください")

    strength_options = {
        "傾聴力": "B-1. 言葉にならない思いを汲み取る「傾聴力」",
        "協調性": "B-2. チームワークと報告連絡相談を大切にする「協調性」",
        "忍耐力": "B-3. 認知症の方にも穏やかに対応できる「受容と共感」",
        "明るさ": "B-4. 挨拶と声掛けで職場を明るくする「ムードメーカー」",
        "責任感": "B-5. 小さな変化に気づき事故を防ぐ「観察力と責任感」",
        "向上心": "B-6. 新しい技術や知識を積極的に学ぶ「向上心」"
    }
    
    selected_strength_key = st.radio("一番自信があるのは？", list(strength_options.keys()))
    
    # 将来の目標
    st.markdown("---")
    st.subheader("入社後の目標")
    goal_options = [
        "C-1. 即戦力として、利用者様の顔と名前を早く覚えたい",
        "C-2. 夜勤や変則勤務にも柔軟に対応し、シフトに貢献したい",
        "C-3. 資格取得を目指し、将来的にはリーダーとして貢献したい",
        "C-4. 利用者様にとって「会うと元気になる」存在になりたい",
        "C-5. 業務効率化に取り組み、働きやすい環境を作りたい"
    ]
    selected_goal = st.selectbox("目指す姿", goal_options)

    if st.button("次へ進む（業務経験）"):
        st.session_state.data["strength_desc"] = strength_options[selected_strength_key]
        st.session_state.data["goal"] = selected_goal
        st.session_state.step = 3
        st.rerun()

# ==========================================
# STEP 3: 具体的タスク (Task)
# ==========================================
elif st.session_state.step == 3:
    st.header("3. 経験業務チェック")
    st.write("やったことがある業務にチェックを入れてください。")
    st.caption("※これをもとに「職務経歴書」を自動で作ります")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 身体介護")
        t_meal = st.checkbox("食事介助")
        t_bath = st.checkbox("入浴介助")
        t_excretion = st.checkbox("排泄介助")
        t_transfer = st.checkbox("移乗・移動")
        t_night = st.checkbox("夜勤・巡視")
    
    with col2:
        st.markdown("#### 生活・その他")
        t_dementia = st.checkbox("認知症ケア")
        t_rec = st.checkbox("レクリエーション")
        t_record = st.checkbox("記録・PC入力")
        t_drive = st.checkbox("送迎・運転")
        t_terminal = st.checkbox("看取りケア")

    if st.button("履歴書を生成する！"):
        st.session_state.data["tasks"] = {
            "食事介助": t_meal, "入浴介助": t_bath, "排泄介助": t_excretion,
            "移乗介助": t_transfer, "夜勤業務": t_night, "認知症ケア": t_dementia,
            "レク運営": t_rec, "記録業務": t_record, "送迎": t_drive, "看取り": t_terminal
        }
        st.session_state.step = 4
        st.rerun()

# ==========================================
# STEP 4: 完成・出力・収益化導線
# ==========================================
elif st.session_state.step == 4:
    st.header("🎉 完成しました！")
    d = st.session_state.data
    
    # --- 文章生成ロジック ---
    motivation_text = "【志望動機】\n"
    
    # きっかけ変換
    trigger_text = d["trigger"].split(". ")[1]
    if "家族の介護" in trigger_text:
        motivation_text += "家族の介護を経験し、専門技術を身につけて社会の役に立ちたいと強く思い、志望いたしました。"
    elif "ボランティア" in trigger_text:
        motivation_text += "ボランティア活動で利用者様の笑顔に深いやりがいを感じ、これを生涯の仕事にしたいと考えました。"
    elif "人間関係" in trigger_text:
        motivation_text += "チームワークを重視する貴法人の理念に惹かれ、職員同士が連携できる環境で利用者様に集中したいと考え志望しました。"
    else:
        motivation_text += f"{trigger_text}と考え、志望いたしました。"

    # 強み変換
    strength_key = d["strength_desc"].split(". ")[1].split("「")[1].split("」")[0]
    motivation_text += f"\n\n私の強みは「{strength_key}」です。"
    if "傾聴" in strength_key:
        motivation_text += "言葉にならない思いや表情の変化を汲み取ることを常に心がけています。"
    elif "協調" in strength_key:
        motivation_text += "報告・連絡・相談を徹底し、多職種とスムーズに連携します。"
    
    # 目標変換
    goal_text = d["goal"].split(". ")[1]
    motivation_text += f"\n\n入社後は{goal_text}と考えております。"

    # 職務要約生成
    summary_text = "【職務要約・得意分野】\n"
    active_tasks = [k for k, v in d["tasks"].items() if v]
    
    if not active_tasks:
        summary_text += "未経験ですが、研修を通じて技術を積極的に習得し、早期に戦力となります。"
    else:
        summary_text += "これまでの経験において、以下の業務に従事してまいりました。\n"
        if "食事介助" in active_tasks: summary_text += "・身体介護：三大介助（食事・入浴・排泄）における自立支援\n"
        if "夜勤業務" in active_tasks: summary_text += "・夜勤業務：夜間の巡視、安否確認、緊急時対応\n"
        if "認知症ケア" in active_tasks: summary_text += "・認知症対応：BPSDへの受容的対応、ユマニチュードの実践\n"
        if "レク運営" in active_tasks: summary_text += "・生活支援：レクリエーション企画運営、QOL向上支援\n"
        if "看取り" in active_tasks: summary_text += "・その他：ターミナルケア（看取り）、家族支援\n"

    # 資格変換
    qual_text = ""
    if d["qualifications"] and "なし" not in d["qualifications"]:
        mapping = {
            "ヘルパー2級": "介護職員初任者研修 修了（旧ヘルパー2級）",
            "初任者研修": "介護職員初任者研修 修了",
            "実務者研修": "介護職員実務者研修 修了",
            "ケアマネ": "介護支援専門員（ケアマネジャー）",
            "普通免許(AT)": "普通自動車第一種運転免許（AT限定）"
        }
        qual_list = [mapping.get(q, q) for q in d["qualifications"]]
        qual_text = "\n".join(qual_list)

    # --- 表示エリア ---
    st.success("以下の文章をコピーして使ってください")
    st.text_area("志望動機", motivation_text, height=250)
    st.text_area("職務要約", summary_text, height=150)
    if qual_text:
        st.text_area("資格（正式名称）", qual_text, height=100)

    # --- 【ここが収益化のキモ！】戦略的出口 ---
    st.markdown("---")
    st.header("⚠️ この履歴書をどこに出しますか？")
    st.write("あなたの市場価値は高いです。安売りしてはいけません。")

    col1, col2 = st.columns(2)
    
    # 1. キャリアアップ（攻め）
    with col1:
        st.info("💰 給料を上げたいなら")
        st.write("ハローワークにはない「非公開求人」があります。")
        # ※ここに後でアフィリエイトリンクを入れる（例：きらケア）
        st.markdown("""
            <a href="#" style="display:block; text-align:center; background:#FF9800; color:white; padding:15px; border-radius:10px; text-decoration:none; font-weight:bold;">
            👉 高待遇求人を見る
            </a>
        """, unsafe_allow_html=True)

    # 2. 退職代行・お守り（守り）
    with col2:
        st.error("🛡 辞めさせてくれないなら")
        st.write("「人手が足りない」はあなたの責任ではありません。")
        # ※ここに後でアフィリエイトリンクを入れる（例：退職代行ガーディアン）
        st.markdown("""
            <a href="#" style="display:block; text-align:center; background:#D32F2F; color:white; padding:15px; border-radius:10px; text-decoration:none; font-weight:bold;">
            👉 退職代行に相談する
            </a>
        """, unsafe_allow_html=True)
    
    st.caption("※リンク先は現在はダミーです。アフィリエイト登録後に書き換えます。")

    if st.button("最初からやり直す"):
        st.session_state.step = 1
        st.rerun()
