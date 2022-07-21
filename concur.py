#!/usr/bin/python3
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import time
from pathlib import Path
from datetime import datetime
import argparse
import sys
import os

counter = 1
patience = 1
mydate = datetime.now()
chrome_driver_dir = "/usr/local/bin/"
chrome_driver_location = chrome_driver_dir + "/chromedriver"
profile_location = "/home/daoneill/.config/google-chrome-beta/Profile 1"
url = "https://auth.redhat.com/auth/realms/EmployeeIDP/protocol/saml/clients/concursolutions"

def step(step_str):
    global counter, patience
    print(str(counter) + ": " + step_str)
    counter += 1
    time.sleep(patience)

parser = argparse.ArgumentParser(description='Submit $40 expense claim')
parser.add_argument('--bill_date', dest='bill_date', help='The bill date')
parser.add_argument('--receipt', dest='receipt', help='The receipt filename to attach')
parser.add_argument('--vendor', dest='vendor', help='The vendor')
parser.add_argument('--location', dest='location', help='The location')
args = parser.parse_args()

if args.bill_date is None or args.receipt is None:
    print("Expected: python3 concur.py --bill_date 07/12/2022 --receipt july.pdf")
    sys.exit(1)

options = Options()
options.add_argument("--user-data-dir=" + profile_location)
options.binary_location = "/opt/google/chrome-beta/chrome"
# options.add_argument('--headless')
service = Service(chrome_driver_location)
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
wait = WebDriverWait(driver, 30)

password = Path('../otpanswer/key').read_text()
token = subprocess.check_output("./getpw", cwd="../otpanswer", shell=True).decode("utf-8") 

step("Enter username")
username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
username_field.send_keys('daoneill')

step("Enter password")
username_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
username_field.send_keys(password + token)

step("Create expense")
start_claim_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"quicktasks-menu\"]/ul/li[1]/a/div/div")))
start_claim_element.click()

step("Enter claim name")
report_name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
report_name_field.send_keys('Remote Work Expense ' + mydate.strftime("%B"))

step("Create claim")
report_submit_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"cnqrBody\"]/div[8]/div/div/div[3]/div/div/button[2]")))
report_submit_button.click()

step("Add expense")
add_expense_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-nuiexp='add-btn']")))
add_expense_button.click()

step("Choose expense type")
remote_worker_expense = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Remote Worker Expense')]")))
remote_worker_expense.click()

step("Enter the date")
bill_transaction_date = wait.until(EC.presence_of_element_located((By.ID, "transactionDate")))
bill_transaction_date.send_keys(args.bill_date)

step("Enter the vendor")
bill_vendor = wait.until(EC.presence_of_element_located((By.ID, "vendorDescription")))
bill_vendor.send_keys("Virgin Media" if args.vendor is None else args.vendor)

step("Enter the location")
location_vendor = wait.until(EC.presence_of_element_located((By.ID, "locName")))
location_vendor.send_keys("Cork, IRELAND" if args.location is None else args.location)

step("Choose the location from drop down")
select_country = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"13928\"]")))
select_country.click()

step("Select currency drop down")
expense_curency = wait.until(EC.presence_of_element_located((By.ID, "transactionCurrencyName-combobox-arrow")))
expense_curency.click()

step("Choose USD")
expense_select_usd = wait.until(EC.presence_of_element_located((By.ID, "transactionCurrencyName-group-filtered-options-listbox-option-USD")))
expense_select_usd.click()

step("Enter the transaction amount")
forty_dollars_expense = wait.until(EC.presence_of_element_located((By.ID, "transactionAmount")))
forty_dollars_expense.send_keys("40")

step("Click attach receipt")
attach_receipt = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-nuiexp='attach-receipt-modal-button']")))
attach_receipt.click()

step("Set upload receipt file location")
set_receipt_location = wait.until(EC.presence_of_element_located((By.ID, "upload-receipt")))
set_receipt_location.send_keys(os.getcwd() + "/" + args.receipt)

step("Click itemisations tab")
itemise = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Itemisations')]")))
itemise.click()

step("Click create itemisation")
itemise = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-enablenow-id='create-itemization-button']")))
itemise.click()

step("click itemisation drop down")
itemization_type = wait.until(EC.presence_of_element_located((By.ID, "expName-combobox-arrow")))
itemization_type.click()

step("Choose remote worker expense")
expense_type_rme = wait.until(EC.presence_of_element_located((By.ID, "expName-group-mru-listbox-option-01123")))
expense_type_rme.click()

step("Enter the transaction amount for the itemisation")
transactionAmount = wait.until(EC.presence_of_element_located((By.ID, "transactionAmount")))
transactionAmount.send_keys("40")

step("Click save itemisation")
save_itemisation = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-nuiexp='itm-save-itemization']")))
save_itemisation.click()

step("Click save report")
save = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-nuiexp='exp-save-expense']")))
save.click()

step("Submit the report")
submit = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-nuiexp='reportActionButtons.submitButton']")))
submit.click()

step("Confirm 1")
submit1 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-nuiexp='accept-and-create-button']")))
submit1.click()

step("Confirm 2")
submit2 = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div/div[3]/button[2]")))
submit2.click()

step("Close")
submit2 = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div/div[3]/button")))
submit2.click()

step("We're all done, waiting for 30 seconds")

wait.until(EC.presence_of_element_located((By.ID, "block-xxxxxxxxxxxxxxxx")))

driver.close()


