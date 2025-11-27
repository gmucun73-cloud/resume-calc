import streamlit as st

# ページ設定
st.set_page_config(page_title="支援記録生成くん Ver.2", layout="centered")

st.title("📝 支援記録 一発生成くん Ver.2")
st.caption("就労支援の現場で使える、自然な文章を生成します。")

# --- データの定義（辞書型で正しい日本語を登録） ---
# ここを書き換えれば、自分好みの文章セットが作れます

# 1. 通所・体調の選択肢
conditions_data = {
    "安定": {
        "label": "問題なく通所・安定",
        "da": "本日は定刻通りに通所し、一日を通して安定した様子で過ごせている。",
        "desu": "本日は定刻通りに通所され、一日を通して安定した様子でした。"
    },
    "疲れ": {
        "label": "疲れあり・参加可",
        "da": "来所時にやや疲れた表情が見受けられたが、プログラムには問題なく参加できている。",
        "desu": "来所時にやや疲れた表情が見受けられましたが、プログラムには問題なく参加できました。"
    },
    "不調": {
        "label": "体調不良・休憩",
        "da": "通所時より体調不良の訴えがあり、適宜休憩を挟みながらの参加となった。",
        "desu": "通所時より体調不良の訴えがあり、適宜休憩を挟みながらの参加となりました。"
    },
    "遅刻": {
        "label": "遅刻・切り替え",
        "da": "開始時刻に遅れての通所となったが、到着後はスムーズに作業へ移行できている。",
        "desu": "開始時刻に遅れての通所となりましたが、到着後はスムーズに作業へ移行できました。"
    }
}

# 2. 作業・活動の選択肢
work_data = {
    "集中": {
        "label": "高い集中力",
        "da": "作業場面では高い集中力を維持し、正確に業務を遂行することができていた。",
        "desu": "作業場面では高い集中力を維持し、正確に業務を遂行することができていました。"
    },
    "散漫": {
        "label": "集中切れ・休憩必要",
        "da": "時間が経過するとともに集中力が散漫になりがちであったため、こまめな休憩を促した。",
        "desu": "時間が経過するとともに集中力が散漫になりがちでしたので、こまめな休憩を促しました。"
    },
    "支援": {
        "label": "手が止まる・声かけ",
        "da": "判断に迷い手が止まる場面も見られたが、職員の助言により再開できている。",
        "desu": "判断に迷い手が止まる場面も見られましたが、職員の助言により再開できました。"
    },
    "意欲": {
        "label": "意欲的・手順確認",
        "da": "新しい課題に対して意欲的に取り組み、手順書を確認しながら丁寧に進める様子が見られた。",
        "desu": "新しい課題に対して意欲的に取り組み、手順書を確認しながら丁寧に進める様子が見られました。"
    }
}

# 3. コミュニケーションの選択肢
comm_data = {
    "良好": {
        "label": "良好・適度な距離",
        "da": "対人面においては周囲と適切な距離感を保ち、穏やかに過ごせている。",
        "desu": "対人面においては周囲と適切な距離感を保ち、穏やかに過ごせていました。"
    },
    "談笑": {
        "label": "他者交流・談笑",
        "da": "休憩時間には他の利用者と笑顔で談笑するなど、リラックスして交流する姿が見られた。",
        "desu": "休憩時間には他の利用者と笑顔で談笑するなど、リラックスして交流する姿が見られました。"
    },
    "孤立": {
        "label": "一人を好む・静か",
        "da": "本日は他者との交流よりも一人で過ごすことを好み、静かな環境で自身のペースを保っていた。",
        "desu": "本日は他者との交流よりも一人で過ごすことを好み、静かな環境で自身のペースを保っていました。"
    },
    "報告": {
        "label": "報連相しっかり",
        "da": "作業の進捗報告や不明点の相談など、職員への報告・連絡・相談が適切に行えていた。",
        "desu": "作業の進捗報告や不明点の相談など、職員への報告・連絡・相談が適切に行えていました。"
    }
}

# --- 入力エリア ---
st.markdown("### 1. 本日の様子を選択してください")

col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("利用者名", placeholder="Aさん")
    
with col2:
    style_mode = st.radio("文体モード", ["ケース記録（だ・である）", "日報・連絡帳（です・ます）"])
    # キー変換
    mode_key = "da" if "だ・である" in style_mode else "desu"

st.markdown("---")

# 選択ボックスの作成（辞書のキーを使う）
c_key = st.selectbox("① 通所・体調", list(conditions_data.keys()), format_func=lambda x: conditions_data[x]["label"])
w_key = st.selectbox("② 作業・活動", list(work_data.keys()), format_func=lambda x: work_data[x]["label"])
m_key = st.selectbox("③ 対人・交流", list(comm_data.keys()), format_func=lambda x: comm_data[x]["label"])

free_comment = st.text_area("④ 特記事項（追記があれば）", height=80)

# --- 生成ロジック ---
def generate_full_text(name, mode, c_k, w_k, m_k, free):
    # 各パーツを取得
    part_c = conditions_data[c_k][mode]
    part_w = work_data[w_k][mode]
    part_m = comm_data[m_k][mode]
    
    # 結合（改行を入れることでリズムを作る）
    full_text = f"【{name} 今日の記録】\n"
    full_text += f"{part_c}\n"
    full_text += f"{part_w}\n"
    full_text += f"{part_m}"
    
    if free:
        # 特記事項へのつなぎ言葉
        connector = "\nなお、"
        full_text += connector + free
        if not (free.endswith("。") or free.endswith(".")):
            full_text += "。"
            
    return full_text

# --- 出力エリア ---
st.divider()

if st.button("記録を生成する", type="primary"):
    if not user_name:
        user_name = "利用者"
    
    result = generate_full_text(user_name, mode_key, c_key, w_key, m_key, free_comment)
    
    st.success("生成完了！")
    st.text_area("コピー用テキスト", result, height=250)
    
    st.info("💡 修正ヒント：生成された文章をベースに、具体的な「作業名」や「時間」を書き足すと、より質の高い記録になります。")

    # アフィリエイトリンク（例）
    st.markdown("---")
    st.markdown("[👉 サービス管理責任者のための求人特集を見る](#)")
