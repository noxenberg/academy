import streamlit as st

st.set_page_config(
    page_title="Academ - Your Educational Assistant",
    page_icon="📘",
    layout="wide"
)

with st.sidebar:
    st.page_link("home.py", label="Home", icon="🏛️")
    st.page_link("pages/Calculus Professor.py", label="Calculus I Professor", icon="👨🏻‍🏫")
    st.page_link("pages/Com Prog Professor.py", label="Com Prog Professor", icon="🧑🏻‍💻")
    st.page_link("pages/Physics Professor.py", label="Physics I Professor", icon="🧑🏻‍🔬")
    st.page_link("pages/Project Manager.py", label="Project Manager", icon="🧑🏼‍🎓")
    st.page_link("pages/credit.py", label="Credit", icon="🫶")

# Main header with animation
st.markdown(""" <h1 style='text-align: center; color: #1E88E5; animation: fadeIn 2s;'> Welcome to Academ 📘 </h1>
    <p style='text-align: center; color: #87CEEB
; font-size: 1.2em; '>
        Your Intelligent Educational Assistant at Chulalongkorn University
    </p>
    <style>
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

st.divider()

# Introduction
st.markdown("""
## About :blue[Academ]
*Academ is your personalized educational mentor, designed to support your learning journey 
at <a href='https://www.chula.ac.th/en/' target='_blank' style='color:#eea9bf; text-decoration:none;'>
Chulalongkorn University</a>. Whether you need help with calculus problems, Python programming, 
physics concepts, or project management, our specialized assistants are here to help.*
""", unsafe_allow_html=True)


# Feature Cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Key Features 🎯
    - Specialized subject matter experts
    - Bilingual support (English/Thai)
    - Step-by-step explanations
    - Practice problems and examples
    - Real-time interactive assistance
    """)

with col2:
    st.markdown("""
    ### How It Works ⚙️
    1. Choose your assistant from the sidebar
    2. Enter your name to start a session
    3. Ask questions in English or Thai
    4. Get detailed, helpful responses
    5. Practice with suggested exercises
    """)

# Assistant Cards
st.header("Meet Your :gray[Mentors]")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    #### 👨🏻‍🏫 Calculus Professor
    Expert in calculus concepts from basics to advanced topics:
    - Limits and Continuity
    - Differentiation
    - Integration
    - Series and Sequences
    """)

with col2:
    st.markdown("""
    #### 🧑🏻‍💻 Com Prog Professor 
    Your guide to Python programming:
    - Python Fundamentals
    - Data Structures
    - OOP Concepts
    - Libraries & Tools
    """)

with col3:
    st.markdown("""
    #### 🧑🏻‍🔬 Physics Professor
    Physics concepts made clear:
    - Mechanics
    - Electromagnetics
    - Thermodynamics
    - Modern Physics
    """)

with col4:
    st.markdown("""
    #### 🧑🏼‍🎓 Project Manager
    Help with project planning:
    - Task Breakdown
    - Schedules
    - Risk Management
    - Progress Tracking
    """)

# Tips Section
st.divider()
st.markdown("""
<div style="display: flex; justify-content: center;">

<div style="text-align: left;">

### :Blue[Tips] for Best Results
- Be specific in your questions  
- Show your work when asking about problems  
- Ask for examples if concepts aren't clear  
- Use the chat history for context  
- Try both English and Thai for better understanding  

</center>
""", unsafe_allow_html=True)



# Footer
st.divider()
footer_html = """
<div style="text-align: center; margin-top: 20px; color: #666;">
    <p>Made with 💙 for Chulalongkorn University Students</p>
    <p style="font-size: 0.8em;">Have questions? Check out our <a href="credit">credits page</a> for contact information.</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
