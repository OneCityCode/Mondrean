import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("window-size=1024,768")
options.add_argument("--no-sandbox")

#Provides tab title and icon
st.set_page_config(layout="centered", page_title="Mondrean", page_icon="🖌️")

#Creates container for vertical stack of elements
with st.container():

  #Creates header image and text input box
  st.image("https://raw.githubusercontent.com/OneCityCode/Mondrean/main/Mondrean.png")
  pn = st.text_input("pn", max_chars=20, placeholder="Enter the name of a specific product here, and press enter.", label_visibility = "hidden")

  #Initiates scraping on text input
  if len(pn) > 0:
    #Creates status update bar
    with st.status("Locating relevent information", expanded=True):
      #Reformats the text input and transform it to a scrapable url.
      my_query = pn
      query_depunc = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), my_query))
      query_despace = query_depunc.replace(' ', '+')
      url_end = query_despace.strip()                                                                              
      myurl = f'https://www.reddit.com/search/?q="{url_end}"'
      #Uses selenium to fetch site data
      driver = webdriver.Chrome(service=service, options=options)
      driver.get(myurl)
      #Uses BeautifulSoup to return site HTML
      soup = BeautifulSoup(driver.page_source, 'html.parser')
      #Filters relevent HTML content
      posts = soup.find_all('div', {'class': 'pb-xl'})
      #urls stores information of subpages to scrape that were found
      urls = []
      #res keeps track of total amount of useful data that has been scraped
      res = 0
      #commentsout stores the useful data that has been scraped
      commentsout = []

      #Iterates through subpages found in initial page, and reformats information to scrapable url
      for post in posts[:2]:
          post_url = "https://www.reddit.com" + post.find_all('a')[2]['href']
          urls.append(post_url)

      #Updates status bar
      st.write("Gathering and processing data")

      #Iterates though subpages
      for url in urls:
        #only loads subpage in data threshhold not met
        if res < 3000:
          #scrapes subpage and extracts HTML
          driver.get(url)
          soup_post = BeautifulSoup(driver.page_source, 'html.parser')
          #Filters for comments in HTML
          for comment in soup_post.find_all('div', {'class': 'md'})[1:]:
            #If data threshhold not met, formats comment and adds comment to list and length to tracker             
            if res < 3000:
              comshort = (comment.text)
              comstrip = comshort.strip()
              comtoks = str.split(comstrip)
              res += len(comtoks)
              commentsout.append(comstrip)

      #Updates status bar      
      st.write("Complete!", state="complete")

      #Closes browser
      driver.quit()

    #removes comments, until data length is below threshhold
    while res > 3000:
      res -= len(str.split(commentsout(0)))
      commentsout.pop(0)
    #Return comments and total length of data
    st.write(commentsout)
    st.write(str(res))


# to gpt : Many of the comments which below, which are delimited with quotation marks, pertain to *search term*.
# Provide a wholly unique summary of those comments the in the style of a review, with a length of 500 words. 
# following the summary, under the heading chart:, using data from the comments, provide only a list of the top 5 most 
# relevent attributes of *search term* formatted as one word descriptors and a rating for each attribute on a scale of 1-10.  