import time
import pickle
import traceback

from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def login():
    driver = webdriver.Remote("http://crawler_firefox:4444/wd/hub", DesiredCapabilities.FIREFOX)
    driver.get("https://www.linkedin.com/login")
    username_elem = driver.find_element("id", "username")
    username_elem.send_keys(settings.LINKEDIN_USERNAME)
    password_elem = driver.find_element("id", "password")
    password_elem.send_keys(settings.LINKEDIN_PASSWORD)
    password_elem.submit()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "global-nav-search"))
    )
    pickle.dump(driver.get_cookies(), open("/app/crawler/cookies.pkl", "wb"))
    driver.quit()

def scroll(driver, counter):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_counter = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        scroll_counter += 1
        if new_height == last_height or scroll_counter > counter:
            break
        last_height = new_height

def get_linkedin_feed():
    driver = webdriver.Remote(
        "http://crawler_firefox:4444/wd/hub",
        DesiredCapabilities.FIREFOX,
    )
    cookies = pickle.load(open("/app/crawler/cookies.pkl", "rb"))
    driver.get("https://www.linkedin.com/")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.linkedin.com/feed/")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "global-nav-search"))
    )
    sort = driver.find_element("xpath", "//button[@class='display-flex full-width artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view']")
    if "recent" not in sort.text:
        print('sort on recent')
        sort.click()
        time.sleep(5)
        sort_by_recent = driver.find_element("xpath","//button[@class='display-flex full-width artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view']/following-sibling::div")
        sort_by_recent = sort_by_recent.find_elements("tag name", "li")[1]
        sort_by_recent.click()
        time.sleep(5)
    scroll(driver, 5)
    time.sleep(20)
    articles = driver.find_elements(
        By.XPATH,
        './/div[starts-with(@data-id, "urn:li:activity:")]',
    )
    for article in articles:
        driver.execute_script("arguments[0].scrollIntoView();", article)
        time.sleep(5)
        id = article.get_attribute("data-id")
        body = article.find_element(
            By.CLASS_NAME, "feed-shared-update-v2__commentary"
        ).text
        link = f"https://www.linkedin.com/feed/update/{id}/"
        body = body.replace("#", "-")
        body = body.replace("&", "-")
        message = f"{body}\n\n{link}"
        print(message)
    driver.quit()