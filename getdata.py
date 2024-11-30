import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver
from bs4 import BeautifulSoup

import random

def extract_papers():
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    papers = []

    # Find all rows in the search result table
    rows = soup.select('table.result-table-list tbody tr')

    for row in rows:
        title_tag = row.select_one('td.name a')  # Paper title
        authors_tag = row.select_one('td.author')  # Authors
        journal_tag = row.select_one('td.source a')  # Journal name

        # Extract the information if available
        if title_tag and authors_tag and journal_tag:
            title = title_tag.get_text(strip=True)
            authors = ', '.join([author.get_text(strip=True) for author in authors_tag.find_all('a')])
            journal = journal_tag.get_text(strip=True)
            papers.append((title, authors, journal))

    return papers

if __name__ == '__main__':
    # 设置Selenium WebDriver，打开淘宝商品搜索页
    # 启动 Chrome 浏览器
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")  # 最大化窗口
    driver = webdriver.Chrome(options=options)

    url = 'https://libyc.nudt.edu.cn/view-login'  # 示例搜索页面URL
    driver.get(url)

    # 等待页面加载完成
    time.sleep(3)

    # 等待并定位到账户输入框
    account_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, "account"))
    )
    account_input.send_keys("YOUR USERNAME")

    # 等待并定位到密码输入框
    password_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys("YOUR PASSWORD")

    # 登录
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
    )
    login_button.click()

    # solve_slide_captcha(driver)

    # 点击搜索
    cnki_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'CNKI中国知网')]"))
    )
    # 输入账户信息
    cnki_button.click()

    # 等待搜索框出现
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    driver.refresh()

    try:
        search_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-input"))
        )
        # 输入账户信息
        search_input.send_keys("人工智能")
    except Exception as e:
        # 等待搜索框出现
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        driver.refresh()

    # 点击搜索
    search_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'search-btn'))
    )
    # 输入账户信息
    search_button.click()

    while True:
        papers = extract_papers()
        for title, authors, journal in papers:
            print(f"Title: {title}\nAuthors: {authors}\nJournal: {journal}\n")

        # Try to find the "Next" button
        try:
            next_button = driver.find_element(By.ID, "PageNext")
            next_button.click()  # Click the "Next" button
            time.sleep(5)  # Wait for the next page to load
        except Exception as e:
            print("No more pages to scrape.")
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
            driver.refresh()

        wait_time = random.uniform(3, 5)
        time.sleep(wait_time)
