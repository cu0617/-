import streamlit as st
import streamlit.components.v1 as components

def show_mof_detail(date_str):
    sections = [
        {"title": "전력검침량 (SHV 1-4, 사무동)", "sub": "(배율 : *7200)", "meter": "01-3537-4119",
         "items": [
            ("9", "A 시간대(순방향) 유효전력량 전월 (중부하)", "KWH"),
            ("10", "B 시간대(순방향) 유효전력량 전월 (최대부하)", "KWH"),
            ("11", "C 시간대(순방향) 유효전력량 전월 (경부하)", "KWH"),
            ("12", "A 시간대(지상) 무효전력량 전월", "KVARH"),
            ("13", "B 시간대(지상) 무효전력량 전월", "KVARH"),
            ("14", "A 시간대 누적최대수요전력 전월", "KW"),
            ("15", "B 시간대 누적최대수요전력 전월", "KW")
        ]},
        {"title": "전력검침량 (SHV 2-4, 판매동)", "sub": "(배율 : *7200)", "meter": "01-3537-4155",
         "items": [
            ("9", "A 시간대(순방향) 유효전력량 전월 (중부하)", "KWH"),
            ("10", "B 시간대(순방향) 유효전력량 전월 (최대부하)", "KWH"),
            ("11", "C 시간대(순방향) 유효전력량 전월 (경부하)", "KWH"),
            ("12", "A 시간대(지상) 무효전력량 전월", "KVARH"),
            ("13", "B 시간대(지상) 무효전력량 전월", "KVARH"),
            ("14", "A 시간대 누적최대수요전력 전월", "KW"),
            ("15", "B 시간대 누적최대수요전력 전월", "KW")
        ]},
        {"title": "전력검침량 (SHV 3-3, 빙축열)", "sub": "(배율 : *6000)", "meter": "01-3537-4164",
         "items": [("7", "전월 누적 유효전력량 (기타시간대)", "KWH"), ("8", "전월 누적 유효전력량 (심야시간대)", "KWH"), ("9", "전월 누적 무효전력량", "KVAR"), ("10", "전월 누적 최대수요전력", "KW")]},
        {"title": "전력검침량 (LVB417, 정화조)", "sub": "(배율 : *60)", "meter": "01-3537-4128",
         "items": [
             ("4", "전월 누적 수전 유효전력량(KWh)-A (중간시간)", "KWH"),
             ("5", "전월 누적 수전 유효전력량(KWh)-B (최대부하)", "KWH"),
             ("6", "전월 누적 수전 유효전력량(KWh)-C (경부하)", "KWH"),
             ("7", "전월 누적 수전 지상 무효전력량(KWh)-A(중간부하)", "KVARH"),
             ("8", "전월 누적 수전 지상 무효전력량(KWh)-B(최대부하)", "KVARH"),
             ("9", "전월 누적 수전 지상 무효전력량(KWh)-C(경부하)", "KVARH"),
             ("10", "전월 누적 수전최대수요전력(KW) - A (중간시간)", "KW"),
             ("11", "전월 누적 수전최대수요전력(KW) - B (최대부하)", "KW")
        ]}
    ]

    def generate_html_content():
        content = ""
        for sec in sections:
            rows = "".join([f"<tr><td>{i[0]}</td><td class='left'>{i[1]}</td><td>{i[2]}</td><td><input type='number' class='inp-val' placeholder='-'></td></tr>" for i in sec['items']])
            content += f"""
            <div class='section-header'><div>{sec['title']}<br><small>{sec['sub']}</small></div><div class='meter-no'>계량기 번호<br>({sec['meter']})</div></div>
            <table><thead><tr><th width='10%'>순번</th><th width='55%'>내용</th><th width='15%'>단위</th><th width='20%'>당월지침</th></tr></thead><tbody>{rows}</tbody></table>
            <div style='height:10px;'></div>"""
        return content

    html_template = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        body {{ font-family: 'Noto Sans KR', sans-serif; margin: 0; padding: 20px 0; display: flex; flex-direction: column; align-items: center; background-color: #525659; overflow-x: hidden;}}
        
        .paper {{ width:95%; max-width: 210mm; min-height: 297mm; background: white; padding: 12mm 15mm; color: black; box-sizing: border-box; box-shadow: 0 0 10px rgba(0,0,0,0.5); page-break-after: avoid; }}
        h2 {{ text-align: center; margin: 0 0 15px 0; font-size: 22px; text-decoration: underline; }}
        .info {{ display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 10px; font-weight: bold; }}
        
        .section-header {{ display: flex; justify-content: space-between; align-items: center; background: #fff; border: 1px solid #000; border-bottom: none; padding: 5px 10px; font-size: 11px; font-weight: bold; text-align: center; }}
        .meter-no {{ border-left: 1px solid #000; padding-left: 10px; width: 110px; }}
        
        table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 5px; }}
        th, td {{ border: 1px solid #000; text-align: center; font-size: 11px; height: 21px; }}
        th {{ background: #f2f2f2; }}
        .left {{ text-align: left; padding-left: 8px; font-size: 10.5px; }}
        
        /* 입력창 스타일 */
        .inp-name {{ border: none; border-bottom: 1px dotted #000; width: 100px; text-align: center; background: #fffde7; font-weight: bold; }}
        .inp-val {{ width: 90%; border: none; background: #fffde7; text-align: center; font-size: 11px; height: 20px; }}
        .inp-val:focus {{ background: #fff; outline: 1px solid #28a745; }}

        /* 버튼 개별 설정 */
        .btn {{ position: fixed; padding: 10px 20px; color: white; border: none; border-radius: 50px; cursor: pointer; font-weight: bold; z-index: 100; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
        #btn-save {{ position: absolute; top: 30px; right: 130px; background: #28A745; }}
        #btn-print {{ top: 30px; right: 30px; background: #FF9800; }}
        #btn-reset {{ top: 30px; left: 30px; background: #444; }}

        @media print {{
            @page {{ size: A4; margin: 0; }}
            body {{ padding: 0; background: white; }}
            .btn {{ display: none !important; }}
            .paper {{ box-shadow: none; margin: 0; width: 210mm; height: 280mm; padding: 15mm; overflow: hidden; }}
            .inp-val, .inp-name {{ background: transparent !important; border: none; }}
            input[type=number]::-webkit-inner-spin-button {{ display: none; }}
        }}
    </style>

    <script>
        function resetMOF() {{
            if(confirm("모든 MOF 지침 데이터를 초기화하시겠습니까?")) {{
                document.querySelectorAll('.inp-val').forEach(input => input.value = "");
                document.querySelectorAll('.inp-name').forEach(input => input.value = "");
            }}
        }}
    </script>
    <button id="btn-save" class="btn" onclick="saveData()">💾 저장</button>
    <button id="btn-print" class="btn" onclick="window.print()">🖨️ 인쇄</button>
    <button id="btn-reset" class="btn" onclick="resetMOF()">🗑️ 데이터 초기화</button>

    <div class="paper">
        <h2>주변전실 MOF 검침표</h2>
        <div class="info">
            <span>검침 일자: {date_str}</span>
            <span>점검자: <input type="text" class="inp-name" placeholder="         "> (인)</span>
        </div>
        {generate_html_content()}
    </div>
    """
    components.html(html_template, height=1200, scrolling=True)
