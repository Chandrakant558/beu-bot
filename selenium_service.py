import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def open_login_and_capture_captcha():
    driver = create_driver()
    driver.get("https://beu.intelllexams.com/BeuIntellLoginPage.aspx")

    time.sleep(3)

    captcha = driver.find_element(By.ID, "imgCaptcha")
    captcha.screenshot("captcha.png")

    return driver


def perform_login(driver, reg_no, password, captcha_text):
    driver.find_element(By.ID, "txtRegNo").send_keys(reg_no)
    driver.find_element(By.ID, "txtPassword").send_keys(password)
    driver.find_element(By.ID, "txtCaptcha").send_keys(captcha_text)

    driver.find_element(By.ID, "btnLogin").click()

    time.sleep(5)

    if "Dashboard" in driver.page_source:
        return True
    return False
