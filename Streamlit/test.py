import streamlit as st
import pandas as pd
import numpy as np
from streamlit_card import card
from PIL import Image
import base64


with open("./Images/Cardm.jpeg", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
data = "data:image/png;base64," + encoded.decode("utf-8")

# Image.open('./Images/Cardm.jpeg')

# st.image.show(image)

card(
    title="Mondrean",
    text="Minute ON Demand REview ANalysis",
    image=data,
    styles={
        "card": {
            "width": "500px",
            "height": "300px",
            "border-radius": "10px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",}
        },

)