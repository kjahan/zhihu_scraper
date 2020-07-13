from googlesearch import search
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

# given topic, search popular questions on Zhihu
def search_zhihu_topic(topic, top = 20):
    query = topic + " site:www.zhihu.com"
    return search(query, stop= top)

def is_url_zhihu_question(url):
    return "zhihu.com/question" in url

def init_translate_chrome():
    options = Options()
    prefs = {
      "translate_whitelists": {"zh-CN":"en"},
      "translate":{"enabled":"true"}
    }
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(chrome_options=options)

def get_answers(browser, url):
    browser.get(url)
    browser.switch_to.window(browser.current_window_handle)
    time.sleep(5)

    y = 1000
    for timer in range(0, 10):
        browser.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 1000
        time.sleep(1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(browser.page_source)
    quesion_title = soup.findAll("h1", {"class": "QuestionHeader-title"})[0].get_text()
    answers = soup.findAll("div", {"class": "RichContent-inner"})
    return (quesion_title, answers)

if __name__ == "__main__":
    browser = init_translate_chrome()
    topic = "black lives matter"
    # might want to tranlsate topic to Chinese
    urls = [url for url in search_zhihu_topic(topic, 10) if is_url_zhihu_question(url)]
    for url in urls:
        title, answers = get_answers(browser, url)
        for answer in answers:
            file_name = title + "_" + str(random.randint(1,10000)) +".html"
            with open(file_name, "w") as fp:
                fp.write(str(answer))
