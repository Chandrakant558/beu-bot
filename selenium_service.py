import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def create_driver():
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Try common chrome paths (Render / Linux)
    possible_paths = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            chrome_options.binary_location = path
            break

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def open_login_and_capture_captcha():
    driver = create_driver()
    driver.get("https://beu.intelllexams.com/BeuIntellLoginPage.aspx")

    time.sleep(4)

    captcha = driver.find_element(By.ID, "imgCaptcha")
    captcha.screenshot("captcha.png")

    return driver


def perform_login(driver, reg_no, password, captcha_text):
    driver.find_element(By.ID, "txtRegNo").send_keys(reg_no)
    driver.find_element(By.ID, "txtPassword").send_keys(password)
    driver.find_element(By.ID, "txtCaptcha").send_keys(captcha_text)

    driver.find_element(By.ID, "btnLogin").click()

    time.sleep(5)

    if "Dashboard" in driver.page_source or "Logout" in driver.page_source:
        return True

    return False
