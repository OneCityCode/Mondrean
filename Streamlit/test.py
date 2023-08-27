import streamlit as st
# import pandas as pd
# import numpy as np
from PIL import Image
# # import base64


# with open("./Images/Title.png", "rb") as f:
#     data = f.read()
#     encoded = base64.b64encode(data)
# data = "data:image/png;base64," + encoded.decode("utf-8")

Image.open("./Images/Title.png")

st.image("./Images/Title.png")

