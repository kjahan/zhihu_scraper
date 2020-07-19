from googlesearch import search
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from langdetect import detect

html_round_divider = '<hr style="border-top: 8px solid #bbb; border-radius: 5px;">'

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
    if "signin" in browser.current_url:
        return None

    y = 300
    for timer in range(0, 50):
        browser.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 300
        time.sleep(1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(browser.page_source)
    quesion_title = soup.findAll("h1", {"class": "QuestionHeader-title"})[0].get_text()
    answers = soup.findAll("div", {"class": "RichContent-inner"})
    tags = [topic_link_element.text for topic_link_element in soup.findAll('a', {"class": "TopicLink"})]
    return (quesion_title, answers, tags)

if __name__ == "__main__":
    import sys
    from blogger.blogObject import blog_manager
    with init_translate_chrome() as browser:
        topic = sys.argv[1]
        # might want to tranlsate topic to Chinese
        urls = [url for url in search_zhihu_topic(topic, 10) if is_url_zhihu_question(url)]
        for url in urls:
            returns = get_answers(browser, url)
            if returns:
                title, answers, tags = returns
                answers = [answer for answer in answers if len(answer.text) > 500 and detect(answer.text) == "en"][0:5]
                answers_html = [str(answer) for answer in answers]
                answers_html = html_round_divider.join(answers_html)
                if len(answers_html) > 0:
                    blog_manager.topic_map['us_problem'][0].post_content(answers_html, title, tags)
