import streamlit as st
import streamlit.components.v1 as components

def show_electricity_meter(date_str):
    st.subheader("⚡ 전기실 계량기 검침표")
    
    # 1. 데이터 리스트 (필요시 별도 csv에서 불러오도록 수정 가능)
    data = [
        ("39층", "HV39-1", 3000), ("10층(CGV)", "LV-1", 2400), ("10층(극장)", "LV-2", 800), ("10층(극장)", "LV-4", 240),
        ("총변전실", "LV9B-1", 240), ("총변전실", "LV9A-1", 240), ("", "LV8B-1", 1000), ("", "LV8B-1E", 1000),
        ("", "LV8A-1", 1000), ("", "LV8A-1E", 240), ("", "LV7B-1", 1000), ("", "LV7B-1E", 240),
        ("", "LV7A-1", 1000), ("", "LV7A-1E", 240), ("", "LV6A-1", 1000), ("", "LV6A-1E", 240),
        ("", "LV6B-1", 1000), ("", "LV6B-1E", 240), ("", "LV5B-1", 1000), ("", "LV5B-1E", 240),
        ("", "LV5A-1", 1000), ("", "LV5A-1E", 240), ("", "LV4A-1", 1000), ("", "LV4A-1E", 240),
        ("", "LV4B-1", 1000), ("", "LV4B-1E", 240), ("", "LV3B-1", 1000), ("", "LV3B-1E", 240),
        ("", "LV3A-1", 1000), ("", "LV3A-1E", 240), ("", "LV2A-1", 1000), ("", "LV2A-1E", 240),
        ("", "LV2B-1", 1000), ("", "LV2B-1E", 240), ("1F 엔터", "LV1B-1", 400), ("1F 엔터", "LV1A-1", 240),
        ("", "LVB1A-1", 1000), ("", "LVB1A-1E", 1200), ("", "LVB1B-1", 1000), ("", "LVB1B-1E", 1200),
        ("MART 2", "SHV1-2", 9600), ("MART 2", "HV1-1", 7200), ("", "LVB-41", 800), ("", "LVB-44", 800),
        ("", "LVB-47", 1280), ("", "HV2-1", 7200), ("롯데마트", "HV2-4", 2400), ("롯데마트", "LVB2-1", 1000),
        ("", "LVB-412", 800), ("", "LVB-414", 800), ("", "LVB-418", 1280), ("MART 1", "HV4-1", 7200),
        ("", "HV3-1", 7200), ("", "SHV2-2", 9600), ("MART 3", "SHV3-2", 7200), ("", "HV6-1", 6000),
        ("", "HV5-1", 6000), ("", "LVB-423", 1280), ("", "LVB-424", 1000)
    ]

    all_names = [item[1] for item in data]
    targets = st.multiselect("🚨 집중 확인 판넬", all_names, default=["LV-1", "LV1B-1", "LV1A-1", "HV2-4", "LVB2-1"])
    summary_data = [d for d in data if d[1] in targets]

    def make_table(items, is_summary=False):
        if not items and is_summary: return "<p style='text-align:center;'>선택된 계량기 없음</p>"
        rows = "".join([f"<tr><td class='bg'>{v}</td><td class='nm'>{n}</td><td><input type='number' class='inp-meter' data-panel='{n.replace('-','_')}' oninput='syncInput(this)'></td><td class='bg'>{m}</td></tr>" for v, n, m in items])
        return f"<table><thead><tr><th>비고</th><th>판넬명</th><th>당월지침</th><th>배율</th></tr></thead><tbody>{rows}</tbody></table>"

    half = (len(data) + 1) // 2
    html_code = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        body {{ font-family: 'Noto Sans KR', sans-serif; background:#525659; display:flex; flex-direction:column; align-items:center; padding:20px; }}
        .btn {{ position:fixed; padding:12px 25px; border:none; border-radius:50px; cursor:pointer; font-weight:bold; color:white; z-index:9999; box-shadow:0 4px 15px rgba(0,0,0,0.4); }}
        #btn-save {{ top:270px; right:130px; background:#28A745; }} #btn-print {{ top:270px; right:20px; background:#FF9800; }} #btn-reset {{ top:270px; left:20px; background:#444; }}
        .container {{ width:210mm; }} .summary-section {{ background:#fff; padding:15px; border-radius:8px; margin-bottom:20px; border-top:5px solid #ff5722; }}
        .paper {{ width:210mm; height:296mm; background:white; padding:10mm; box-shadow:0 0 15px rgba(0,0,0,0.5); }}
        h2 {{ text-align:center; text-decoration:underline; font-size:18px; }}
        .info {{ display:flex; justify-content:space-between; font-size:12px; border-bottom:2px solid #000; padding-bottom:5px; margin-bottom:10px; }}
        table {{ width:100%; border-collapse:collapse; table-layout:fixed; font-size:10px; }}
        th, td {{ border:1px solid #000; text-align:center; height:22px; }}
        th {{ background:#f2f2f2; }} .bg {{ background:#fafafa; font-size:9px; }} .nm {{ text-align:left; padding-left:3px; font-weight:bold; }}
        .inp-meter, .inp-name {{ border:none; background:#fffde7; text-align:center; width:95%; font-weight:bold; }}
        @media print {{ .btn, .summary-section {{ display:none; }} .paper {{ box-shadow:none; padding:0; }} .inp-meter {{ background:none; color:blue; }} }}
    </style>
    <script>
        function syncInput(el) {{ 
            const val = el.value;
            document.querySelectorAll(`input[data-panel="${{el.getAttribute('data-panel')}}"]`).forEach(t => t.value = val);
        }}
        function resetData() {{ if(confirm("초기화하시겠습니까?")) document.querySelectorAll('.inp-meter, .inp-name').forEach(i => i.value = ""); }}
        function saveData() {{ alert("데이터 저장 기능(DB)은 Python 백엔드 연동이 필요합니다."); }}
    </script>
    <button id="btn-save" class="btn" onclick="saveData()">💾 저장</button>
    <button id="btn-print" class="btn" onclick="window.print()">🖨️ 인쇄</button>
    <button id="btn-reset" class="btn" onclick="resetData()">🗑️ 리셋</button>
    <div class="container">
        <div class="summary-section"><h3>🚨 주요 계량기 집중 확인</h3>{make_table(summary_data, True)}</div>
        <div class="paper">
            <h2>전기실 계량기 검침표</h2>
            <div class="info"><span>검침 일자: {date_str}</span><span>점검자: <input type="text" class="inp-name" style="width:80px; border-bottom:1px dotted #000;"> (인)</span></div>
            <div style="display:flex; justify-content:space-between;">
                <div style="width:49%">{make_table(data[:half])}</div>
                <div style="width:49%">{make_table(data[half:])}</div>
            </div>
        </div>
    </div>
    """
    components.html(html_code, height=1350, scrolling=True)
