import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

# 🔑 주인님의 유튜브 API 키 (이미 설정됨)
API_KEY = 'AIzaSyBdIEh1Nt5pPvWoES07L0x_XnBirlVOc7E'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 웹 페이지 제목 설정
st.set_page_config(page_title="코끼리 유튜브 분석기", page_icon="🐘")
st.title("🐘 코끼리 유튜브 실시간 분석기")
st.write("주인님, 분석하고 싶은 키워드를 입력하고 버튼을 눌러주세요!")

# 입력창과 버튼
keyword = st.text_input("검색 키워드", "경제 전망")
num_results = st.slider("가져올 결과 개수", 1, 10, 5)

if st.button('🚀 실시간 데이터 긁어오기'):
    with st.spinner('유튜브에서 정보를 가져오는 중입니다...'):
        # 유튜브 검색 API 호출
        request = youtube.search().list(
            part='snippet',
            q=keyword,
            type='video',
            maxResults=num_results,
            order='relevance'
        )
        response = request.execute()

        # 결과 출력
        for item in response['items']:
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            video_id = item['id']['videoId']
            
            with st.container():
                st.subheader(f"▶ {title}")
                st.write(f"📺 채널명: {channel}")
                st.video(f"https://www.youtube.com/watch?v={video_id}")
                st.divider()
    st.success("모든 분석 결과를 가져왔습니다!")
