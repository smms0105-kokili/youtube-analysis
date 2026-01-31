import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import base64

# 1. 페이지 설정 및 다크 모드 스타일 적용
st.set_page_config(page_title="코끼리 AI 유튜브 마스터", layout="wide")

st.markdown("""
    <style>
    /* 배경 및 글자색 설정 */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    /* 메인 버튼 스타일 (주황색 포인트) */
    div.stButton > button {
        background-color: #FF4B4B; color: white; border-radius: 5px;
        width: 100%; height: 3em; font-weight: bold; border: none;
    }
    /* 카드 형태 디자인 */
    .video-card {
        background-color: #1E1E1E; border-radius: 10px; padding: 20px;
        margin-bottom: 20px; border: 1px solid #333;
    }
    .video-title { color: #FF4B4B; font-size: 1.2em; font-weight: bold; text-decoration: none; }
    .metric-box {
        background-color: #262730; padding: 15px; border-radius: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바 - 설정 메뉴
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3843/3843105.png", width=80)
    st.title("🐘 마스터 설정")
    keyword = st.text_input("🎯 분석 키워드", value="경제 전망")
    num_results = st.slider("📊 데이터 수집량", 5, 50, 15)
    st.divider()
    st.write("✅ **연결 상태**: 최상")
    st.caption("실시간 유튜브 데이터를 정밀 분석합니다.")

# 3. 메인 화면 상단
st.title("📊 유튜브 실시간 키워드 분석 리포트")
st.write(f"현재 **'{keyword}'** 키워드로 수집된 최신 정보를 대시보드 형태로 제공합니다.")

# 4. API 연결
try:
    api_key = st.secrets["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
except:
    st.error("API 키 설정이 필요합니다.")
    st.stop()

# 5. 실행 버튼 및 데이터 분석
if st.button("🚀 AI 정밀 분석 및 대시보드 생성"):
    with st.spinner('데이터를 정밀하게 분석 중입니다...'):
        try:
            request = youtube.search().list(
                part='snippet', q=keyword, type='video',
                maxResults=num_results, order='relevance'
            )
            response = request.execute()

            data = []
            for item in response['items']:
                data.append({
                    "날짜": item['snippet']['publishedAt'][:10],
                    "채널명": item['snippet']['channelTitle'],
                    "제목": item['snippet']['title'],
                    "링크": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "썸네일": item['snippet']['thumbnails']['medium']['url']
                })
            df = pd.DataFrame(data)

            # --- 대시보드 레이아웃 ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='metric-box'><h3>총 분석</h3><h2>{len(df)}개</h2></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='metric-box'><h3>채널 수</h3><h2>{df['채널명'].nunique()}개</h2></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='metric-box'><h3>기준일</h3><h2>{df['날짜'].max()}</h2></div>", unsafe_allow_html=True)
            
            st.divider()

            # --- 카드 뉴스형 리스트 (image_142f6d.jpg 느낌) ---
            st.subheader("🎬 상세 분석 리스트")
            for i in range(len(df)):
                st.markdown(f"""
                <div class="video-card">
                    <div style="display: flex; align-items: flex-start;">
                        <img src="{df['썸네일'][i]}" style="width: 200px; border-radius: 5px; margin-right: 20px;">
                        <div>
                            <a href="{df['링크'][i]}" target="_blank" class="video-title">{df['제목'][i]}</a>
                            <p style="margin-top:10px; color:#AAA;">📺 채널: {df['채널명'][i]} | 📅 게시일: {df['날짜'][i]}</p>
                            <p style="color:#666;">#유튜브분석 #실시간데이터 #코끼리AI</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- 하단 데이터 테이블 ---
            st.divider()
            st.subheader("📋 데이터 통계표")
            st.dataframe(df[['날짜', '채널명', '제목']], use_container_width=True)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
