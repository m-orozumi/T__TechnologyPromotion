import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if __name__ == '__main__':
    filename = './zeal_search_result.csv'
    titles = []
    urls = []

    # Selenium Gridサーバーへ接続する。
    driver = webdriver.Remote(
        command_executor=os.environ["SELENIUM_URL"],
        desired_capabilities=DesiredCapabilities.CHROME.copy()
    )

    # 1. 検索キーワード入力
    keyword = input("Search Keyword：")

    # 2. Googleにアクセス+入力キーワードで検索
    driver.get("https://zdh.stagingbridge.net/")
    driver.find_element(By.NAME, "q").send_keys(keyword + Keys.RETURN)
    # 検索結果描画待機
    wait = WebDriverWait(driver, 10)
    wait.until(
        presence_of_element_located((By.XPATH, '//a/h3')))

    # 3. タイトルとURLを抽出
    for elem_h3 in driver.find_elements_by_xpath('//a/h3'):
        title = elem_h3.text
        url = elem_h3.find_element_by_xpath('..').get_attribute('href')
        print("Title:"+title+" | "+"URL:"+url)
        titles.append(title)
        urls.append(url)

    # 4. csv出力
    result = [list(row) for row in zip(titles, urls)]
    with open(filename, mode="w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(result)
    driver.quit()