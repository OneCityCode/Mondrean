import os
import openai
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

# Set key as env var with $ echo "export OPENAI_API_KEY='sk-xxxxxxxxxx'" >> ~/.zshrc
openai.api_key = os.environ['OPENAI_API_KEY']

# Settings for chrome to operate headless
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument('--disable-dev-shm-usage')

# Provides tab title and icon
st.set_page_config(layout="centered", page_title="Mondrean", page_icon="🖌️")

# Creates container for vertical stack of elements
with st.container():

  # Creates header image and text input box
  st.image("https://raw.githubusercontent.com/OneCityCode/Mondrean/main/Mondrean.png")
  pn = st.text_input("pn", max_chars=20, placeholder="Enter the name of a specific product here, and press enter.", label_visibility = "hidden")

  # Initiates scraping on text input
  if len(pn) > 0:
    # Creates status update bar
    with st.status("Locating relevent information", expanded=True):
      # Reformats the text input and transforms it to a scrapable url.
      my_query = pn
      query_depunc = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), my_query))
      query_despace = query_depunc.replace(' ', '+')
      url_end = query_despace.strip()                                                                              
      myurl = f'https://www.reddit.com/search/?q="{url_end}"'
      # Uses selenium to fetch site data
      driver = webdriver.Chrome(service=service, options=options)
      driver.get(myurl)
      # Uses BeautifulSoup to return site HTML
      soup = BeautifulSoup(driver.page_source, 'html.parser')
      # Filters relevent HTML content
      posts = soup.find_all('post-consume-tracker')
      # urls stores html strings containing links to subpages
      urls = []
      # keeps track of number of words that have been scraped
      res = 0
      # commentsout stores scraped data to be parsed by the LLM
      commentsout = []

      # Iterates through subpages found and reformats string to scrapable url
      for post in posts[:10]:
          post_url = "https://www.reddit.com" + post.find_all('a')[0]['href']
          urls.append(post_url)

      # Updates status bar
      st.write("Gathering and processing data")

      # Iterates though subpages
      for url in urls:
        # Loads subpage if data threshhold not met
        if res < 2500:
          # Scrapes subpage and extracts HTML
          driver.get(url)
          soup_post = BeautifulSoup(driver.page_source, 'html.parser')
          # Filters for comments text
          for comment in soup_post.find_all('div', {'class': 'md'})[1:]:
            # Formats comments, appends commentsout, and updates res, if data threshhold not met.             
            if res < 2500:
              comshort = (comment.text)
              comstrip = comshort.strip()
              comtoks = str.split(comstrip)
              res += len(comtoks)
              commentsout.append(comstrip)

      # Updates status bar      
      st.write("Parsing data with AI, just a moment~", state="complete")

      # Closes browser
      driver.quit()

    # Removes comments until data length is below threshhold
    while res > 2500:
      res -= len(str.split(commentsout[0]))
      commentsout.pop(0)

    # Parse comment data using openai api
    prompt = f"""Many of the following comments, which are delimited with \
        quotation marks, pertain to {my_query}. Provide a wholly unique summary \
        of those comments the in the style of a personal review, with a length of \
        500 words. {commentsout}"""
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}])
    
    # Return parsed information
    st.write(completion.choices[0].message.content)