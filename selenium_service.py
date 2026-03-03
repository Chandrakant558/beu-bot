import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def create_driver():
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Try common Linux chrome paths (Render compatible attempt)
    possible_paths = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            chrome_options.binary_location = path
            break

    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        raise Exception("❌ Chrome not found on server. Selenium cannot start.\n" + str(e))


def open_login_and_capture_captcha():
    driver = create_driver()

    driver.get("https://beu.intelllexams.com/BeuIntellLoginPage.aspx")

    time.sleep(4)

    try:
        captcha = driver.find_element(By.ID, "imgCaptcha")
        captcha.screenshot("captcha.png")
    except Exception:
        driver.quit()
        raise Exception("❌ Captcha element not found.")

    return driver


def perform_login(driver, reg_no, password, captcha_text):
    try:
        driver.find_element(By.ID, "txtRegNo").send_keys(reg_no)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        driver.find_element(By.ID, "txtCaptcha").send_keys(captcha_text)

        driver.find_element(By.ID, "btnLogin").click()

        time.sleep(5)

        page_source = driver.page_source

        if "Dashboard" in page_source or "Logout" in page_source:
            return True

        return False

    except Exception as e:
        print("Login error:", e)
        return False
