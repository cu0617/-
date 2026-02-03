import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="전기 설비 검침 시스템", layout="wide")

# CSS: 배경색 및 인쇄 설정
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    body, [data-testid="stAppViewContainer"] { background-color: #525659 !important; }
    [data-testid="stSidebar"] { background-color: #262730 !important; color: white; }
    @media print { .no-print { display: none !important; } }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "usage_data.csv"

# --- [공통] 데이터 저장 함수 ---
def save_data(date, category, data_dict):
    new_rows = [{"검침일자": date, "구분": category, "항목": k, "수치": v} for k, v in data_dict.items() if v != 0]
    if not new_rows:
        st.warning("⚠️ 입력된 값이 없어 저장하지 않았습니다.")
        return
        
    new_df = pd.DataFrame(new_rows)
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = new_df
    df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
    st.success(f"✅ {date} {category} 데이터 {len(new_rows)}건 저장 완료!")

# --- [메뉴 1] 전기실 계량기 검침 ---
def show_electricity_meter(date_str):
    st.subheader("⚡ 전기실 계량기 검침표")

    # 1. 기존 데이터 리스트 (그대로 유지)
    data = [
        ("39층", "HV39-1", 3000), ("10층(CGV)", "LV-1", 2400), ("10층(극장)", "LV-2", 800),
        ("비상용", "EM-1", 1), ("비상용", "EM-2", 1), ("비상용", "EM-3", 1),
        ("B1F", "LV-1", 1200), ("B1F", "LV-2", 1200), ("B1F", "LV-3", 1200),
        ("B2F", "LV-1", 1200), ("B2F", "LV-2", 1200), ("B3F", "LV-1", 1200),
        ("B3F", "LV-2", 1200), ("B4F", "LV-1", 800), ("B4F", "LV-2", 1200),
        # 여기에 기존 리스트를 모두 복사해서 넣으시면 됩니다.
    ]

    # 2. 입력창 섹션 (3열 배치로 공간 절약)
    with st.expander("📝 지침 입력창 (클릭하여 열기)", expanded=True):
        inputs = {}
        cols = st.columns(3)
        for i, (loc, name, mul) in enumerate(data):
            label = f"{loc} - {name}"
            inputs[label] = cols[i % 3].number_input(f"{label} (×{mul})", key=f"in_{label}", step=0.1)

    if st.button("💾 데이터 서버 저장", type="primary"):
        save_data(date_str, "계량기", inputs)

    # 3. 기존 HTML 출력 양식 (출력 및 인쇄용)
    rows_html = "".join([
        f"<tr><td>{loc}</td><td>{name}</td><td style='color:blue; font-weight:bold;'>{inputs[f'{loc} - {name}'] if inputs[f'{loc} - {name}'] > 0 else ''}</td><td>{mul}</td></tr>"
        for loc, name, mul in data
    ])
    
    html_template = f"""
    <div style="background:white; padding:15mm; color:black; width:190mm; margin:0 auto; font-family:'Noto Sans KR';">
        <h2 style="text-align:center; text-decoration:underline;">전기실 계량기 검침표</h2>
        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold;">
            <span>검침일자: {date_str}</span>
            <span>점검자: ________________ (인)</span>
        </div>
        <table style="width:100%; border-collapse:collapse; text-align:center; border:2px solid black;">
            <thead><tr style="background:#f2f2f2;">
                <th style="border:1px solid black; height:30px;">비고</th>
                <th style="border:1px solid black;">판넬명</th>
                <th style="border:1px solid black;">당월지침</th>
                <th style="border:1px solid black;">배율</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div class="no-print" style="margin-top:20px; text-align:center;">
            <button onclick="window.print()" style="padding:10px 25px; background:#FF9800; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">🖨️ 이 양식으로 인쇄하기</button>
        </div>
    </div>
    <style>
        td {{ border: 1px solid black; height: 25px; font-size: 11px; }}
    </style>
    """
    components.html(html_template, height=800, scrolling=True)

# --- [메뉴 2] 자고객/MOF/인버터 등 (동일한 구조로 확장 가능) ---
def show_other_page(title, date_str):
    st.subheader(f"📊 {title}")
    st.info("기존 코드를 이 통합 시스템 구조에 맞춰 순차적으로 결합할 예정입니다.")

# --- [메뉴 3] 데이터 조회 ---
def show_db_view():
    st.header("📋 누적 데이터 조회")
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 엑셀(CSV) 다운로드", csv, f"검침데이터_{datetime.now().strftime('%Y%m%d')}.csv")
    else:
        st.info("저장된 데이터가 없습니다.")

# --- 메인 실행 컨트롤러 ---
def main():
    with st.sidebar:
        st.title("📂 통합 검침 시스템")
        menu = st.radio("메뉴 선택", ["계량기 검침", "MOF 검침", "자고객 검침", "인버터 운전일지", "📊 데이터 조회"])
        date_str = st.date_input("🗓️ 검침 일자", datetime.now()).strftime('%Y-%m-%d')
        st.markdown("---")
        st.write("Logged in: Admin")

    if menu == "계량기 검침":
        show_electricity_meter(date_str)
    elif menu == "📊 데이터 조회":
        show_db_view()
    else:
        show_other_page(menu, date_str)

if __name__ == "__main__":
    main()
