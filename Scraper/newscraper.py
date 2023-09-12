from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

my_query = ""
query_depunc = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), my_query))
query_despace = query_depunc.replace(' ', '+')
url_end = query_despace.strip()
myurl = "https://www.reddit.com/search/?q=" + url_end
options = Options()
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options)
driver.fullscreen_window()
driver.get(myurl)
urls = []
posts = []

post_html = driver \
    .find_elements(By.CSS_SELECTOR, ('div', {'class': 'pb-xl'}))

post_links = driver \
    .find_elements(By.CSS_SELECTOR, ('a')[2]['href'])

for post_link in post_links[:5]:
    driver.get("https://www.reddit.com" + post_link)
    comments = driver \
        .find_elements(By.CSS_SELECTOR, '[data-click-id="comments"]') 
    for comment in comments:
        posts.append(comment)

driver.quit()

df = pd.DataFrame(posts)
df.to_csv('comments.csv', index=False)