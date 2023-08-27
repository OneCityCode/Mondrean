import streamlit as st
import pandas as pd
import numpy as np
from streamlit_card import card
from PIL import Image


Image.open('./Images/Cardm.jpeg')

# st.image.show(image)

card(
    title="Minute ON Demand REview ANalysis",
    text="Some description",
    image='./Images/Cardm.jpeg',
    url="https://www.google.com",
)