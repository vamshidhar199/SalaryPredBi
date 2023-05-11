import streamlit as st
import pickle
import numpy as np
from autoMl import automl_pipeline
import pandas as pd
from api import call_openai_api

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Prediction")

    st.write("""### """)


    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    expericence = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, expericence ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
        # Add a button to trigger the auto ML pipeline
    
        
    st.title("Upload a csv")
    
    # Add a file uploader to allow users to upload a new CSV file
    uploaded_file = st.file_uploader("Upload a new CSV file")
    
    # If a file is uploaded, update the CSV file
    if uploaded_file is not None:
        df_new = pd.read_csv(uploaded_file)
        df_existing = pd.read_csv("survey_results_public_2022.csv")
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
        df_updated.to_csv("salary_data.csv", index=False)
        st.success("CSV file updated successfully")
    if st.button("Run Auto ML Pipeline"):
        automl_pipeline()
    
    # st.title("Chat App")

    # # Create an input box for user to enter messages
    # user_input = st.text_area("Enter your message here:")

    # # Display the conversation history
    # st.subheader("Conversation History")
    # st.text("Hello!")
    # st.text("Hi there!")
    # st.text("How can I assist you?")

    # # Handle user input
    # if st.button("Send"):
    #     # Add the user's message to the conversation history
    #     st.text(f"You: {user_input}")
        
    #     # Send the user's message to the chatbot API and get the response
    #     # Replace this with your API call code
        
    #     response = call_openai_api(user_input)
        
    #     # Add the chatbot's response to the conversation history
    #     st.text(f"Chatbot: {response}")