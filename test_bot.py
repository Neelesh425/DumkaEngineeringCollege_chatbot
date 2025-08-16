import streamlit as st
import sounddevice as sd
import soundfile as sf
import whisper
from datetime import datetime
from openai import OpenAI

# === SET YOUR OPENAI API KEY HERE ===
client = OpenAI(api_key="sk-...")  # Replace with your OpenAI key

# === Load Whisper model once ===
whisper_model = whisper.load_model("base")

# === Page configuration ===
st.set_page_config(page_title="🎓 DEC Chatbot Assistant", layout="wide")

# === Chat history ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Sidebar ===
with st.sidebar:
    st.image("D:/pythonProgs/decimage.jpg", width=100)
    st.markdown("## 🎓 Dumka Engineering College")
    st.markdown("Chat via text or voice. Ask about DEC courses, faculty, etc.")
    if st.button("📝 Download Chat Log"):
        filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for speaker, msg in st.session_state.chat_history:
                f.write(f"{speaker}: {msg}\n")
        with open(filename, "rb") as f:
            st.download_button("Download Log", f, file_name=filename)

# === Fallback knowledge base ===
fallback_qa = {
    "cse 6th semester subjects": {
        "brief": "📚 Subjects in 6th Sem CSE:\n- TOC\n- Web Tech\n- AI\n- Electives\n- Constitution of India\n- Labs & Mini Project",
        "detailed": """🧠 Detailed CSE 6th Sem Syllabus:
1. **Theory of Computation**
   - Finite automata, regular expressions
   - Pushdown automata, Turing machines, decidability

2. **Web Technology**
   - HTML, CSS, JS, backend frameworks

3. **Artificial Intelligence**
   - Search, knowledge representation, decision making

4. **Electives**
   - Professional Elective: Image Processing or similar
   - Open Elective

5. **Labs & Mini Project**
   - TOC Lab, AI Lab, Web Tech Lab, Mini Project team work"""
    },
    "cse 6th semester faculty": {
        "brief": "👨‍🏫 Key Faculty for 6th Sem CSE:\n- TOC: Mr. Amit Pramanik\n- AI: Ms. Sunidhi Priyadarsini\n- Web Tech: Mr. Ranandeep Dey (HOD)",
        "detailed": """👩‍🏫 Detailed Faculty Allocation (from routine):
- **Theory of Computation**: Mr. Amit Pramanik
- **Artificial Intelligence**: Ms. Sunidhi Priyadarsini
- **Web Technology**: Mr. Ranandeep Dey
- **Constitution of India**: Guest Faculty

🧪 Labs handled by the same faculty. Scheduling varies by day."""
    }
}

def get_fallback_answer(user_input, detail_level="brief"):
    question = user_input.lower()
    for key in fallback_qa:
        if key in question:
            return fallback_qa[key][detail_level]
    return None

# === Record audio ===
def record_audio(filename="output.wav", duration=5, fs=44100):
    st.info("🎙️ Recording for 5 seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, recording, fs)
    st.success("✅ Recording complete")
    return filename

# === Transcribe audio ===
def transcribe_audio(filepath="output.wav"):
    st.info("🔍 Transcribing...")
    result = whisper_model.transcribe(filepath)
    return result["text"]

# === Generate response ===
def generate_response(prompt):
    detail_level = st.radio("Choose response detail level:", ["brief", "detailed"], horizontal=True)

    # Fallback first
    fallback = get_fallback_answer(prompt, detail_level)
    if fallback:
        return fallback

    # Otherwise, use OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Dumka Engineering College."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# === App title ===
st.title("🎓 DEC Chatbot Assistant with Voice")

# === Input mode: text or voice ===
input_mode = st.radio("Choose Input Mode:", ["Text", "Voice"])

# === Text input ===
if input_mode == "Text":
    user_query = st.text_input("💬 Your question:")
    if user_query:
        st.session_state.chat_history.append(("User", user_query))
        with st.spinner("🤖 Generating response..."):
            reply = generate_response(user_query)
        st.session_state.chat_history.append(("Bot", reply))

# === Voice input ===
elif input_mode == "Voice":
    if st.button("🎤 Record Audio"):
        audio_file = record_audio()
        with st.spinner("🧠 Transcribing and generating response..."):
            transcribed_text = transcribe_audio(audio_file)
            st.session_state.chat_history.append(("User", transcribed_text))
            reply = generate_response(transcribed_text)
            st.session_state.chat_history.append(("Bot", reply))

# === Display chat history ===
st.markdown("## 💬 Chat History")
for speaker, message in st.session_state.chat_history:
    bg_color = "#b4f0ae" if speaker == "User" else "#f0f0f0"
    st.markdown(f"""
    <div style='background-color: {bg_color}; padding: 10px; border-radius: 10px; margin-bottom: 10px; max-width: 75%;'>
        <b>{speaker}:</b><br>{message}
    </div>
    """, unsafe_allow_html=True)
