#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import datetime
import os
import glob

counter = 1
patience = 1
mydate = datetime.now()
chrome_driver_dir = "/usr/local/bin/"
chrome_driver_location = chrome_driver_dir + "/chromedriver"
profile_location = "/home/daoneill/.config/google-chrome-beta/Profile 1"
url = "https://www.virginmedia.ie/sign-in?conversation=https%3A%2F%2Fwww%2Evirginmedia%2Eie%2Fmyvirginmedia%2F"

def step(step_str):
    global counter, patience
    print(str(counter) + ": " + step_str)
    counter += 1
    time.sleep(patience)

options = Options()
options.add_argument("--user-data-dir=" + profile_location)
options.binary_location = "/opt/google/chrome-beta/chrome"
# options.add_argument('--headless')
service = Service(chrome_driver_location)
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
wait = WebDriverWait(driver, 30)

step("Enter username")
username_field = wait.until(EC.presence_of_element_located((By.ID, "background_fullwidth_templatesection_2_section_content_uxpcontainer_containerparsys_signin_0_username")))
username_field.send_keys(os.environ.get('virgin_username'))

step("Enter password")
username_field = wait.until(EC.presence_of_element_located((By.ID, "background_fullwidth_templatesection_2_section_content_uxpcontainer_containerparsys_signin_0_password")))
username_field.send_keys(os.environ.get('virgin_password'))

step("Click login")
login = wait.until(EC.presence_of_element_located((By.ID, "background_fullwidth_templatesection_2_section_content_uxpcontainer_containerparsys_signin_0_buttonsignin")))
login.click()

step("Wait till logged in")
wait_for_login = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Hello David')]")))

driver.get("https://www.virginmedia.ie/myvirginmedia/billsandpayments/fixed/mybills/") 

step("Wait for latest bill")
latest_bill = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Latest Bill')]")))

step("Download pdf")
download_pdf = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div[3]/div/div/div/div[5]/div/div[2]/div[4]/div/div[2]/div[2]")))
download_pdf.click()

time.sleep(2)

home = os.path.expanduser("~")
downloadspath=os.path.join(home, "Downloads")

list_of_files = glob.glob(downloadspath + "/*.pdf")
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

os.rename(latest_file , os.getcwd() + "/" + mydate.strftime("%B") + ".pdf")

driver.close()
