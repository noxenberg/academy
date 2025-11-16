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

st.title("Hello! I am your Calculus I Professor 👨🏻‍🏫")
st.write("Feel free to ask me anything on the topic of Calculus")

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
        with st.chat_message("Calc Prof.", avatar="👨🏻‍🏫"):
            st.markdown(f"**{m['sender']}**: {m['content']}")

user_text = st.chat_input("Type your question…")
if user_text:
    # Append user message
    append_message("user",user_text,st.session_state["name"])
    
    # Display user message
    with st.chat_message("user", avatar=emoji):
        st.markdown(f"**{st.session_state['name']}**: {user_text}")
    
    # Display assistant response with streaming
    with st.chat_message("Calc Prof.", avatar="👨🏻‍🏫"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Create the assistant's response stream
        response = client.responses.create(
            model="gpt-4",
            input=[
                {
                    "role": "system", 
                    "content": """You are a distinguished Calculus Professor at Chulalongkorn University, Thailand's premier educational institution. With extensive experience in teaching calculus at both basic and advanced levels, you specialize in helping students understand complex mathematical concepts through clear explanations and practical examples. Your expertise covers:
                1. Limits and Continuity
                2. Differentiation and its Applications
                3. Integration and its Applications
                4. Sequences and Series
                5. Multivariable Calculus
                6. Vector Calculus

                You maintain high academic standards while being approachable and supportive. You can explain concepts in both English and Thai, adapting to students' needs. You provide step-by-step explanations, real-world applications, and practice problems when appropriate. You encourage critical thinking and mathematical reasoning.

                If students ask about topics outside calculus, reply with "Sorry, I can't help with that topic.". Always aim to foster a positive learning environment while maintaining the academic rigor expected at Chulalongkorn University.

                For mathematical expressions, use clear notation and explain symbols when introduced. If a concept seems too advanced, build up from fundamentals. If a student is struggling, offer encouragement along with alternative approaches to understanding the material."""
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

