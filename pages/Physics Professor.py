import streamlit as st
from openai import OpenAI
with st.sidebar:
    st.page_link("home.py", label="Home", icon="🏛️")
    st.page_link("pages/Calculus Professor.py", label="Calculus I Professor", icon="👨🏻‍🏫")
    st.page_link("pages/Com Prog Professor.py", label="Com Prog Professor", icon="🧑🏻‍💻")
    st.page_link("pages/Physics Professor.py", label="Physics I Professor", icon="🧑🏻‍🔬")
    st.page_link("pages/Project Manager.py", label="Project Manager", icon="🧑🏼‍🎓")
    st.page_link("pages/credit.py", label="Credit", icon="🫶")

client = OpenAI(
    api_key = st.secrets.get("api", {}).get("OPENAI_API_KEY") if "api" in st.secrets else None,
)

def append_message(role,content,sender):
    st.session_state.messages.append({
        "role": role,
        "content":content,
        "sender":sender
        })

st.set_page_config(page_title="Academ",page_icon='📘',layout='centered')

st.title("Hello! I am your Physics Professor 🧑🏻‍💼")
st.write("Feel free to ask me anything on the topic of Physics")

current_response_id = st.session_state.get("current_response_id", None)

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    name = st.text_input("Display name",placeholder = 'Enter name' ,value=st.session_state.get("name", ""))
    emoji = st.selectbox("How are you feeling?",('😀','😴','😊','😩','😒','😍','😑','😎','🥶'))
    join = st.button("Join", type="primary", use_container_width=True)
    if join and name.strip():
        st.session_state["name"] = name.strip()
        append_message("system",f"{name} joined the chat.","system")
if "name" not in st.session_state:
    st.info("Enter your name in the sidebar and click **Join** to begin.")
    st.stop()

for m in st.session_state.messages:
    if m["role"] == "system":
        st.markdown(f"> *{m['content']}*")
    elif m["role"] == "user":
        with st.chat_message("user", avatar=emoji):
            st.markdown(f"**{m['sender']}**: {m['content']}")
    elif m["role"] == "assistant":
        with st.chat_message("Phys Prof.", avatar="🧑🏻‍💼"):
            st.markdown(f"**{m['sender']}**: {m['content']}")

user_text = st.chat_input("Type your question…")
if user_text:
    # Append user message
    append_message("user",user_text,st.session_state["name"])
    
    # Display user message
    with st.chat_message("user", avatar=emoji):
        st.markdown(f"**{st.session_state['name']}**: {user_text}")
    
    # Display assistant response with streaming
    with st.chat_message("Phys Prof.", avatar="🧑🏻‍💼"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Create the assistant's response stream
        response = client.responses.create(
            model="gpt-4",
            input=[
                {
                    "role": "system", 
                    "content": """You are a distinguished Physics Professor at Chulalongkorn University, one of Thailand's leading institutions. With extensive experience teaching physics from introductory to advanced levels, you help students build strong conceptual understanding and problem-solving skills. Your areas of expertise include:
                1. Classical mechanics (kinematics, dynamics, energy, momentum)
                2. Electromagnetism (electrostatics, circuits, Maxwell's equations basics)
                3. Thermodynamics and statistical mechanics
                4. Waves and optics
                5. Modern physics (special relativity, quantum mechanics basics)
                6. Mathematical methods for physics (calculus, linear algebra, differential equations)
                7. Experimental methods and data analysis

                Maintain high academic standards while being approachable and supportive. Explain concepts in both English and Thai where helpful, and adapt explanations to the student's background. Provide step-by-step derivations, worked examples, and clear explanations of assumptions and approximations.

                When presenting equations or derivations:
                - Use clear notation and define all symbols and units.
                - Show intermediate steps when helpful, and provide the physical interpretation of results.
                - Offer common sanity checks and guidance on units and dimensional analysis.

                For problem-solving help:
                - Outline a solution strategy first (identify knowns/unknowns, choose principles to apply).
                - Provide worked examples, then suggest practice problems with increasing difficulty.

                For experimental or computational questions, suggest simple lab setups, measurement strategies, and basic data analysis (including error estimation). Encourage good scientific habits: checking assumptions, verifying limiting cases, and comparing to known results.

                If a student asks about topics outside physics, reply with "Sorry, I can't help with that topic." , but avoid providing unrelated subject-matter instruction. If a student is struggling, offer simpler explanations, analogies, visualizations, or stepwise decompositions of the problem."""
                },
                {
                    "role": "user",
                    "content": user_text,
                },
            ],
            previous_response_id=current_response_id,
            max_output_tokens=1000,
        )
        current_response_id = response.id
        st.session_state["current_response_id"] = current_response_id
        # Process the stream
        try:
            # Check for '6767' in the complete response
            if "Sorry, I can't help with that topic." in response.output_text:
                st.error("Sorry, I can't help with that topic.")
            else:
                message_placeholder.markdown(response.output_text)
                append_message("assistant",response.output_text,"Assistant")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

