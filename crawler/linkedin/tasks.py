from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def login():
    driver = webdriver.Remote("http://crawler_firefox:4444/wd/hub", DesiredCapabilities.FIREFOX)
    driver.get("https://www.linkedin.com/login")
    username_elem = driver.find_element("id", "username")
    username_elem.send_keys(settings.LINKEDIN_USERNAME)
    password_elem = driver.find_element("id", "password")
    password_elem.send_keys(settings.LINKEDIN_PASSWORD)
    password_elem.submit()