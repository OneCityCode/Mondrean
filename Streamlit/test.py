import streamlit as st
import pandas as pd
import numpy as np
# from streamlit_card import card
from PIL import Image


img = Image.open('card.jpg')

st.image(img)

# card(
#     title="Minute ON Demand REview ANalysis",
#     text="Some description",
#     image=('Card.jpg'),
#     url="https://www.google.com",
# )