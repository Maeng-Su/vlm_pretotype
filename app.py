import streamlit as st
import tempfile
import pandas as pd
import time
import random
from pathlib import Path
import plotly.express as px

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="JNEWORKS - Behavior Analysis",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 커스텀 CSS로 디자인 개선 ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # style.css 파일이 없을 경우를 대비한 기본 스타일
        st.markdown("""
        <style>
        /* 기본 배경 및 폰트 색상 */
        .stApp {
            background-color: #F0F2F6;
        }
        /* 모든 텍스트를 검은색으로 설정 */
        body, h1, h2, h3, h4, h5, h6, p, div, label, .st-emotion-cache-10trblm, [data-testid="stMarkdownContainer"] p {
            color: #000000 !important;
        }
        /* 사이드바 스타일 */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
        }
        /* 버튼 및 위젯 스타일 */
        .stButton>button {
            border-radius: 20px;
            background-color: #8FDF94; /* 원하는 배경색 */
            color: white; /* 원하는 글자색 */
        }
        /* 로고 옆 제목 스타일 조정 */
        [data-testid="stSidebar"] h1 {
            padding-top: 10px; /* 제목의 상단 여백 조정 */
        }
        </style>
        """, unsafe_allow_html=True)

# style.css 파일 로드 (선택 사항)
local_css("style.css")


# --- 사이드바 구성 ---
with st.sidebar:
    # --- 로고와 텍스트를 가로로 배치 ---
    logo_col, title_col = st.columns([1, 3]) # 로고와 텍스트의 비율을 1:3으로 설정

    with logo_col:
        # 'logo.png' 파일을 app.py와 같은 폴더에 두거나, 이미지 파일의 정확한 경로를 입력하세요.
        logo_path = "./rsc/회사 로고.png"
        if Path(logo_path).is_file():
            st.image(logo_path, width=60) # 로고 너비를 60px로 설정
        else:
            st.image("https://placehold.co/60x60/4A90E2/FFFFFF?text=J&font=sans", width=60)

    with title_col:
        st.title("JNEWORKS")

    st.caption("Behavior Analysis Platform") # 로고 아래에 작은 설명 추가
    st.markdown("---")

    # 메뉴 선택
    selected_menu = st.radio(
        "메뉴를 선택하세요.",
        ["Behavior Analysis", "Analysis results"],
        label_visibility="collapsed",
        key="menu_selection"
    )

    # 선택된 메뉴에 따라 다른 UI 표시 (여기서는 Behavior Analysis만 활성화)
    if selected_menu == "Behavior Analysis":
        st.success("Behavior Analysis 선택됨")
    else:
        st.info("Analysis results 선택됨")


    # 사이드바 하단 공간 확보 및 추가 메뉴
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.button("📞 Contact Support")
    # st.warning("🎁 Free Gift Awaits You!")
    if st.button("🚪 Logout"):
        st.info("로그아웃 되었습니다.")


# --- 메인 페이지 구성 ---
st.header("Behavior Analysis")

# 2개의 컬럼으로 화면 분할
col1, col2 = st.columns([6, 4]) # 비디오와 분석 결과의 비율을 6:4로 설정

with col1:
    st.subheader("Video")
    
    # 동영상 파일 업로더
    uploaded_file = st.file_uploader(
        "비디오를 끌어 놓으세요 또는 클릭해서 업로드하기",
        type=['mp4', 'mov', 'avi', 'mkv']
    )

    if uploaded_file is not None:
        # Streamlit의 st.video는 파일 경로를 요구하므로, 업로드된 파일을 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            video_path = Path(tmp_file.name)
        
        # 비디오 플레이어 출력
        st.video(str(video_path))
        
    else:
        # 업로드 전 안내 메시지
        st.info("분석할 비디오 파일을 업로드해주세요.")


with col2:
    analysis_header = st.container()
    header_col, button_col, reset_col = analysis_header.columns([3, 1, 1])     

    # 업로드 전 안내 메시지 초기화 및 객체화
    placeholder = st.empty()
    with header_col:
        analysis_results_header = st.subheader("Analysis results")  # 제목 객체화

    with button_col:
        analyze_button = st.button("분석 실행", key="analyze")  # 버튼 객체화
    with reset_col:
        reset_button = st.button("초기화", key="reset")  # 버튼 객체화

    # --- 분석 결과 및 메시지 표시 로직 ---
    if analyze_button:
        if uploaded_file:
            with placeholder.container():
                info_message = st.empty()
                info_message.info("동영상 분석 중입니다. 잠시만 기다려 주세요...")
                
                # "분석 중" 메시지가 잠시 보이도록 짧은 지연 추가
                time.sleep(5)

                analysis_results_text = [
                    """• 2.72s ~ 9s :
◦ 작업자의 시선이 책을 향하고, 왼손이 책 근처에 위치합니다.""",
                    """• 11.28s ~ 12.84s :
◦ 작업자의 시선이 왼쪽 선반으로 향합니다.
◦ 왼손으로 왼쪽 선반의 물체를 집어 작업대로 가져옵니다.""",
                    """• 13.84s ~ 18.88s :
◦ 작업자의 시선이 손과 작업대를 번갈아 봅니다.
◦ 왼손으로 작업대의 부품을 잡고, 오른손으로 다른 부품을 끼워 조립합니다.""",
                    """• 23.32s ~ 25.44s :
◦ 작업자의 시선이 앞쪽 선반으로 향합니다.
◦ 오른손으로 앞쪽 선반의 물체를 집어 작업대로 가져옵니다.""",
                    """• 26.48s ~ 28.8s :
◦ 작업자의 시선이 손과 작업대를 번갈아 봅니다.
◦ 오른손에 들고 있는 물체를 작업대의 다른 부품 위에 올려놓습니다.""",
                    """• 31.24s ~ 32.4s :
◦ 작업자의 시선이 왼쪽 선반으로 향했다가 다시 작업대로 돌아옵니다.
◦ 왼손으로 왼쪽 선반의 물체를 집어 작업대로 가져옵니다.""",
                    """• 36.56s ~ 37.92s :
◦ 작업자의 시선이 측정 도구로 향하고, 왼손으로 이를 집어 부품의 위치를 확인합니다.""",
                    """• 39.36s ~ 40.4s :
◦ 작업자의 시선이 스크루드라이버로 향하며, 조립을 위해 오른손으로 스크루드라이버를 집습니다.""",
                    """• 41.2s ~ 44.56s :
◦ 오른손으로 드라이버를 사용하여 조립 부위에 볼트를 조여 고정합니다.
◦ 이 시기 시선은 조립부위에서 고정됩니다.""",
                    """• 44.76s ~ 47.24s :
◦ 오른손으로 사용한 드라이버를 원래 위치에 내려놓습니다."""
                ]

                for line in analysis_results_text:
                    st.text(line)
                    time.sleep(random.uniform(1.5, 3)) # 속도 개선

                # 표로 데이터 출력
                st.markdown("---")
                st.subheader("분석 상세 정보")
                table_data = {
                    '시작 시간 (초)': ['2.72', '11.28', '13.84', '23.32', '26.48', '31.24', '36.56', '39.36', '41.20', '44.76'],
                    '종료 시간 (초)': ['9.0', '12.84', '18.88', '25.44', '28.80', '32.40', '37.92', '40.40', '44.56', '47.24'], 
                    '행동 분류 (Meta_action_label)': [
                        'Consult sheets',
                        'Picking left',
                        'Assemble system',
                        'Picking in front',
                        'Assemble system',
                        'Picking left',
                        'Take measuring rod',
                        'Take screwdriver',
                        'Assemble system',
                        'Put down screwdriver'
                    ]
                }
                df_table = pd.DataFrame(table_data)
                st.dataframe(df_table, use_container_width=True, hide_index=True)

                # --- Gantt 차트 시각화 추가 (수정된 부분) ---
                st.markdown("---")
                st.subheader("행동 타임라인 차트 (Gantt Chart)")

                # 시간 데이터를 숫자로 변환하고, 고유한 Y축을 위해 인덱스를 리셋
                df_chart = df_table.copy().reset_index()
                df_chart['시작 시간 (초)'] = pd.to_numeric(df_chart['시작 시간 (초)'])
                df_chart['종료 시간 (초)'] = pd.to_numeric(df_chart['종료 시간 (초)'])
                # 각 행동의 소요 시간 계산
                df_chart['소요 시간'] = df_chart['종료 시간 (초)'] - df_chart['시작 시간 (초)']

                # Plotly Express의 bar 차트를 사용하여 Gantt 차트 생성
                fig = px.bar(
                    df_chart,
                    x='소요 시간',
                    y='index', # Y축에 고유한 인덱스 값을 사용하여 각 행을 별도로 그림
                    base='시작 시간 (초)',
                    orientation='h', # 수평 막대 차트
                    custom_data=['시작 시간 (초)', '종료 시간 (초)', '행동 분류 (Meta_action_label)'], # hover 정보에 원래 라벨 추가
                    color_discrete_sequence=["#1E90FF"]
                )

                # 마우스를 올렸을 때 표시될 정보(hover) 포맷 지정
                fig.update_traces(
                    hovertemplate='<b>%{customdata[2]}</b><br><br>' + # customdata에서 원래 라벨을 가져옴
                                  '시작 시간: %{customdata[0]:.2f}s<br>' +
                                  '종료 시간: %{customdata[1]:.2f}s<br>' +
                                  '소요 시간: %{x:.2f}s<extra></extra>'
                )

                # 차트 레이아웃 업데이트
                fig.update_layout(
                    title_text='행동 시간 흐름',
                    xaxis_title="동영상 시간 (초)",
                    yaxis_title="행동 분류",
                    plot_bgcolor='white',
                    xaxis=dict(
                        showgrid=True, 
                        gridcolor='lightgray'
                    ),
                    # y축 순서를 표와 같이 위에서부터 표시하고, 라벨을 원래 행동 이름으로 설정
                    yaxis=dict(
                        autorange="reversed", # 0번 인덱스가 위로 오도록 축을 뒤집음
                        tickmode='array',
                        tickvals=df_chart['index'], # Y축 눈금 위치는 인덱스 값
                        ticktext=df_chart['행동 분류 (Meta_action_label)'] # Y축 눈금 텍스트는 실제 행동 분류 이름
                    )
                )
                
                # Streamlit에 차트 표시
                st.plotly_chart(fig, use_container_width=True)


                # 분석 결과 표시
                info_message.success("동영상 분석이 완료되었습니다.")
                st.markdown("---")
        else:
            placeholder.warning("분석할 비디오 파일을 먼저 업로드해주세요.")
    elif reset_button:
        # 참고: 이 버튼은 현재 결과 표시 영역만 초기화합니다.
        placeholder.warning("비디오를 업로드하면 분석 결과가 여기에 표시됩니다.")
    elif uploaded_file is not None:
        placeholder.info("비디오가 업로드되었습니다. '분석 실행' 버튼을 눌러주세요.")
    else:
        # 초기 상태
        placeholder.warning("비디오를 업로드하면 분석 결과가 여기에 표시됩니다.")