import streamlit as st

# --- 1. 초기 상태 설정 (Session State 초기화) ---
def init_state():
    """Streamlit 세션 상태를 초기화합니다."""
    if 'power' not in st.session_state:
        st.session_state.power = 'OFF'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Cool'
    if 'target_temp' not in st.session_state:
        st.session_state.target_temp = 25

init_state()

# --- 2. UI 설정 및 레이아웃 (리모컨 디자인 및 배경 이미지) ---
st.set_page_config(layout="centered", page_title="중앙 냉난방 시스템 리모컨")

st.markdown("""
    <style>
    /* 전체 배경 이미지 설정: static 폴더와 1.png 파일명을 사용합니다. */
    div.stApp {
        background-image: url("static/1.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        /* 배경 이미지 위에 반투명한 레이어를 씌워 텍스트 가독성을 높임 */
        background-color: rgba(247, 249, 251, 0.7);
        background-blend-mode: overlay;
    }
    .remote-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        background-color: rgba(255, 255, 255, 0.85); /* 반투명한 흰색 배경 */
        backdrop-filter: blur(5px); /* 배경 이미지를 살짝 블러 처리 */
        font-family: 'Arial', sans-serif;
    }
    .status-display {
        background-color: #1f2937; /* 다크 블루/그레이 디스플레이 */
        color: #10b981; /* 에메랄드 그린 텍스트 */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        transition: all 0.2s;
    }
    .temp-vertical-control {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        margin-top: 15px;
    }
    .current-temp-display {
        font-size: 3rem;
        font-weight: 900;
        color: #3b82f6;
    }
    .temp-control-button {
        width: 100%;
        height: 50px;
        font-size: 1.5rem;
    }
    </style>
    <div class="remote-container">
    """, unsafe_allow_html=True)


st.title("❄️ 중앙 냉난방 시스템 원격 제어")

# --- 3. 상태 표시부 ---
status_color = "red" if st.session_state.power == 'OFF' else "#10b981"
status_emoji = "🔴" if st.session_state.power == 'OFF' else "🟢"

st.markdown(f"""
    <div class="status-display">
        <span>시스템 상태 {status_emoji}</span>
        <span style="color: {status_color};">{st.session_state.power}</span>
    </div>
    """, unsafe_allow_html=True)


# 시스템이 켜져 있을 때만 제어판 표시
if st.session_state.power == 'ON':
    
    # --- 현재 설정 표시 ---
    st.info(f"""
    **현재 설정**
    - 모드: {st.session_state.mode}
    - 희망 온도: {st.session_state.target_temp}°C
    """)

    # --- 4. 작동 모드 제어 ---
    st.header("1. 작동 모드")
    mode_options = ['Cool', 'Heat']
    mode_labels = {'Cool': '냉방 🧊', 'Heat': '난방 🔥'}
    
    cols = st.columns(2)
    for i, mode in enumerate(mode_options):
        is_selected = st.session_state.mode == mode
        
        with cols[i]:
            # 선택된 모드만 primary 색상으로 표시
            if st.button(mode_labels[mode], key=f"mode_{mode}", type="primary" if is_selected else "secondary"):
                st.session_state.mode = mode
                st.rerun()
                
    # --- 5. 희망 온도 제어 (버튼 방식, 수직 배치) ---
    st.header("2. 희망 온도")
    
    MIN_TEMP = 18
    MAX_TEMP = 29
    
    def increase_temp():
        """온도를 1도 올립니다 (최대 29도)."""
        if st.session_state.target_temp < MAX_TEMP:
            st.session_state.target_temp += 1
            st.toast("온도 +1°C", icon="🔼")

    def decrease_temp():
        """온도를 1도 내립니다 (최저 18도)."""
        if st.session_state.target_temp > MIN_TEMP:
            st.session_state.target_temp -= 1
            st.toast("온도 -1°C", icon="🔽")

    # 수직 제어를 위한 컨테이너 시작
    temp_col = st.columns([1, 2, 1])[1] # 중앙 컬럼 확보
    
    with temp_col:
        st.markdown('<div class="temp-vertical-control">', unsafe_allow_html=True)
        
        # 1. 온도 올리기 버튼 (상단)
        st.button("▲", on_click=increase_temp, key='temp_up', help="온도를 1도 올립니다.", 
                  use_container_width=True)
                  
        # 2. 현재 온도 표시 (중앙)
        st.markdown(f'<div style="text-align: center; width: 100%;"><div class="current-temp-display">{st.session_state.target_temp}°C</div></div>', unsafe_allow_html=True)

        # 3. 온도 내리기 버튼 (하단)
        st.button("▼", on_click=decrease_temp, key='temp_down', help="온도를 1도 내립니다.", 
                  use_container_width=True)
                  
        st.markdown('</div>', unsafe_allow_html=True) # 수직 제어 컨테이너 종료

    st.markdown(f"<div style='text-align: center; margin-top: 10px; font-size: 0.85rem;'>현재 온도 범위: {MIN_TEMP}°C ~ {MAX_TEMP}°C</div>", unsafe_allow_html=True)


    # --- 6. 설정 적용 버튼 (실제 시스템 명령 시뮬레이션) ---
    def apply_settings():
        """설정 적용 시뮬레이션 및 피드백"""
        st.toast(f"설정이 적용되었습니다: 모드={st.session_state.mode}, 온도={st.session_state.target_temp}°C", icon='✅')

    st.markdown("---")
    st.button("설정 적용 (시스템에 명령 전송)", on_click=apply_settings, type="primary")

else:
    st.warning("시스템이 현재 꺼져 있습니다. 전원 버튼을 눌러 켜주세요.")

# --- 7. 전원 버튼 (항상 표시) ---
st.markdown("<br>", unsafe_allow_html=True)
power_col1, power_col2, power_col3 = st.columns([1, 2, 1])

with power_col2:
    if st.session_state.power == 'OFF':
        if st.button("전원 켜기 🟢", key='power_on_btn', type="primary"):
            st.session_state.power = 'ON'
            st.rerun()
    else:
        if st.button("전원 끄기 🔴", key='power_off_btn', type="secondary"):
            st.session_state.power = 'OFF'
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
