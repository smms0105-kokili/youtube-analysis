import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 럭셔리 다크 테마
st.set_page_config(page_title="KOKIRI AI MASTER", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans KR', sans-serif; }
    .stApp { background: radial-gradient(circle, #1a1c23 0%, #07080a 100%); color: #ffffff; }
    
    /* 카드 디자인: 투명도가 있는 유리 느낌 */
    .video-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px; padding: 25px; margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.4s ease;
    }
    .video-card:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: #FF4B4B;
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.2);
    }
    .video-title { color: #ffffff; font-size: 1.3em; font-weight: 700; text-decoration: none; line-height: 1.4; }
    .channel-badge { background: #FF4B4B; color: white; padding: 3px 10px; border-radius: 50px; font-size: 0.8em; font-weight: bold; }
    .metric-title { color: #888; font-size: 0.9em; }
    .metric-value { color: #FF4B4B; font-size: 2em; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바 제어 패널
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐘</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>KOKIRI MASTER</h2>", unsafe_allow_html=True)
    st.divider()
    keyword = st.text_input("🔍 타겟 키워드", value="경제 전망")
    num_results = st.slider("📊 데이터 분석 범위", 10, 50, 25)
    sort_option = st.selectbox("🔃 데이터 정렬", ["관련성순", "최신순"])
    st.divider()
    st.caption("Designed by Gemini & Master smms0105")

# 3. 메인 대시보드
st.title("🛰️ 실시간 마켓 트렌드 인텔리전스")
st.write(f"시스템이 현재 유튜브상의 **'{keyword}'** 데이터를 정밀 트래킹하고 있습니다.")

# 4. 데이터 엔진 가동
try:
    api_key = st.secrets["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
except:
    st.error("API 연동을 확인하세요.")
    st.stop()

if st.button("🚀 데이터 딥다이브 시작"):
    with st.spinner('AI가 실시간 정보를 구조화하고 있습니다...'):
        try:
            order_param = 'date' if sort_option == "최신순" else 'relevance'
            request = youtube.search().list(
                part='snippet', q=keyword, type='video',
                maxResults=num_results, order=order_param
            )
            response = request.execute()

            data = []
            for item in response['items']:
                data.append({
                    "날짜": item['snippet']['publishedAt'][:10],
                    "채널": item['snippet']['channelTitle'],
                    "제목": item["snippet"]["title"],
                    "링크": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "썸네일": item['snippet']['thumbnails']['high']['url']
                })
            df = pd.DataFrame(data)

            # --- 상단 메트릭 섹션 ---
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(f"<div class='metric-title'>총 분석 영상</div><div class='metric-value'>{len(df)}</div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='metric-title'>유효 채널 수</div><div class='metric-value'>{df['채널'].nunique()}</div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='metric-title'>최신 데이터 일자</div><div class='metric-value' style='font-size:1.5em;'>{df['날짜'].max()}</div>", unsafe_allow_html=True)
            with c4: st.markdown(f"<div class='metric-title'>분석 상태</div><div class='metric-value' style='color:#00FF00;'>LIVE</div>", unsafe_allow_html=True)
            
            st.divider()

            # --- 시각화 차트 추가 (진짜 전문가 느낌) ---
            col_chart1, col_chart2 = st.columns([1, 1])
            with col_chart1:
                st.subheader("📈 채널별 점유율 비중")
                fig = px.pie(df, names='채널', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                st.subheader("📅 날짜별 업로드 추이")
                date_counts = df.groupby('날짜').size().reset_index(name='counts')
                fig2 = px.line(date_counts, x='날짜', y='counts', markers=True)
                fig2.update_traces(line_color='#FF4B4B')
                fig2.update_layout(margin=dict(t=20, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

            # --- 하이엔드 카드 리스트 ---
            st.subheader("🎬 AI 정밀 분석 영상 리포트")
            for i in range(len(df)):
                st.markdown(f"""
                <div class="video-card">
                    <div style="display: flex; gap: 30px; align-items: center;">
                        <div style="flex: 1;">
                            <img src="{df['썸네일'][i]}" style="width: 100%; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
                        </div>
                        <div style="flex: 2;">
                            <span class="channel-badge">{df['채널'][i]}</span>
                            <p style="margin-top: 15px;"><a href="{df['링크'][i]}" target="_blank" class="video-title">{df['제목'][i]}</a></p>
                            <p style="color: #888; margin-top: 10px;">📅 분석 일자: {df['날짜'][i]} | 🔗 <a href="{df['링크'][i]}" style="color:#FF4B4B;">원본 영상 보기</a></p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"시스템 오류 발생: {e}")
