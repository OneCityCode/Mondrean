import streamlit as st
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup

st.set_page_config(layout="centered", page_title="Mondrean", page_icon="🖌️")

with st.container():
    st.image("https://raw.githubusercontent.com/OneCityCode/Test/main/Streamlit/Title.png")
    pn = st.text_input("", max_chars=25, placeholder="Enter the name of a specific product here, and press enter.")

commentsout = []

if len(pn) > 0:
  my_query = pn
  query_depunc = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), my_query))
  query_despace = query_depunc.replace(' ', '+')
  url_end = query_despace.strip()
  myurl = "https://www.reddit.com/search/?q=" + url_end
  driver = webdriver.Chrome()
  driver.get(myurl)
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  posts = soup.find_all('div', {'class': 'pb-xl'})
  urls = []

  for post in posts[:5]:
      post_url = "https://www.reddit.com" + post.find_all('a')[2]['href']
      urls.append(post_url)

  for url in urls:
      driver.get(url)
      soup_post = BeautifulSoup(driver.page_source, 'html.parser')
      for comment in soup_post.find_all('div', {'class': 'md'}):
          commentsout.append(comment.text)

  driver.quit()

if len(commentsout) > 0:
  st.write(commentsout)


