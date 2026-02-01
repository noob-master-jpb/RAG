import streamlit as st
import random
import time

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
    
def render_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)

def stream_response(text: str, delay: float = 0.05):
    placeholder = st.empty()
    full_text = ""

    for word in text.split():
        full_text += word + " "
        time.sleep(delay)
        placeholder.markdown(full_text + "▌")

    placeholder.markdown(full_text)
    return full_text

def generate_response():
    return random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )

# if "upload" not in st.session_state:
#     st.session_state.upload = False
#     st.session_state.upload = st.button("Upload")
# else:
#     st.session_state.upload = True
    
if True:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    prompt = st.chat_input("What is up?")


    if prompt:
        # Store & render user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        render_message("user", prompt)

        # Generate assistant response
        assistant_text = generate_response()

        # Render assistant message with typing effect
        with st.chat_message("assistant"):
            final_response = stream_response(assistant_text)

        # Store assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": final_response}
        )
    