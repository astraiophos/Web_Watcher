from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import smtplib
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Set up SMTP instance
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("jacobbfull@gmail.com", "twjr ihio nnlo woqm")

browser_options = Options()
browser_options.add_argument("--headless=new")
url = "https://store.steampowered.com/sale/steamdeckrefurbished"

def start():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=browser_options)
    driver.get(url)
    return driver


def refresh(driver):
    driver.refresh()


def quit(driver):
    driver.quit()

def find_console(mytext):
    prods = mytext.split('\n')
    idx = prods.index("Steam Deck 512 GB OLED - Valve Certified Refurbished")
    return (prods[idx], prods[idx+1])

def runner(driver):
    all_btn = driver.find_elements(By.XPATH, "//*[@id='SaleSection_33131']")
    try:
        x = all_btn[0].text
    except:
        return 0
    stock = find_console(x)
    if stock[1].lower() != "out of stock":
        to="jacobbfull@gmail.com" ## Sender email address
        from_="jacobbfull@gmail.com" ## Recipient email address
        s.sendmail(
            to_addrs=to,
            from_addr=from_,
            msg="Time to buy, the console is in stock right now"
        )
        status = 1
    else:
        print(stock)
        print(datetime.now())
        status = 0
    return status


def get_my_deck():
    c= 0
    driver = start()
    time.sleep(10) ## DO NOT EDIT
    print("Started Scraper")
    while True:
        try:
            if c<11:
                status = runner(driver)
                if status == 1:
                    break
                time.sleep(20) ## HOW OFTEN TO CHECK THE WEBSITE
                c = c+1
                refresh(driver)
            else:
                print("Rebooting")
                quit(driver)
                time.sleep(20) ## DO NOT EDIT
                c = 0
                driver = start()
        except Exception as e:
            print(e)
            driver.quit()
            time.sleep(20) ## DO NOT EDIT
            get_my_deck()


get_my_deck()
