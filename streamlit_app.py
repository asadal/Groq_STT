from openai import OpenAI
import os
import streamlit as st

def app():
    st.set_page_config(
        page_title="Groq Speech-to-Text",
        page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Speaker_Icon.svg/1024px-Speaker_Icon.svg.png"
    )

    # 세션 상태 초기화 체크
    if "script_text" not in st.session_state:
        st.session_state.script_text = None
    if "filename" not in st.session_state:
        st.session_state.filename = None
    if "audio_file" not in st.session_state:
        st.session_state.audio_file = None 

    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("Groq Speech-to-Text")
    with col2:
        if st.button("clear ↺"):
            st.session_state.audio_file = None
            st.session_state.filename = None
            st.session_state.script_text = None  # 세션 상태에서 본문 텍스트도 초기화
            st.rerun()

    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Speaker_Icon.svg/1024px-Speaker_Icon.svg.png", width=150)
    
    groq_api_key = st.text_input("Groq API Key", type="password", placeholder="Groq API Key")
    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg"])
    
    if st.button("Transcribe"):
        if groq_api_key:
            groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
            if audio_file:
                st.session_state.audio_file = audio_file
                st.session_state.filename = audio_file.name

                transcript = groq.audio.transcriptions.create(
                    model='whisper-large-v3', 
                    file=audio_file,
                    response_format='text'
                )
                st.session_state.script_text = transcript  # 스크립트 텍스트 세션 상태에 저장
            else:
                st.error("Audio File is not uploaded")
        else:
            st.error("Groq API Key is not set")
    
    if st.session_state.script_text:
        file_head = os.path.splitext(st.session_state.filename)[0]
        script_text = st.text_area("Script Text", value=st.session_state.script_text, height=500)
        st.download_button(
            label="Download Script", 
            data=script_text, 
            file_name=file_head + ".txt", 
            mime="text/plain"
        )

if __name__ == "__main__":
    app()
