#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# coding=utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup 
import time
s = Service('/Users/lemon/Downloads/chromedriver_win32/chromedriver')

driver = webdriver.Chrome(service=s)
driver.get('https://nid.naver.com/nidlogin.login')
## 아이디/비밀번호를 입력해준다.
driver.find_element_by_name('id').send_keys('ID')
driver.find_element_by_name('pw').send_keys('PASSWORD')
driver.find_element(By.CSS_SELECTOR, '#login_keep_wrap > div.keep_check > label').click()
driver.find_element(By.CSS_SELECTOR, '.btn_login_wrap button').click()
cycle = 0
time.sleep(17)
while True:
    for pg in range(1, 11):
        driver.get("https://cafe.naver.com/nyblog?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=15424483%26search.media=0%26search.searchdate=all%26search.defaultValue=1%26search.exact=%26search.include=%26userDisplay=15%26search.exclude=%26search.option=0%26search.sortBy=date%26search.searchBy=0%26search.includeAll=%26search.query=%B7%CE%BF%A1%BA%A3%26search.viewtype=title%26search.page="+str(cycle*10 + pg))
        driver.switch_to.frame('cafe_main')
        articles = driver.find_elements(By.CSS_SELECTOR, "a.article")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # do sth form list of search articles
        original_window = driver.current_window_handle
        article_list = []
        for article in articles:
            link = article.get_attribute("href")
            print(link)
            article_list.append (link)
            
        print(article_list)
            
        for link in article_list:
            driver.switch_to.new_window('tab')
            #wait.until(EC.number_of_windows_to_be(current_num_of_window+1))
            driver.get(link)
        driver.switch_to.window(original_window)

    try: 
        driver.find_element(By.CSS_SELECTOR, 'a.pgR').click()
        cycle += 1
        
    except :
        break
print('done '+str(cycle))

