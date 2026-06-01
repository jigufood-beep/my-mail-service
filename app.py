import streamlit as st
from google import genai
import os

# 1. 페이지 설정
st.set_page_config(page_title="FIT-SALGI 우체국", layout="centered")
st.title("💌 FIT-SALGI 마음 배달부")
st.subheader("안전하고 따뜻한 마음을 가족에게 전하세요.")

# 2. 사이드바: API 키 입력
# Streamlit Cloud 등에서 환경변수로 키를 관리할 때 유용합니다.
api_key = st.sidebar.text_input("Gemini API 키를 입력하세요", type="password")

# 3. 메인 기능
uploaded_file = st.file_uploader("추억이 담긴 사진을 선택하세요", type=['jpg', 'png'])
sender = st.text_input("보내는 사람")
content = st.text_area("편지 내용을 적어주세요")

if st.button("편지 검사하고 보내기"):
    if not api_key:
        st.error("사이드바에 API 키를 입력해주세요!")
    elif not sender or not content:
        st.warning("내용을 모두 입력해주세요.")
    else:
        # AI 검열 엔진 연결
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("AI가 따뜻한 마음을 검사 중입니다..."):
                prompt = f"""
                당신은 교정시설 편지 보안 검열관입니다. 
                제공된 편지 내용을 분석하여 아래 형식으로 답변하세요.
                
                1. 판정: (안전/위험)
                2. 이유: (위험한 이유)
                3. 순화된 문장: (위험한 표현을 안전하고 따뜻한 언어로 바꾼 문장)
                
                내용: {content}
                """
                response = client.models.generate_content(
                    model="gemini-1.5-flash-latest",
                    contents=prompt
                )
                
                st.success("검사 완료!")
                st.write("---")
                st.write(response.text)
                
                if uploaded_file:
                    st.image(uploaded_file, caption="첨부된 사진", use_container_width=True)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
