from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
prefs = {
  "translate_whitelists": {"zh-CN":"en"},
  "translate":{"enabled":"true"}
}

options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=options)
url = "https://www.zhihu.com/question/400305423/answer/1273297051"
browser.get(url)
browser.switch_to.window(browser.current_window_handle)

time.sleep(5)

y = 1000
for timer in range(0,10):
    browser.execute_script("window.scrollTo(0, "+str(y)+")")
    y += 1000  
    time.sleep(1)

browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

html = browser.page_source
soup = BeautifulSoup(html)
contents = soup.findAll("div", {"class": "RichContent-inner"})

with open("output.html", "w") as fp:
    fp.write(str(contents[0]))
