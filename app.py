import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from chat import chat
# st.set_page_config(
    
#     layout="wide",
    
# )
page = st.sidebar.selectbox("Explore Or Predict", ("Explore", "Predict","Chat"))

if page == "Predict":
    show_predict_page()
if page == "Chat":
    chat()
if page=="Explore":
    show_explore_page()
