import streamlit as st

def init_state():
    """Streamlit 세션 상태를 초기화합니다."""
    if 'power' not in st.session_state:
        st.session_state.power = 'OFF'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Cool'
    if 'target_temp' not in st.session_state:
        st.session_state.target_temp = 25

init_state()

st.set_page_config(layout="centered", page_title="중앙 냉난방 시스템 리모컨")

st.markdown("""
    <style>
    .remote-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        background-color: #f7f9fb; /* 라이트 그레이 배경 */
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
    .temp-control-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 15px;
    }
    .temp-button {
        width: 100px;
        height: 100px;
        font-size: 2rem;
    }
    .current-temp-display {
        font-size: 3rem;
        font-weight: 900;
        color: #3b82f6;
    }
    </style>
    <div class="remote-container">
    """, unsafe_allow_html=True)


st.title("❄️ 중앙 냉난방 시스템 원격 제어")

status_color = "red" if st.session_state.power == 'OFF' else "#10b981"
status_emoji = "🔴" if st.session_state.power == 'OFF' else "🟢"

st.markdown(f"""
    <div class="status-display">
        <span>시스템 상태 {status_emoji}</span>
        <span style="color: {status_color};">{st.session_state.power}</span>
    </div>
    """, unsafe_allow_html=True)


if st.session_state.power == 'ON':
    
    st.info(f"""
    **현재 설정**
    - 모드: {st.session_state.mode}
    - 희망 온도: {st.session_state.target_temp}°C
    """)

    st.header("1. 작동 모드")
    mode_options = ['Cool', 'Heat']
    mode_labels = {'Cool': '냉방 🧊', 'Heat': '난방 🔥'}
    
    cols = st.columns(2)
    for i, mode in enumerate(mode_options):
        is_selected = st.session_state.mode == mode
        
        with cols[i]:
            if st.button(mode_labels[mode], key=f"mode_{mode}", type="primary" if is_selected else "secondary"):
                st.session_state.mode = mode
                st.rerun()
                
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

    temp_col1, temp_col2, temp_col3 = st.columns([1, 2, 1])

    with temp_col1:
        st.button("▲", on_click=increase_temp, key='temp_up', help="온도를 1도 올립니다.")

    with temp_col2:
        st.markdown(f'<div class="current-temp-display">{st.session_state.target_temp}°C</div>', unsafe_allow_html=True)

    with temp_col3:
        st.button("▼", on_click=decrease_temp, key='temp_down', help="온도를 1도 내립니다.")

    st.markdown(f"<div style='text-align: center; margin-top: 10px; font-size: 0.85rem;'>현재 온도 범위: {MIN_TEMP}°C ~ {MAX_TEMP}°C</div>", unsafe_allow_html=True)


    def apply_settings():
        """설정 적용 시뮬레이션 및 피드백"""
        st.toast(f"설정이 적용되었습니다: 모드={st.session_state.mode}, 온도={st.session_state.target_temp}°C", icon='✅')

    st.markdown("---")
    st.button("설정 적용 (시스템에 명령 전송)", on_click=apply_settings, type="primary")

else:
    st.warning("시스템이 현재 꺼져 있습니다. 전원 버튼을 눌러 켜주세요.")

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
