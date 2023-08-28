import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup

st.set_page_config(layout="centered", page_title="Mondrean", page_icon="🖌️")

with st.container():
  st.image("https://raw.githubusercontent.com/OneCityCode/Test/main/Streamlit/Title.png")
  pn = st.text_input("", max_chars=25, placeholder="Enter the name of a specific product here, and press enter.")

  if len(pn) > 0:
    with st.status("Locating relevent information", expanded=True):
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
      res = 0
      commentsout = []
  
      for post in posts[:12]:
          post_url = "https://www.reddit.com" + post.find_all('a')[2]['href']
          urls.append(post_url)

      st.write("Gathering and processing data")

      for url in urls:
        if res < 2000:
          driver.get(url)
          soup_post = BeautifulSoup(driver.page_source, 'html.parser')
          for comment in soup_post.find_all('div', {'class': 'md'})[1:]:           
            if res < 2000:
              res += len(comment.text)
              commentsout.append(comment.text)
            
      st.write("Complete!", state="complete")

      driver.quit()

    st.write(commentsout)
    st.write(str(res))


