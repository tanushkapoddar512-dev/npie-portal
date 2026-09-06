import os
import sqlite3
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. STREAMLIT CONFIGURATION & PORT HANDLING
# ==========================================
PORT = os.environ.get("PORT", "8501")

st.set_page_config(
    page_title="National & State Government Scheme Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. TRICOLOUR BANNER & NATIONAL UI STYLING
# ==========================================
st.markdown("""
<style>
    /* Indian Flag Top Accent Bar */
    .flag-bar {
        height: 8px;
        width: 100%;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
        border-radius: 4px;
        margin-bottom: 25px;
    }
    /* Welcome Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-left: 6px solid #FF9933;
        border-radius: 12px;
        padding: 24px;
        color: #f8fafc;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .hero-container h2 {
        color: #FF9933;
        margin-top: 0;
        font-weight: 700;
    }
</style>
<div class="flag-bar"></div>
""", unsafe_allow_html=True)

# ==========================================
# 3. FAIL-SAFE IN-MEMORY DATABASE (SQLite)
# ==========================================
@st.cache_resource
def get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            state TEXT NOT NULL,
            max_income INTEGER NOT NULL,
            min_age INTEGER NOT NULL,
            max_age INTEGER NOT NULL,
            target_gender TEXT DEFAULT 'All',
            location TEXT DEFAULT 'All',
            benefit TEXT NOT NULL
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM schemes")
    if cursor.fetchone()[0] == 0:
        schemes_data = [
            ("PMAY-G (Pradhan Mantri Awaas Yojana - Gramin)", "Central", "All", 180000, 18, 70, "All", "Rural", "Financial assistance of ₹1.2 Lakh for house construction"),
            ("Lakshmir Bhandar", "State", "West Bengal", 250000, 25, 60, "Female", "All", "Direct monthly transfer of ₹1000 (General) / ₹1200 (SC/ST)"),
            ("Kanyashree Prakalpa (K1 & K2)", "State", "West Bengal", 120000, 13, 19, "Female", "All", "Annual stipend of ₹1000 and one-time grant of ₹25,000"),
            ("PMEGP (Prime Minister Employment Generation Program)", "Central", "All", 500000, 18, 55, "All", "All", "Subsidized loan assistance up to 35% for new enterprise setups"),
            ("Mukhyamantri Yuva Swavalamban Yojana", "State", "Gujarat", 600000, 17, 25, "All", "All", "Higher education tuition fee support and hostel allowance"),
            ("Ayushman Bharat - PM-JAY", "Central", "All", 120000, 1, 100, "All", "All", "Health cover of ₹5 Lakh per family per year for secondary & tertiary care")
        ]
        cursor.executemany("""
            INSERT INTO schemes (name, type, state, max_income, min_age, max_age, target_gender, location, benefit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, schemes_data)
        conn.commit()
    return conn

conn = get_db()

# ==========================================
# 4. INDIAN VOICE ASSISTANCE (WEB SPEECH API)
# ==========================================
def announce_voice(text, lang="en-IN"):
    clean_text = text.replace('"', '').replace("'", "").replace('\n', ' ')
    js_code = f"""
    <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{clean_text}");
        msg.rate = 0.9;
        msg.pitch = 1.0;
        msg.lang = "{lang}";
        
        var voices = window.speechSynthesis.getVoices();
        for(var i = 0; i < voices.length; i++) {{
            if(voices[i].lang === "{lang}" || voices[i].lang.includes("IN")) {{
                msg.voice = voices[i];
                break;
            }}
        }}
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# ==========================================
# 5. HEADER WITH EMBLEM OF INDIA
# ==========================================
head_col1, head_col2 = st.columns([1, 6])

with head_col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg",
        width=110
    )

with head_col2:
    st.title("राष्ट्रीय एवं राज्य सरकारी योजना पोर्टल")
    st.subheader("National & State Government Scheme Portal")
    st.caption("Government of India Alignment | Citizen Social Welfare & Eligibility Directory")

# Welcome Hero Section
st.markdown("""
<div class="hero-container">
    <h2>🙏 Welcome Citizen / স্বাগতম / स्वागतम्</h2>
    <p>Discover central and state social welfare schemes tailored to your age, household income, and resident state. Filter your eligibility parameters below or listen to voice instructions.</p>
</div>
""", unsafe_allow_html=True)

# Voice Assistance Bar
v_col1, v_col2, v_col3 = st.columns([2, 2, 3])
with v_col1:
    if st.button("🔊 English Voice Guide", use_container_width=True):
        announce_voice("Welcome to the National and State Government Scheme Portal. Select your age, annual household income, and resident state below to check eligible government schemes.", "en-IN")
with v_col2:
    if st.button("🔊 বাংলা দিকনির্দেশনা", use_container_width=True):
        announce_voice("জাতীয় এবং রাজ্য সরকারি প্রকল্প পোর্টালে আপনাকে স্বাগতম। আপনার সুবিধা অনুযায়ী উপযুক্ত সরকারি প্রকল্পগুলি খুঁজে পেতে নিচে আপনার বয়স, বার্ষিক আয় এবং রাজ্য নির্বাচন করুন।", "bn-IN")
with v_col3:
    if st.button("🔊 हिंदी दिशा-निर्देश", use_container_width=True):
        announce_voice("राष्ट्रीय एवं राज्य सरकारी योजना पोर्टल में आपका स्वागत है। अपनी पात्रता के अनुसार सरकारी योजनाओं को खोजने के लिए कृपया नीचे अपनी आयु, वार्षिक आय और राज्य दर्ज करें।", "hi-IN")

st.divider()

# ==========================================
# 6. ELIGIBILITY FILTER FORM
# ==========================================
st.markdown("### 🔎 Citizen Eligibility Criteria")

col1, col2, col3, col4 = st.columns(4)
with col1:
    age = st.number_input("Age (Years)", min_value=1, max_value=100, value=22)
with col2:
    income = st.number_input("Annual Household Income (₹)", min_value=0, value=150000, step=10000)
with col3:
    gender = st.selectbox("Gender", ["All", "Female", "Male", "Other"])
with col4:
    state_opt = st.selectbox("State of Residence", ["All", "West Bengal", "Gujarat", "Maharashtra", "Tamil Nadu", "Delhi"])

if st.button("Find Eligible Schemes 🎯", type="primary", use_container_width=True):
    cursor = conn.cursor()
    query = """
        SELECT * FROM schemes 
        WHERE min_age <= ? AND max_age >= ? 
        AND max_income >= ?
    """
    params = [age, age, income]

    if state_opt != "All":
        query += " AND (state = ? OR state = 'All')"
        params.append(state_opt)

    if gender != "All":
        query += " AND (target_gender = ? OR target_gender = 'All')"
        params.append(gender)

    cursor.execute(query, params)
    results = cursor.fetchall()

    if results:
        count = len(results)
        st.success(f"Found {count} eligible government scheme(s) matching your profile!")
        announce_voice(f"We found {count} eligible schemes for your profile.", "en-IN")

        for r in results:
            with st.expander(f"📌 {r['name']} ({r['type']} Scheme)"):
                st.write(f"**Benefit Details:** {r['benefit']}")
                st.write(f"**Target State:** {r['state']} | **Target Gender:** {r['target_gender']}")
                st.write(f"**Maximum Income Cap:** ₹{r['max_income']:,}")
    else:
        st.warning("No matching schemes found for your current profile inputs.")
        announce_voice("No matching schemes were found for your criteria.", "en-IN")

st.sidebar.title("⚙️ System Status")
st.sidebar.info(f"Active Server Port: **{PORT}**")
st.sidebar.caption("Configured for Streamlit (8501) & PyCafe / Cloud Deployments (5000)")