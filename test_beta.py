import streamlit as st
from datetime import datetime
import difflib

# === Page Setup ===
st.set_page_config(page_title="🎓 DEC Offline Chatbot", layout="wide")

# === Session State ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Sidebar ===
with st.sidebar:
    st.image("D:/pythonProgs/decimage.jpg", width=100)
    st.markdown("## 🎓 Dumka Engineering College")
    st.markdown("This chatbot works offline using built-in DEC info.")
    if st.button("📝 Download Chat Log"):
        filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for speaker, msg in st.session_state.chat_history:
                f.write(f"{speaker}: {msg}\n")
        with open(filename, "rb") as f:
            st.download_button("Download Log", f, file_name=filename)

# === Fallback Answers ===
fallback_qa = {
    "hostel facilities": {
        "brief": "🏠 DEC provides separate hostels for boys and girls with mess and security.",
        "detailed": """🏠 DEC Hostel Info:
- Separate hostels for boys and girls
- Mess, Wi-Fi, study area, 24/7 security
- Allotment based on availability and rules"""
    },
    "cse 6th semester subjects": {
        "brief": "📚 TOC, Web Tech, AI, Electives, Constitution of India, Labs & Project",
        "detailed": """🧠 6th Sem CSE Syllabus:
- **TOC**: Automata, Turing Machines
- **AI**: Search, knowledge representation
- **Web Tech**: HTML, CSS, JS, backend
- Electives: Image Processing etc.
- Labs & Mini Project"""
    },
    "cse 6th semester faculty": {
        "brief": "👨‍🏫 TOC - Mr. Pramanik, AI - Ms. Sunidhi, Web Tech - Mr. Dey (HOD)",
        "detailed": """👩‍🏫 Faculty Allocation:
- TOC: Mr. Amit Pramanik
- AI: Ms. Sunidhi Priyadarsini
- Web Tech: Mr. Ranandeep Dey
- Constitution: Guest Faculty"""
    },
    "branches offered": {
        "brief": "🎓 DEC offers 4 main branches: CSE, CE, EE, ME.",
        "detailed": """🎓 B.Tech Courses Offered:
- Computer Science Engineering (CSE)
- Civil Engineering (CE)
- Electrical Engineering (EE)
- Mechanical Engineering (ME)"""
    },
    "courses offered": {
        "brief": "🎓 B.Tech in CSE, CE, EE, ME under JUT Ranchi.",
        "detailed": """📘 Courses Offered:
- All courses are 4-year B.Tech programs
- Affiliated to Jharkhand University of Technology
- Based on JEE counselling"""
    },
    "contact information": {
        "brief": "📞 Head Office: +91-9007600888, Email: coordinatortigjh@gmail.com",
        "detailed": """📍 DEC Head Office (not campus):
EM-4/1, Sector-V, Salt Lake Electronic Complex, Kolkata-700091  
📞 +91-9007600888  
📧 coordinatortigjh@gmail.com"""
    },
    "college location": {
        "brief": "📍 DEC is located in Dumka, Jharkhand.",
        "detailed": "📍 Dumka Engineering College is a government institution in Dumka district, Jharkhand, India."
    }
}

# === Related Question Keywords ===
related_keys = {
    "branches": "branches offered",
    "brances": "branches offered",
    "course": "courses offered",
    "courses": "courses offered",
    "location": "college location",
    "contact": "contact information",
    "email": "contact information",
    "phone": "contact information",
    "hostel": "hostel facilities",
    "hostals": "hostel facilities",
    "faculty": "cse 6th semester faculty",
    "teachers": "cse 6th semester faculty",
    "syllabus": "cse 6th semester subjects",
    "subject": "cse 6th semester subjects"
}

# === Helper: Match input to fallback key ===
def find_best_match(question):
    question = question.lower()
    if question in fallback_qa:
        return question

    all_keys = list(fallback_qa.keys()) + list(related_keys.keys())
    best = difflib.get_close_matches(question, all_keys, n=1, cutoff=0.4)
    if best:
        key = best[0]
        return related_keys.get(key, key)

    return None

# === Generate Answer ===
def generate_response(user_input):
    detail_level = st.radio("Choose response detail level:", ["brief", "detailed"], horizontal=True)

    matched_key = find_best_match(user_input)
    if matched_key and matched_key in fallback_qa:
        return fallback_qa[matched_key][detail_level]
    return "🤷 Sorry, I don't have information on that yet."

# === Title ===
st.title("🎓 DEC Offline Chatbot")

# === User Input ===
user_query = st.text_input("💬 Ask your question:")
if user_query:
    st.session_state.chat_history.append(("User", user_query))
    with st.spinner("🤖 Thinking..."):
        reply = generate_response(user_query)
    st.session_state.chat_history.append(("Bot", reply))

# === Chat Display with Fixed Styling ===
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
}
.chat-bubble {
    padding: 12px;
    border-radius: 10px;
    max-width: 80%;
    font-size: 16px;
    line-height: 1.5;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.user-bubble {
    align-self: flex-end;
    background-color: #b4f0ae;
    color: black;
}
.bot-bubble {
    align-self: flex-start;
    background-color: #1e1e1e;
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 💬 Chat History")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, message in st.session_state.chat_history:
    role = "user-bubble" if speaker == "User" else "bot-bubble"
    st.markdown(f"<div class='chat-bubble {role}'><b>{speaker}:</b><br>{message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
