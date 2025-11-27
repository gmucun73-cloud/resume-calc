import streamlit as st
import datetime

# ページ設定
st.set_page_config(page_title="支援記録生成くん", layout="centered")

st.title("📝 支援記録 一発生成くん")
st.caption("キーワードを選ぶだけで、行政実務に使える「それっぽい記録」を自動生成します。")

# --- 入力エリア ---
st.subheader("1. 本日の様子を選択してください")

col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("利用者名（イニシャル等）", placeholder="Aさん")
    time_zone = st.selectbox("時間帯", ["午前", "午後", "一日を通して"])
    
with col2:
    style = st.radio("文体を選択", ["だ・である調（ケース記録）", "です・ます調（日報・連絡帳）"])

st.markdown("---")
st.write("▼ 該当する項目を選んでください")

# 状態の選択肢
condition = st.selectbox("① 通所・体調", [
    "問題なく通所し、安定して過ごせている",
    "来所時に疲れた表情が見られたが、活動には参加できた",
    "体調不良の訴えがあり、休憩を挟みながら過ごした",
    "遅刻して来所したが、その後の切り替えはスムーズだった",
    "通所直後は不安げだったが、時間とともに落ち着きを取り戻した"
])

work_attitude = st.selectbox("② 作業・活動の様子", [
    "高い集中力を維持し、正確に作業を進めていた",
    "周囲の雑音を気にすることなく、自身の課題に取り組めていた",
    "時折手が止まる場面も見られたが、職員の声かけで再開できた",
    "集中力が散漫になりがちで、こまめな休憩が必要だった",
    "他の利用者との私語が多く、作業ペースが低下していた",
    "新しい作業に意欲的に取り組み、手順をよく確認していた"
])

communication = st.selectbox("③ コミュニケーション・対人", [
    "周囲と適切な距離感を保ち、穏やかに過ごせている",
    "職員への報告・連絡・相談が適切に行えていた",
    "他の利用者と楽しそうに談笑する場面が見られた",
    "一人で過ごすことを好み、静かな環境で作業を行った",
    "些細なことで苛立ちを見せる場面があり、クールダウンを促した"
])

free_comment = st.text_area("④ 特記事項（あれば手入力）", placeholder="具体的な出来事や、特筆すべきエピソードがあれば追記してください。")

# --- 生成ロジック ---
def generate_text(name, time, style, cond, work, comm, free):
    # 文末の調整
    if style == "だ・である調（ケース記録）":
        # そのまま利用（デフォルトを「だ・である」想定でリスト作成済みならそのままでOKだが、微調整）
        end_s = "。"
    else:
        # 簡易的な置換（本来は辞書変換がベストですが、今回は簡易実装）
        cond = cond.replace("た", "ました").replace("る", "ます").replace("ない", "ありません")
        work = work.replace("た", "ました").replace("る", "ます")
        comm = comm.replace("た", "ました").replace("る", "ます")
        end_s = "。"

    text = f"【{name} / {time}の記録】\n"
    text += f"{cond}。\n"
    text += f"{work}。\n"
    text += f"{comm}。"
    
    if free:
        text += f"\nなお、{free}"
        if not free.endswith("。"):
            text += "。"
            
    return text

# --- 出力エリア ---
st.divider()
st.subheader("2. 生成結果")

if st.button("記録を作成する"):
    if user_name == "":
        st.warning("利用者名を入力してください")
    else:
        result_text = generate_text(user_name, time_zone, style, condition, work_attitude, communication, free_comment)
        
        st.success("作成完了！以下のテキストをコピーして使ってください。")
        st.text_area("コピー用", result_text, height=200)
        
        # 現場で安心して使うための注意書き
        st.info("🔒 **セキュリティ安心設計**：このフォームに入力された個人情報や内容は、サーバーには一切保存されません。ブラウザを閉じると完全に消去されます。")

        # 広告・回遊エリア
        st.markdown("---")
        st.write("お疲れ様です！記録が終わったら、ご自身のキャリアもチェックしませんか？")
        st.markdown("[👉 **福祉・介護職のための「非公開求人」を見てみる**](#)") # ここも後でアフィリエイトリンクに！
