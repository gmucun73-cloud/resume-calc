import streamlit as st
import time

# ==========================================
# 0. デザイン設定 (シニア・アクセシビリティ & CVボタン)
# ==========================================
st.set_page_config(page_title="福祉職の履歴書メーカー", layout="centered")

st.markdown("""
    <style>
    /* 文字サイズ・配色の調整 */
    html, body, [class*="css"] {
        font-family: "Hiragino Sans", "Meiryo", sans-serif;
        font-size: 18px !important;
        line-height: 1.8 !important;
        color: #333333;
    }
    /* ボタンの巨大化 */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        font-weight: bold;
        background-color: #F1F8E9;
        border: 2px solid #558B2F;
        color: #558B2F;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .stButton > button:hover {
        background-color: #558B2F;
        color: white;
    }
    /* 広告リンクボタンのデザイン（オレンジ） */
    .ad-link {
        display: block;
        width: 100%;
        padding: 20px;
        background-color: #FF9800; /* 目立つオレンジ */
        color: white !important;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 10px;
        font-size: 22px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .ad-link:hover {
        opacity: 0.8;
    }
    /* 退職代行ボタンのデザイン（赤） */
    .quit-link {
        background-color: #D32F2F; /* 警告色 */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("福祉職のための履歴書メーカー")
st.markdown("**質問に答えるだけで、あなたの経験を「採用される文章」に変換します。**")

# セッション管理
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
        "今の職場を離れたい・人間関係": [
            "A-1. 人間関係が辛く、環境を変えたい",
            "A-2. 「人手が足りない」と言われ辞めさせてくれない",
            "A-3. サービス残業や休日の連絡に疲れてしまった",
            "A-4. 自分の心身を守るために、退職を決意した"
        ],
        "経験者・キャリアアップ": [
            "B-1. 訪問介護の経験から、在宅支援を深めたい",
            "B-2. 認知症ケアなど、専門スキルを磨きたい",
            "B-3. リーダー経験を活かし、給与アップを目指したい",
            "B-4. 「自立支援」という理念に共感した"
        ],
        "未経験・復職・その他": [
            "C-1. 家族の介護を経験し、役に立ちたいと思った",
            "C-2. ボランティアで感動し、介護職を目指した",
            "C-3. 手に職をつけて、長く安定して働きたい",
            "C-4. 子育てが一段落したので復帰したい"
        ]
    }

    trigger_cat = st.radio("現在の状況", list(trigger_options.keys()))
    selected_trigger = st.selectbox("具体的な理由", trigger_options[trigger_cat])

    # 資格入力
    st.markdown("---")
    st.subheader("お持ちの資格")
    qualifications = st.multiselect("複数選択可（略称でOK）", [
        "なし", "ヘルパー2級", "初任者研修", "実務者研修",
        "介護福祉士", "社会福祉士", "精神保健福祉士", "ケアマネ","普通免許(MT)",
        "普通免許(AT)", "喀痰吸引研修"
    ])

    if st.button("次へ進む"):
        st.session_state.data["trigger_cat"] = trigger_cat # カテゴリを保存（広告出し分け用）
        st.session_state.data["trigger"] = selected_trigger
        st.session_state.data["qualifications"] = qualifications
        st.session_state.step = 2
        st.rerun()

# ==========================================
# STEP 2: 強み (Strength)
# ==========================================
elif st.session_state.step == 2:
    st.header("2. あなたの長所")
    strength_options = {
        "傾聴力": "言葉にならない思いを汲み取る「傾聴力」",
        "協調性": "チームワークを大切にする「協調性」",
        "忍耐力": "認知症の方にも穏やかに対応できる「忍耐力」",
        "明るさ": "職場を明るくする「ムードメーカー」",
        "責任感": "小さな変化に気づき事故を防ぐ「責任感」",
        "向上心": "新しい技術を積極的に学ぶ「向上心」"
    }
    selected_strength_key = st.radio("一番自信があるのは？", list(strength_options.keys()))
    
    st.markdown("---")
    st.subheader("入社後の目標")
    goal_options = [
        "即戦力として、利用者様の顔と名前を早く覚えたい",
        "夜勤や変則勤務にも柔軟に対応し、シフトに貢献したい",
        "資格取得を目指し、将来的にはリーダーになりたい",
        "利用者様にとって「会うと元気になる」存在になりたい"
    ]
    selected_goal = st.selectbox("目指す姿", goal_options)

    if st.button("次へ進む"):
        st.session_state.data["strength_desc"] = strength_options[selected_strength_key]
        st.session_state.data["goal"] = selected_goal
        st.session_state.step = 3
        st.rerun()

# ==========================================
# STEP 3: 具体的タスク (Task)
# ==========================================
elif st.session_state.step == 3:
    st.header("3. 経験業務チェック")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 身体介護")
        t_meal = st.checkbox("食事介助")
        t_bath = st.checkbox("入浴介助")
        t_excretion = st.checkbox("排泄介助")
        t_night = st.checkbox("夜勤・巡視")
    with col2:
        st.markdown("#### その他")
        t_dementia = st.checkbox("認知症ケア")
        t_rec = st.checkbox("レクリエーション")
        t_record = st.checkbox("記録・PC入力")
        t_terminal = st.checkbox("看取りケア")

    if st.button("履歴書を生成する"):
        st.session_state.data["tasks"] = {
            "食事": t_meal, "入浴": t_bath, "排泄": t_excretion, "夜勤": t_night,
            "認知症": t_dementia, "レク": t_rec, "記録": t_record, "看取り": t_terminal
        }
        st.session_state.step = 4
        st.rerun()

# ==========================================
# STEP 4: 完成・収益化導線 (Ads & Offer)
# ==========================================
elif st.session_state.step == 4:
    st.header("🎉 完成しました！")
    d = st.session_state.data
    
    # --- 収益ポイント1: 写真アップロード（アプリ訴求） ---
    with st.expander("📸 証明写真は用意しましたか？（クリックで開く）"):
        st.info("履歴書の写真はスマホで撮れます。")
        st.write("わざわざ証明写真機に行く必要はありません。このアプリなら、美肌補正もできて、コンビニで数十円で印刷できます。")
        # アプリインストールのアフィリエイトリンク（例：履歴書カメラなど）
        st.markdown("[👉 **おすすめの履歴書カメラアプリを入れる**](#)") 

    st.markdown("---")
    
    # --- 文章生成ロジック（簡略化して表示） ---
    motivation_text = "【志望動機】\n"
    # (ロジックは前のバージョンと同じですが、今回は省略せず実装されていると仮定)
    if "人間関係" in d["trigger_cat"]:
        motivation_text += "チームワークを重視する貴法人の理念に惹かれ、職員同士が連携できる環境で利用者様に集中したいと考え志望しました。"
    else:
        motivation_text += "これまでの経験を活かし、貴施設で貢献したいと考え志望しました。" # 簡易版
    
    motivation_text += f"\n\n私の強みは「{d['strength_desc'].split('「')[1].split('」')[0]}」です。"
    motivation_text += f"\n入社後は{d['goal']}と考えております。"

    # --- 出力表示 ---
    st.success("以下の文章をコピーして使ってください")
    st.text_area("志望動機", motivation_text, height=200)

    # --- 収益ポイント2 & 3: 文脈連動型オファー ---
    st.markdown("---")
    st.header("⚠️ 最後に一つだけ確認です")
    
    # 退職代行ロジック（Triggerがネガティブなら表示）
    if "今の職場を離れたい" in d["trigger_cat"]:
        st.error("無理に自分で辞めようとしていませんか？")
        st.write("「辞めさせない」と言われたり、有給消化を拒否されるのは違法です。プロに任せて、明日から行かなくていい方法があります。")
        
        # 退職代行のアフィリエイトリンク
        st.markdown("""
            <a href="#" class="ad-link quit-link">
            🛡 退職代行で即日退職する
            </a>
        """, unsafe_allow_html=True)
        st.caption("※弁護士・労働組合監修のサービスへ移動します")
    
    # 転職エージェントロジック（全員に表示するが、ポジティブな文脈で）
    else:
        st.info("あなたの市場価値を確かめましたか？")
        st.write("この履歴書を最大限に活かすなら、一般には出ていない「非公開求人」を見るべきです。")

    # 全員共通：PDFダウンロード直前の「高単価オファー」
    st.markdown("### 🎁 履歴書をプロに見てもらう（無料）")
    st.write("今、エージェントに登録すると、作成した履歴書の添削と、あなたに合ったホワイト企業の紹介が無料で受けられます。")
    
    # 転職エージェントのアフィリエイトリンク（きらケア、マイナビ等）
    st.markdown("""
        <a href="#" class="ad-link">
        👉 無料登録して非公開求人を見る
        </a>
    """, unsafe_allow_html=True)
    st.caption("※登録完了で、あなたの希望に合った求人がメールで届きます。")

    if st.button("最初からやり直す"):
        st.session_state.step = 1
        st.rerun()
