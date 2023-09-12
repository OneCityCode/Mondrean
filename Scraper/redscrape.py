from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

my_query = ""
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

comments = []

for url in urls:
    driver.get(url)
    soup_post = BeautifulSoup(driver.page_source, 'html.parser')
    for comment in soup_post.find_all('div', {'class': 'md'}):
        comments.append(comment.text)

df = pd.DataFrame(comments)
df.to_csv('comments.csv', index=False)