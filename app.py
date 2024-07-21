# Importing Required Libraries
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure genai API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a function to load gemini-1.5-flash model
model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(question):
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response, chat

# Setup Streamlit app
st.set_page_config(page_title="🤖 Gemini Pro API 🧠")
st.title("🤖 Conversational Q&A Chatbot Using Gemini Pro API 🧠")

# Initialize Session state for Chat History if it does not Exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Sidebar for Chat History
st.sidebar.header("Chat History")
for i, chat in enumerate(st.session_state.chat_history):
    st.sidebar.write(f"**Query {i+1}**: {chat.get('you')}")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the Question...")

if submit and input:
    response, chat = get_gemini_response(input)
    st.session_state.chat_history.append({"you": input})
    
    # Initialize an empty string to collect response chunks
    response_text = ""

    # Handle streaming response
    try:
        for chunk in response:
            # Ensure chunk is of valid type and has 'text' attribute
            if hasattr(chunk, 'text'):
                response_text += chunk.text
            else:
                st.write("Received an unexpected response type.")
        
        # Display the complete response
        st.subheader("Response: ")
        st.write(response_text, unsafe_allow_html=True)
        
        # Append the response to chat history
        st.session_state.chat_history[-1]["Bot"] = response_text
    except Exception as e:
        st.write(f"An error occurred: {e}")
