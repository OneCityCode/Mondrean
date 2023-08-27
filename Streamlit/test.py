import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="centered", page_title="Mondrean", page_icon="🖌️")

with st.container():
    st.image("https://raw.githubusercontent.com/OneCityCode/Test/main/Streamlit/Title.png")

    st.text_input("Enter the name of the product you would like to learn about", key="productname")

    st.session_state.productname




