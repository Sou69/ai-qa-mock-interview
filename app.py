import streamlit as st
import json
import random
from gtts import gTTS
import io

try:
    from streamlit_mic_recorder import speech_to_text
except ImportError:
    speech_to_text = None

# Configure page settings
st.set_page_config(page_title="AI QA Automation Interview", page_icon="🤖", layout="wide")

# Custom UI Enhancements
st.markdown("""
<style>
    /* Global Styles & Dark Theme Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(20, 25, 43) 0%, rgb(10, 14, 23) 90%);
        color: #c8e6c9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Gradient */
    .header-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Subtitle Styling */
    .subtitle {
        text-align: center; 
        color: #8fa0b5; 
        font-size: 1.1rem;
        margin-bottom: 40px;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
        text-align: center;
    }
    
    .question-card {
        background-color: rgba(20, 25, 43, 0.8);
        border: 1px solid rgba(0, 201, 255, 0.2);
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .score-number {
        font-size: 3.5rem;
        font-weight: bold;
        color: #00C9FF;
        line-height: 1.1;
    }
    
    .score-label {
        font-size: 0.9rem;
        color: #92FE9D;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons (Dynamic Gradient) */
    .stButton>button {
        background: linear-gradient(45deg, rgba(0, 201, 255, 0.15) 0%, rgba(146, 254, 157, 0.15) 100%);
        color: #c8e6c9 !important;
        border: 1px solid rgba(0, 201, 255, 0.5) !important;
        border-radius: 12px;
        transition: all 0.3s ease;
        font-weight: bold;
        height: 50px;
        backdrop-filter: blur(4px);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, rgba(0, 201, 255, 0.4) 0%, rgba(146, 254, 157, 0.4) 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,201,255,0.4);
        border-color: #92FE9D !important;
        color: #ffffff !important;
    }

    /* Dynamic Media Elements (Audio & Mic Iframe) */
    audio {
        border-radius: 50px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,201,255,0.2);
    }
    audio::-webkit-media-controls-panel {
        background: linear-gradient(90deg, #112240 0%, #23395d 100%) !important;
    }

    iframe {
        border-radius: 12px;
        /* Swap bright white iframe background to dark mode intelligently */
        filter: invert(0.85) hue-rotate(180deg);
        box-shadow: 0 4px 15px rgba(146,254,157,0.2);
    }
    
    /* Input Text Area Override */
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #c8e6c9 !important;
    }
    .stTextArea textarea:focus {
        border-color: #00C9FF !important;
        box-shadow: 0 0 0 1px #00C9FF !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

def evaluate_answer(user_ans, correct_ans):
    u = user_ans.lower().strip()
    c = correct_ans.lower().strip()
    if u == c:
        return True
    
    u_words = set(u.split())
    c_words = set(c.split())
    stop_words = {'the', 'is', 'a', 'to', 'of', 'and', 'in', 'it', 'that', 'for', 'on', 'with', 'an', 'by', 'as', 'are', 'what', 'how', 'do'}
    u_words = u_words - stop_words
    c_words = c_words - stop_words
    
    if len(c_words) == 0:
        return u == c

    overlap = u_words.intersection(c_words)
    if len(overlap) / len(c_words) >= 0.4:
         return True
    
    if u in c and len(u) > 3:
         return True
    if c in u:
         return True
        
    return False

def main():
    # Hero Header
    st.markdown('<h1 class="header-title">Elevate AI: QA Interview</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Experience the next generation of technical interviews. Listen to the AI, speak your answers, and receive instant feedback.</p>', unsafe_allow_html=True)
    
    # State Management
    if 'questions' not in st.session_state:
        qs = load_questions()
        random.shuffle(qs)
        st.session_state.questions = qs
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.state = 'asking'
        st.session_state.feedback = ""

    current_index = st.session_state.current_index
    questions = st.session_state.questions
    
    # Layout Grid Using Columns
    col1, spacer, col2 = st.columns([1, 0.1, 2.5])

    # LEFT PANEL: Dashboard & Stats
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin-bottom:5px;">Performance</h4>
            <div class="score-label">Score</div>
            <div class="score-number">{st.session_state.score}</div>
            <hr style="opacity: 0.1; margin: 15px 0;">
            <p style="color:#a1a1aa; margin-bottom:0;">Progress</p>
            <strong style="font-size: 1.2rem;">{current_index} / {len(questions)}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 Restart Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # RIGHT PANEL: Interview Experience
    with col2:
        if current_index >= len(questions):
            st.balloons()
            st.markdown(f"""
            <div class="question-card" style="text-align: center;">
                <h2>🎉 Interview Complete!</h2>
                <h4 style="color:#00C9FF;">Your Final Score: {st.session_state.score} / {len(questions)}</h4>
                <p>Great job practicing your QA Automation concepts.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        q_data = questions[current_index]
        question_text = q_data['question']
        correct_answer = q_data['answer']

        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#00C9FF; font-weight:bold; letter-spacing:1px; margin-bottom:5px;'>QUESTION {current_index + 1}</p>", unsafe_allow_html=True)
        
        # ACTIVE QUESTION STATE
        if st.session_state.state == 'asking':
            st.markdown(f"<h3 style='color:#c8e6c9; margin-top:0;'>{question_text}</h3>", unsafe_allow_html=True)
            
            # Autoplay audio
            audio_fp = text_to_speech(question_text)
            st.audio(audio_fp, format="audio/mp3", autoplay=True)

            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
            
            # Input Methods
            subcol1, subcol2 = st.columns([1, 1])
            with subcol1:
                st.markdown("⌨️ **Type your answer**")
                user_answer = st.text_area("Your Answer:", key=f"input_{current_index}", height=120, label_visibility="collapsed", placeholder="Type your full answer here...")
            
            with subcol2:
                st.markdown("🎤 **Speak your answer**")
                spoken_text = None
                if speech_to_text:
                    spoken_text = speech_to_text(
                         language='en',
                         start_prompt="Record Audio 🔴",
                         stop_prompt="Stop Recording ⏹️",
                         just_once=True,
                         key=f"stt_{current_index}"
                    )
                else:
                    st.warning("Speech recognition is unavailable.")
                
                if spoken_text:
                    st.info(f"**Transcribed:** {spoken_text}")
            
            final_answer = spoken_text if spoken_text else user_answer
            
            st.write("")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit_clicked = st.button("🚀 Submit Answer", type="primary", use_container_width=True)
            with col_btn2:
                skip_clicked = st.button("⏭️ Pass Question", use_container_width=True)
                
            if submit_clicked:
                if final_answer:
                    is_correct = evaluate_answer(final_answer, correct_answer)
                    if is_correct:
                        st.session_state.score += 1
                        st.session_state.feedback = f"✅ **Outstanding!**\n\n**Your Answer:** {final_answer}\n\n**Algorithm's Expected Answer:** {correct_answer}"
                    else:
                        st.session_state.feedback = f"❌ **Not quite right.**\n\n**Your Answer:** {final_answer}\n\n**Algorithm's Expected Answer:** {correct_answer}"
                    
                    st.session_state.state = 'answered'
                    st.rerun()
                else:
                    st.error("⚠️ Please either type or record your answer before submitting.")
                    
            if skip_clicked:
                st.session_state.feedback = f"⏭️ **Question Skipped.**\n\n**Algorithm's Expected Answer:** {correct_answer}"
                st.session_state.state = 'answered'
                st.rerun()

        # FEEDBACK STATE
        elif st.session_state.state == 'answered':
            st.markdown(f"<h4 style='color:#8fa0b5; margin-top:0;'>{question_text}</h4>", unsafe_allow_html=True)
            
            if "✅" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
            
            st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
            if st.button("➡️ Continue to Next Question", type="primary", use_container_width=True):
                st.session_state.current_index += 1
                st.session_state.state = 'asking'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
