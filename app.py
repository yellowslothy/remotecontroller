import streamlit as st

def init_state():
    """Streamlit 세션 상태를 초기화합니다."""
    if 'power' not in st.session_state:
        st.session_state.power = 'OFF'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Cool'
    if 'target_temp' not in st.session_state:
        st.session_state.target_temp = 25
    if 'fan_speed' not in st.session_state:
        st.session_state.fan_speed = 'Auto'

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
    .stSlider > div > div:nth-child(2) {
        background: #3b82f6 !important; /* 슬라이더 트랙 색상 */
    }
    .stSlider {
        margin-top: 20px;
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
    - 팬 속도: {st.session_state.fan_speed}
    """)

    st.header("1. 작동 모드")
    mode_options = ['Cool', 'Heat', 'Fan', 'Auto']
    mode_labels = {'Cool': '냉방 🧊', 'Heat': '난방 🔥', 'Fan': '송풍 💨', 'Auto': '자동 🔄'}
    
    cols = st.columns(4)
    for i, mode in enumerate(mode_options):
        is_selected = st.session_state.mode == mode
        button_style = "primary" if is_selected else "secondary"
        
        with cols[i]:
            if st.button(mode_labels[mode], key=f"mode_{mode}"):
                st.session_state.mode = mode
                st.rerun()

    st.header("2. 희망 온도")
    
    new_temp = st.slider(
        '온도 설정 (최소 18°C ~ 최대 30°C)',
        min_value=18, 
        max_value=30, 
        value=st.session_state.target_temp, 
        step=1
    )
    st.session_state.target_temp = new_temp
    
    st.header("3. 팬 속도")
    fan_options = ['Low', 'Medium', 'High', 'Auto']
    fan_labels = {'Low': '약풍', 'Medium': '중풍', 'High': '강풍', 'Auto': '자동'}
    
    cols = st.columns(4)
    for i, speed in enumerate(fan_options):
        is_selected = st.session_state.fan_speed == speed
        button_style = "primary" if is_selected else "secondary"
        
        with cols[i]:
            if st.button(fan_labels[speed], key=f"fan_{speed}"):
                st.session_state.fan_speed = speed
                st.rerun()

    def apply_settings():
        """설정 적용 시뮬레이션 및 피드백"""
        st.toast(f"설정이 적용되었습니다: 모드={st.session_state.mode}, 온도={st.session_state.target_temp}°C, 팬={st.session_state.fan_speed}", icon='✅')

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
