import streamlit as st
import pickle
import numpy as np
from autoMl import automl_pipeline
import pandas as pd
from api import call_openai_api

def chat():
    
    st.title("Chat with gpt-3.5-turbo")

    # Create an input box for user to enter messages
    user_input = st.text_area("Enter your message here:")

    # Display the conversation history
    # st.subheader("Conversation History")
    # st.text("Hello!")
    # st.text("Hi there!")
    # st.text("How can I assist you?")

    # Handle user input
    if st.button("Send"):
        # Add the user's message to the conversation history
        st.text(f"You: {user_input}")
        
        # Send the user's message to the chatbot API and get the response
        # Replace this with your API call code
        with st.spinner("Calling the API..."):
            response = call_openai_api(user_input)
        # st.success("API response received!")
        
        # Add the chatbot's response to the conversation history
        st.text_area(label="output",value= response)