import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai

# 1. AI 설정 (제미나이 연결)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 가장 빠르고 효율적인 1.5-flash 모델 사용
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"AI 연결 설정 오류: {e}. Secrets에 GEMINI_API_KEY를 확인하세요.")

# 2. 화면 구성 (럭셔리 다크 테마)
st.set_page_config(page_title="KOKIRI AI MASTER", layout="wide")
st.title("🐘 AI 마켓 트렌드 인텔리전스")

# 3. 사이드바 (분석 옵션)
with st.sidebar:
    st.header("⚙️ 설정")
    keyword = st.text_input("🔍 분석 키워드", value="경제 전망")
    num_results = st.slider("📊 분석 영상 수", 5, 20, 10)

# 4. 분석 실행
if st.button("🚀 데이터 분석 및 필승 주제 찾기"):
    try:
        youtube = build("youtube", "v3", developerKey=st.secrets["YOUTUBE_API_KEY"])
        request = youtube.search().list(part='snippet', q=keyword, type='video', maxResults=num_results)
        response = request.execute()
        
        titles = [item['snippet']['title'] for item in response['items']]
        titles_str = "\n".join(titles)

        # AI에게 주제 선정 요청
        prompt = f"""
        당신은 조회수 100만 유튜브 전략가입니다. 
        '{keyword}' 관련 다음 영상들을 분석하여 '돈 되는 주제'를 제안하세요:
        {titles_str}

        [응답 양식]
        1. 현재 핵심 트렌드 (1줄)
        2. 시청자의 숨겨진 니즈 (1줄)
        3. 추천 필승 주제 3가지 (제목과 간단한 이유)
        """
        
        with st.spinner('제미나이 AI가 전략을 수립 중입니다...'):
            ai_res = model.generate_content(prompt)
            st.success("✅ 분석 완료!")
            
            # AI 결과 출력
            st.markdown("---")
            st.header("🏆 AI 전략 아이템 선정")
            st.info(ai_res.text)
            
            # 수집 데이터 목록
            st.markdown("---")
            st.subheader("🎬 수집된 원본 데이터")
            for item in response['items']:
                st.write(f"• {item['snippet']['title']}")
    except Exception as e:
        st.error(f"오류 발생: {e}")
