
# Background Image

from streamlit_card import card
card(
    title="Hello World!",
    text="Some description",
    image="http://placekitten.com/300/250",
    url="https://www.google.com",
)

# Page Title

st.title('Minute ON Demand REview ANalasys')

# Query Entry:

import streamlit as st
st.text_input("Enter the name of the product you would like to learn about", key="productname")

st.session_state.productname

# Submit button

st.button

# Enter not needed if using button

from st_keyup import st_keyup
st.write("## Notice how the output updates with every key you press")
out2 = st_keyup("Keyup input")
st.write(out2)

# Sidebar Links:

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

# Progress status:

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

# Progress Bar:

import time
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

# Vertical stack in container

with st.container():
   st.write("This is inside the container")
   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))
st.write("This is outside the container")

# Side by Side columns:

import numpy as np
import pandas as pd
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')
# or call Streamlit functions inside a "with" block:
with right_column:
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

# Or

from streamlit_extras.grid import grid
random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
my_grid = grid(2, [2, 4, 1], 1, 4, vertical_align="bottom")
# Row 1:
my_grid.dataframe(random_df, use_container_width=True)
my_grid.line_chart(random_df, use_container_width=True)
# Row 2:
my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
my_grid.text_input("Your name")
my_grid.button("Send", use_container_width=True)
# Row 3:
my_grid.text_area("Your message", height=40)
# Row 4:
my_grid.button("Example 1", use_container_width=True)
my_grid.button("Example 2", use_container_width=True)
my_grid.button("Example 3", use_container_width=True)
my_grid.button("Example 4", use_container_width=True)
# Row 5 (uses the spec from row 1):
with my_grid.expander("Show Filters", expanded=True):
    st.slider("Filter by Age", 0, 100, 50)
    st.slider("Filter by Height", 0.0, 2.0, 1.0)
    st.slider("Filter by Weight", 0.0, 100.0, 50.0)
my_grid.dataframe(random_df, use_container_width=True)

# Bar Chart

st.bar_chart
# or
from streamlit_extras.altex import bar_chart, get_weather_data
weather = get_weather_data()
bar_chart(
    data=weather.head(15),
    x="temp_max:Q",
    y=alt.Y("date:O", title="Temperature"),
    title="A beautiful horizontal bar chart",

# Text summary (streaming)

from streamlit_extras.streaming_write import write
def stream_example():
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.1)
    # Also supports any other object supported by `st.write`
    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.05)
if st.button("Stream data"):
    write(stream_example)

# Hyperlink

st.write("check out this [link](https://google.com)")

# Or

from markdownlit import mdlit
mdlit(
    """Tired from [default links](https://extras.streamlit.app)?
Me too! Discover Markdownlit's `@()` operator. Just insert a link and it
will figure a nice icon and label for you!
Example: @(https://extras.streamlit.app)... better, right? You can
also @(🍐)(manually set the label if you want)(https://extras.streamlit.app)
btw, and play with a [red]beautiful[/red] [blue]set[/blue] [orange]of[/orange]
[violet]colors[/violet]. Another perk is those beautiful arrows -> <-
"""
)

# Or

from streamlit_extras.stylable_container import stylable_container
with stylable_container(
    key="green_button",
    css_styles="""
        button {
            background-color: green;
            color: white;
            border-radius: 20px;
        }
        """,
):
    st.button("Green button")
st.button("Normal button")
with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """,
):
    st.markdown("This is a container with a border.")

# Link to similar products

from streamlit_extras.switch_page_button import switch_page
want_to_contribute = st.button("I want to contribute!")
if want_to_contribute:
    switch_page("Contribute")

