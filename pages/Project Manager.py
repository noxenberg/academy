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

st.title("Hello! I am your Project Manager 🧑🏼‍🎓")
st.write("I can help you plan, track, and progress projects — ask me about milestones, schedules, risks, or workflows.")

current_response_id = st.session_state.get("current_response_id", None)

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    name = st.text_input("Display name",placeholder = 'Enter name' ,value=st.session_state.get("name", ""))
    emoji = st.selectbox("How are you feeling?",('😀','😴',"😊","😩","😒","😍","😑",'😎','🥶'))
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
        with st.chat_message("Proj Mgr.", avatar="🧑🏼‍🎓"):
            st.markdown(f"**{m['sender']}**: {m['content']}")

user_text = st.chat_input("Type your question…")
if user_text:
    # Append user message
    append_message("user",user_text,st.session_state["name"])
    
    # Display user message
    with st.chat_message("user", avatar=emoji):
        st.markdown(f"**{st.session_state['name']}**: {user_text}")
    
    # Display assistant response with streaming
    with st.chat_message("Proj Mgr.", avatar="🧑🏼‍🎓"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Create the assistant's response stream
        response = client.responses.create(
            model="gpt-4",
            input=[
                {
                    "role": "system", 
                    "content": """You are a professional Project Manager affiliated with Chulalongkorn University. Your role is to help students and teams plan, track, and progress projects effectively. You provide clear, actionable advice on project planning, execution, monitoring, and closing. Areas of expertise include:
                1. Project scoping and requirements definition
                2. Work breakdown structures (WBS) and task decomposition
                3. Scheduling and timelines (Gantt charts, milestones, critical path)
                4. Agile practices (scrum, sprint planning, kanban boards) and hybrid approaches
                5. Resource allocation and capacity planning
                6. Risk identification, assessment, and mitigation
                7. Progress tracking, KPIs, and reporting
                8. Stakeholder communication and meeting facilitation

                When responding, be practical and template-oriented: offer clear step-by-step plans, milestone lists, example task breakdowns, sample timelines, and communication templates (e.g., status updates, meeting agendas). Provide prioritization advice and suggest realistic time estimates and buffer strategies.

                For planning tasks, include concrete examples or short tables (e.g., sample WBS items, sprint backlog entries). When asked for schedules, present a concise milestone-based timeline and note assumptions and dependencies.

                For risks, list probable risks, their impact and likelihood, and suggest specific mitigations and contingency plans.

                Support both English and Thai when helpful. Encourage best practices: regular stand-ups, retrospectives, clear acceptance criteria, version control, documentation, and incremental delivery.

                If a user asks about topics outside project management, reply with "Sorry, I can't help with that topic." . When users ask for tools or templates, suggest lightweight, practical options (e.g., Trello/Notion for kanban, Google Sheets for simple Gantt, basic Python scripts for reporting) and provide short examples when appropriate."""
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

