import streamlit as st

st.set_page_config(page_title="Credits", page_icon="🫶", layout="centered")

with st.sidebar:
    st.page_link("home.py", label="Home", icon="🏛️")
    st.page_link("pages/Calculus Professor.py", label="Calculus I Professor", icon="👨🏻‍🏫")
    st.page_link("pages/Com Prog Professor.py", label="Com Prog Professor", icon="🧑🏻‍💻")
    st.page_link("pages/Physics Professor.py", label="Physics I  Professor", icon="🧑🏻‍🔬")
    st.page_link("pages/Project Manager.py", label="Project Manager", icon="🧑🏼‍🎓")
    st.page_link("pages/credit.py", label="Credit", icon="🫶")

st.title("Credits & About")

st.markdown("""
This app (Academ) provides specialized assistant pages for different subjects and roles (Calculus Professor, Python Professor, Physics Professor, Project Manager). The goal is to offer focused, helpful guidance to students at Chulalongkorn University.
""")

st.header("Maintainers")
st.markdown("- Anapat, Supolthit — development and prompt design")

st.header("Contributors")
st.markdown("""
- Anapat, Supolthit — Streamlit framework / Open AI API utilization
- Pattadon, Pattrachonm - Report / Demonstration
""")

st.header("Libraries & Services")
st.markdown("""
- Streamlit — UI framework
- OpenAI — language model (requires API key)
- Python standard library
""")

st.header("Contact")
st.markdown("For questions, bug reports, or contributions, open an issue in the repository or contact the maintainers at: supolthit.r@gmail.com (Smith) / anapatleemakdej@gmail.com (Gop)")

st.header("Version")
st.markdown(":grey[v0.1 — initial prototype]")
