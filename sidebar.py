import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="전기 설비 검침 시스템", layout="centered")

# 배경색 및 UI 숨기기
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 20px;}
    body, [data-testid="stAppViewContainer"] { background-color: #525659 !important; }
    [data-testid="stSidebar"] { background-color: #262730 !important; color: white; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "usage_data.csv"

def main():
    # 2. 사이드바 구성
    with st.sidebar:
        st.title("📂 검침 시스템")
        st.subheader("메뉴 선택")
        
        menu_options = {
            "계량기 검침": "meter",
            "MOF 검침": "mof",
            "자고객 검침": "second",
            "인버터 운전일지": "inverter",
            "📊 데이터 조회/다운로드": "view_db"
        }
        choice = st.radio("메뉴를 선택하세요", list(menu_options.keys()))
        
        st.markdown("---")
        selected_date = st.date_input("🗓️ 검침 일자 선택", datetime.now())
        date_str = selected_date.strftime('%Y-%m-%d')

    # 3. 메뉴 선택에 따른 화면 표시 (들여쓰기 주의!)
    if choice == "📊 데이터 조회/다운로드":
        st.title("📋 누적 검침 데이터베이스")
        if os.path.exists(DB_FILE):
            view_df = pd.read_csv(DB_FILE)
            st.dataframe(view_df, use_container_width=True)
            csv = view_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 엑셀(CSV) 다운로드", csv, "검침기록.csv", "text/csv")
        else:
            st.info("저장된 데이터가 없습니다.")

    elif choice == "계량기 검침":
        try:
            from electricity_meter import show_electricity_meter
            show_electricity_meter(date_str)
        except Exception as e:
            st.error(f"파일 로드 오류: {e}")

    elif choice == "MOF 검침":
        try:
            from mof import show_mof_detail
            show_mof_detail(date_str)
        except Exception as e:
            st.error(f"파일 로드 오류: {e}")

    elif choice == "자고객 검침":
        try:
            from second_meter import show_second_meter
            show_second_meter(date_str)
        except Exception as e:
            st.error(f"파일 로드 오류: {e}")

    elif choice == "인버터 운전일지":
        try:
            from inverter import show_inverter_log
            show_inverter_log(date_str)
        except Exception as e:
            st.error(f"파일 로드 오류: {e}")

if __name__ == "__main__":
    main()
