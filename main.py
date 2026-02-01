import fitz # pip install pymupdf
import streamlit as st
import time
from RAG import *



if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

st.text("DO NOT UPLOAD SENSITIVE FILES. THE DATABASE IS SHARED PUBLICLY")

def render_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)

def stream_response(text: str, delay: float = .065):
    placeholder = st.empty()
    full_text = ""

    for word in text.split():
        full_text += word + " "
        time.sleep(delay)
        placeholder.markdown(full_text + " ")

    placeholder.markdown(full_text)
    return full_text


uploaded_file = st.file_uploader(
    "Upload a file for your Ai knowledge base",
    type=["txt",'pdf'],
    key = "file_uploader"
)    
    

if uploaded_file is not None :
    msg3 = st.empty()
    if uploaded_file.type == "text/plain":
        file_data = uploaded_file.read().decode("utf-8")
        load_data(chunk_text(file_data))
        msg3.success("File data loaded into the database!")
        time.sleep(2)
        msg3.empty()
    elif uploaded_file.type == "application/pdf":
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for i in range(len(doc)):
                page = doc[i]
                text += page.get_text("text")
        load_data(chunk_text(text))
        msg3.success("File data loaded into the database!")
        time.sleep(2)
        msg3.empty()



if True:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    prompt = st.chat_input("What is up?")


    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        render_message("user", prompt)

        assistant_text = generate_response(prompt,st.session_state.messages)

        with st.chat_message("assistant"):
            final_response = stream_response(assistant_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": final_response}
        )
    