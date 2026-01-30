import streamlit as st
from googleapiclient.discovery import build

# 1. 페이지 설정
st.set_page_config(page_title="코끼리 유튜브 분석기", page_icon="🐘", layout="wide")
st.title("🐘 코끼리 유튜브 실시간 분석기")
st.write("주인님, 분석하고 싶은 키워드를 입력하고 버튼을 눌러주세요!")

# 2. Secrets에서 안전하게 API 키 불러오기
try:
    # Streamlit Secrets에 저장한 이름 'YOUTUBE_API_KEY'와 똑같아야 합니다.
    api_key = st.secrets["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
except Exception as e:
    st.error(f"설정 에러: Secrets에서 'YOUTUBE_API_KEY'를 찾을 수 없습니다. ({e})")
    st.stop()

# 3. 사용자 입력창
keyword = st.text_input("검색 키워드", value="경제 전망")
num_results = st.slider("가져올 결과 개수", 1, 10, 5)

# 4. 검색 실행
if st.button("🚀 실시간 데이터 긁어오기"):
    with st.spinner('유튜브에서 정보를 가져오는 중입니다...'):
        try:
            request = youtube.search().list(
                part='snippet',
                q=keyword,
                type='video',
                maxResults=num_results
            )
            response = request.execute()
            
            st.success(f"'{keyword}'에 대한 검색 결과입니다!")
            for item in response['items']:
                title = item['snippet']['title']
                video_id = item['id']['videoId']
                st.write(f"✅ **{title}**")
                st.video(f"https://www.youtube.com/watch?v={video_id}")
                st.divider()
                
        except Exception as e:
            st.error(f"데이터를 가져오지 못했습니다. 에러내용: {e}")
