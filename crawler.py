# encoding=utf8
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

reload(sys)
sys.setdefaultencoding('utf8')

driver = webdriver.Chrome('./chromedriver')
driver.get('https://nid.naver.com/nidlogin.login')
driver.find_element_by_name('id').send_keys('ID')
driver.find_element_by_name('pw').send_keys('PASSWORD')
# driver.find_element(By.CSS_SELECTOR, '#login_keep_wrap > div.keep_check > label').click()
driver.find_element(By.CSS_SELECTOR, '.btn_login_wrap button').click()
time.sleep(30)
cycle = 0
while True:
    for pg in range(1, 11):
        driver.get(
            "https://cafe.naver.com/nyblog?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=15424483%26search.media=0%26search.searchdate=all%26search.defaultValue=1%26search.exact=%26search.include=%26userDisplay=15%26search.exclude=%26search.option=0%26search.sortBy=date%26search.searchBy=0%26search.includeAll=%26search.query=%B7%CE%BF%A1%BA%A3%26search.viewtype=title%26search.page="
            + str(cycle * 10 + pg)
        )
        driver.switch_to.frame('cafe_main')
        articles = driver.find_elements(By.CSS_SELECTOR, "a.article")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # do sth form list of search articles
        article_list = []
        for article in articles:
            link = article.get_attribute("href")
            article_list.append(link)

        count = 0
        for link in article_list:
            driver.switch_to.new_window('tab')
            # wait.until(EC.number_of_windows_to_be(current_num_of_window+1))
            driver.get(link)
            driver.implicitly_wait(3)
            time.sleep(1)
            directory = str(10 * cycle + pg) + '-' + str(count)
            driver.switch_to.frame('cafe_main')
            html = driver.page_source
            # driver.implicitly_wait(3)
            # Title
            soup = BeautifulSoup(html, 'html.parser')
            categorySoup = soup.select_one(
                '#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > div > em')
            if categorySoup is not None:
                categorySoup = categorySoup.text
            else:
                categorySoup = ''
            titleSoup = soup.select_one(
                '#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3')
            if titleSoup is None:
                count += 1
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                continue
            else:
                titleSoup = titleSoup.text
            os.mkdir(directory)
            writeSoup = soup.select_one('a.comment_nickname')
            if writeSoup is not None:
                writeSoup = writeSoup.text
            else:
                writeSoup = ''
            tierSoup = soup.select_one(
                '#app > div > div > div.ArticleContentBox > div.article_header > div.WriterInfo > div > div.profile_info > em')
            if tierSoup is not None:
                tierSoup = tierSoup.text
            else:
                tierSoup = ''
            f = open(directory + '/info.html', 'w')
            f.write(categorySoup + '\n' + titleSoup + '\n' + writeSoup + '\n' + tierSoup)
            f.close()
            # Content
            contentSoup = soup.select('div.se-component.se-text span')
            textList = []
            for p in contentSoup:
                textList.append(p.text)
            f = open(directory + '/content.html', 'w')
            f.write(' '.join(textList))
            f.close()
            # Comment
            commentAuthorSoup = soup.select('div.comment_nick_box comment_nick_info a.comment_nickname')
            commentContentSoup = soup.select('div.comment_text_box > p > span')
            if commentAuthorSoup is not None and commentContentSoup is not None:
                textList = []
                for k in range(0, len(commentAuthorSoup)):
                    textList.append(commentAuthorSoup[k].text + '/' + commentContentSoup[k].text)
                f = open(directory + '/comment.html', 'w')
                f.write('\n'.join(textList))
                f.close()

            count += 1
            # time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

    try:
        driver.switch_to.frame('cafe_main')
        driver.find_element(By.CSS_SELECTOR, '#main-area > div.prev-next > a.pgR').click()
        cycle += 1

    except:
        break
print('done ' + str(cycle))
