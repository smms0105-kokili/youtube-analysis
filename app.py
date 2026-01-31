import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

# 1. 페이지 설정 (화면을 넓게 쓰고 전문가 느낌의 레이아웃)
st.set_page_config(page_title="코끼리 유튜브 AI 분석기", layout="wide")

# 2. 사이드바 디자인 (영상 속 왼쪽 메뉴창 스타일)
with st.sidebar:
    st.title("🐘 AI 분석 설정")
    keyword = st.text_input("분석 키워드 입력", value="경제 전망")
    num_results = st.slider("데이터 수집 개수", 5, 50, 15)
    st.divider()
    st.write("✅ **시스템 상태**: API 연결됨")
    st.info("YouTube Data API v3를 사용하여 실시간 데이터를 수집합니다.")

# 3. 메인 화면 제목
st.title("📊 유튜브 실시간 키워드 분석 대시보드")
st.caption(f"현재 '{keyword}'에 대해 가장 화제가 되는 영상들을 분석 중입니다.")

# 4. API 연결 (이미 설정된 Secrets 사용)
try:
    api_key = st.secrets["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
except Exception as e:
    st.error("API 키 설정이 올바르지 않습니다. Secrets를 확인해주세요.")
    st.stop()

# 5. 분석 시작 버튼
if st.button("🚀 실시간 데이터 정밀 분석 시작"):
    with st.spinner('데이터를 수집하고 분석 리포트를 생성 중입니다...'):
        try:
            request = youtube.search().list(
                part='snippet',
                q=keyword,
                type='video',
                maxResults=num_results
            )
            response = request.execute()

            # 데이터 가공 (표 형태로 만들기 위해)
            video_data = []
            for item in response['items']:
                video_data.append({
                    "게시일": item['snippet']['publishedAt'][:10],
                    "채널명": item['snippet']['channelTitle'],
                    "영상 제목": item['snippet']['title'],
                    "링크": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                })
            
            df = pd.DataFrame(video_data)

            # 상단 요약 카드 (전문가 대시보드 느낌)
            col1, col2, col3 = st.columns(3)
            col1.metric("총 분석 영상", f"{len(df)}개")
            col2.metric("참여 채널 수", f"{df['채널명'].nunique()}개")
            col3.metric("최신 업데이트", df['게시일'].max())

            st.divider()

            # 6. 결과 출력 (영상 속 화면처럼 표 형태로 출력)
            st.subheader("📋 실시간 수집 데이터 리스트")
            # 표에 하이라이트 효과와 넓은 보기 적용
            st.dataframe(df, use_container_width=True, hide_index=True)

            # 7. 간단한 시각화 그래프 추가
            st.subheader("📈 주요 채널별 점유율")
            channel_counts = df['채널명'].value_counts().head(10)
            st.bar_chart(channel_counts)

        except Exception as e:
            st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
