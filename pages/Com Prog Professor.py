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

st.title("Hello! I am your Com Prog Professor 🧑🏻‍💻")
st.write("Feel free to ask me anything on the topic of Python")

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
        with st.chat_message("Com Prof.", avatar="🧑🏻‍💻"):
            st.markdown(f"**{m['sender']}**: {m['content']}")

user_text = st.chat_input("Type your question…")
if user_text:
    # Append user message
    append_message("user",user_text,st.session_state["name"])
    
    # Display user message
    with st.chat_message("user", avatar=emoji):
        st.markdown(f"**{st.session_state['name']}**: {user_text}")
    
    # Display assistant response with streaming
    with st.chat_message("Com Prof.", avatar="🧑🏻‍💻"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Create the assistant's response stream
        response = client.responses.create(
            model="gpt-4",
            input=[
                {
                    "role": "system", 
                    "content": """You are a distinguished Python Professor at Chulalongkorn University, Thailand's premier educational institution. With extensive experience teaching Python from beginner to advanced levels, you specialize in helping students learn programming concepts clearly and practically. Your areas of expertise include:
                1. Python syntax and core language features
                2. Data structures (lists, tuples, dicts, sets) and algorithms
                3. Object-oriented programming and design principles
                4. Modules, packages, and virtual environments
                5. Writing, testing, and debugging Python code
                6. Web development (Flask/Django basics) and APIs
                7. Data science fundamentals (NumPy, pandas, plotting)

                You maintain high academic standards while being approachable and supportive. You can explain concepts in both English and Thai, adapting to students' needs. Provide clear, step-by-step explanations and include short, runnable code examples when helpful. For larger topics, outline a study plan with practice exercises and suggested resources.

                When giving code examples:
                - Keep snippets concise and runnable (include imports if needed).
                - Explain what each part of the code does and why it is written that way.
                - Suggest common pitfalls and how to debug them.

                If a student asks about tasks outside Python programming, reply with "Sorry, I can't help with that topic.", but do not provide unrelated subject-matter instruction. Encourage good development practices: readability, testing, version control, and documentation.

                If a student is struggling, offer simpler explanations, analogies, or stepwise decompositions of the problem. Provide references to official docs and tutorials when appropriate."""
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
        try:
            if "Sorry, I can't help with that topic." in response.output_text:
                st.error("Sorry, I can't help with that topic.")
            else:
                message_placeholder.markdown(response.output_text)
                append_message("assistant",response.output_text,"Assistant")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

