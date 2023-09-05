import streamlit as st
import datetime
import sqlite3

st.title("飛行日誌アプリ")

# SQLiteデータベースを作成するか、既存のものに接続します
conn = sqlite3.connect("flight_logs.db")

# SQLコマンドを実行するためのカーソルオブジェクトを作成します
cursor = conn.cursor()

# 飛行ログを保存するためのテーブルを定義します
cursor.execute("""
    CREATE TABLE IF NOT EXISTS flight_logs (
        id INTEGER PRIMARY KEY,
        date TEXT,
        flight_schedule TEXT,
        flight_time INTEGER,
        inspection_status TEXT,
        inspection_date TEXT,
        inspection_record TEXT
    )
""")

# 変更をコミットし、データベース接続を閉じます
conn.commit()
conn.close()

# 飛行日誌のデータを保存するためのリスト
flight_logs = []

class FlightLog:
    def __init__(self, date, flight_schedule, flight_time, inspection_status, inspection_date, inspection_record):
        self.date = date
        self.flight_schedule = flight_schedule
        self.flight_time = flight_time
        self.inspection_status = inspection_status
        self.inspection_date = inspection_date
        self.inspection_record = inspection_record

# 新しい飛行日誌の追加
def add_flight_log(date, flight_schedule, flight_time, inspection_status, inspection_date, inspection_record):
    conn = sqlite3.connect("flight_logs.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO flight_logs (date, flight_schedule, flight_time, inspection_status, inspection_date, inspection_record)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, flight_schedule, flight_time, inspection_status, inspection_date, inspection_record))

    conn.commit()
    conn.close()

# サイドバーにカレンダーを表示
selected_date = st.sidebar.date_input("カレンダーを選択", datetime.datetime.now())
st.sidebar.text("")  # 空行を挿入して見た目を調整

# 新しい飛行日誌の入力フォーム
st.header("新しい飛行日誌の追加")
flight_schedule = st.date_input("飛行日程")
flight_time = st.number_input("飛行時間（分）", min_value=0)
inspection_status = st.radio("点検異常", ["あり", "なし"])
inspection_date = st.date_input("点検日")
inspection_record = st.text_area("点検記録")

if st.button("追加"):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    add_flight_log(date, flight_schedule, flight_time, inspection_status, inspection_date, inspection_record)
    st.success("飛行日誌が追加されました。")
    st.experimental_rerun()

# サイドバーに選択された日付に対応する飛行データを表示
selected_date_str = selected_date.strftime('%Y-%m-%d')
st.sidebar.subheader(f"{selected_date_str} の飛行データ")

# SQLiteから飛行データを取得
conn = sqlite3.connect("flight_logs.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM flight_logs WHERE flight_schedule=?", (selected_date_str,))
logs_for_selected_date = cursor.fetchall()
conn.close()

for idx, log in enumerate(logs_for_selected_date, start=1):
    expander_state = st.sidebar.expander(f"--- 飛行データ {idx} ---", expanded=True)
    with expander_state:
        st.sidebar.write("飛行日程:", log[2])
        st.sidebar.write("飛行時間:", log[3], "分")
        st.sidebar.write("点検異常:", log[4])
        st.sidebar.write("点検日:", log[5])
        st.sidebar.write("飛行記録:", log[6])
