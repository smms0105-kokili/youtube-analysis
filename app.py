import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import base64

# 1. 페이지 설정
st.set_page_config(page_title="코끼리 AI 유튜브 마스터", layout="wide")

# 2. 스타일링 (더 세련된 디자인)
st.markdown("""
    <style>
    .main { background-color: #111; }
    .stMetric { background-color: #222; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .video-title { font-size: 18px; font-weight: bold; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (설정 창)
with st.sidebar:
    st.header("🐘 마스터 설정")
    keyword = st.text_input("🎯 분석할 핵심 키워드", value="경제 전망")
    num_results = st.slider("📊 수집 데이터 양", 5, 50, 20)
    st.divider()
    st.write("🚀 **기능 가이드**")
    st.caption("1. 키워드를 입력하고 분석 시작 클릭")
    st.caption("2. 결과가 나오면 표 아래에서 엑셀 다운로드 가능")

st.title("📊 유튜브 실시간 AI 분석 리포트")

# 4. API 연결
try:
    api_key = st.secrets["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
except Exception as e:
    st.error("API 키 연결 확인이 필요합니다.")
    st.stop()

# 5. 엑셀 다운로드 함수
def get_table_download_link(df):
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="youtube_analysis.csv" style="text-decoration:none;"><button style="background-color:#FF4B4B; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">📥 분석 결과 엑셀 저장하기</button></a>'

# 6. 실행 버튼
if st.button("🚀 AI 정밀 분석 및 시각화 시작"):
    with st.spinner('유튜브 서버에서 데이터를 정밀하게 추출 중입니다...'):
        try:
            request = youtube.search().list(
                part='snippet',
                q=keyword,
                type='video',
                maxResults=num_results,
                order='relevance'
            )
            response = request.execute()

            data = []
            for item in response['items']:
                data.append({
                    "날짜": item['snippet']['publishedAt'][:10],
                    "채널명": item['snippet']['channelTitle'],
                    "영상 제목": item['snippet']['title'],
                    "링크": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "썸네일": item['snippet']['thumbnails']['medium']['url']
                })
            
            df = pd.DataFrame(data)

            # --- 상단 대시보드 ---
            c1, c2, c3 = st.columns(3)
            c1.metric("총 분석 수", f"{len(df)}개")
            c2.metric("참여 채널", f"{df['채널명'].nunique()}개")
            c3.metric("최신 기준일", df['날짜'].max())
            st.divider()

            # --- 메인 결과 (이미지와 함께) ---
            st.subheader("🎬 주요 영상 리스트 분석")
            for i in range(len(df)):
                col_img, col_txt = st.columns([1, 3])
                with col_img:
                    st.image(df['썸네일'][i], use_container_width=True)
                with col_txt:
                    st.markdown(f"<p class='video-title'>{df['영상 제목'][i]}</p>", unsafe_allow_html=True)
                    st.write(f"📺 채널: {df['채널명'][i]} | 📅 날짜: {df['날짜'][i]}")
                    st.markdown(f"[🎥 영상 바로보기]({df['링크'][i]})")
                st.write("") # 간격 띄우기

            st.divider()

            # --- 하단 데이터 표 및 엑셀 다운로드 ---
            st.subheader("📋 전체 데이터 표")
            st.dataframe(df[['날짜', '채널명', '영상 제목']], use_container_width=True)
            
            # 엑셀 다운로드 버튼 배치
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"데이터를 가져오지 못했습니다: {e}")
