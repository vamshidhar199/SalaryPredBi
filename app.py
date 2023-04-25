import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

st.set_page_config(
    
    layout="wide",
    
)
page = st.sidebar.selectbox("Explore Or Predict", ("Explore", "Predict"))

if page == "Predict":
    show_predict_page()
else:
    show_explore_page()