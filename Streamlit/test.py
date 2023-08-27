import streamlit as st
# import pandas as pd
# import numpy as np
from PIL import Image
# import base64


# with open("Title.png", "rb") as f:
#     data = f.read()
#     encoded = base64.b64encode(data)
# data = "data:image/png;base64," + encoded.decode("utf-8")

Image.open("Title.png")

st.image("Title.png")

