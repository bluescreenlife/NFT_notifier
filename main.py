from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import smtplib
from dotenv import load_dotenv
import os

# scraper settings
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
URL = input("Enter the Blur URL for the NFT you want to track: ")
driver.get(URL)

for_sale = False
minutes = int(input("How often should the program check for changes (minutes)? "))
check_frequency = minutes * 60

# email settings
load_dotenv()

SENDER = os.getenv("SENDER")
RECIPIENT = os.getenv("RECIPIENT")
SENDER_PW = os.getenv("SENDER_PW")
SENDER_SERVER = os.getenv("SENDER_SERVER")
SENDER_PORT = os.getenv("SENDER_PORT")

def get_price():
    '''Returns NFT price or - if not listed.'''
    time.sleep(10)
    price = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div").text
    print(f"Testing: price: {price}")
    if price == "-":
        for_sale = False
    elif get_price != "-":
        for_sale = True
    return price

def send_email(message, from_addr=SENDER, to_addr=RECIPIENT):
    '''Sends notification email with price alert.'''
    with smtplib.SMTP(SENDER_SERVER, port=SENDER_PORT) as connection:
        connection.starttls()
        connection.login(user=SENDER, password=SENDER_PW)
        connection.sendmail(
            from_addr=SENDER, 
            to_addrs=RECIPIENT, 
            msg=message
        )

# main loop
# listing notification loop
if for_sale == False:
        message = f"Subject: NFT Activity Subscription Notification\n\nYou will be noified of sales for the item lited at:\n{URL}"
        send_email(message, SENDER, RECIPIENT)
        while True:
            price = get_price()
            if for_sale == False:
                pass
            elif for_sale == True:
                message = f"Subject: NFT Listing Notification\n\nAn item you're monitoring has been listed for {price} ETH.\nLink: {URL}"
                send_email(message, SENDER, RECIPIENT)
                print("Listing notification sent.")
                break
            time.sleep(check_frequency)

# sale notification loop
if for_sale == True:
    message = f"Subject: NFT Activity Subscription Notification\n\nYou will be noified of listings for the item lited at:\n{URL}"
    send_email(message, SENDER, RECIPIENT) 
    while True:
            price = get_price()
            if for_sale == True:
                pass
            elif for_sale == False:
                message = f"Subject: NFT Sale Notification\n\nAn item you're monitoring has been sold for {price} ETH.\nLink: {URL}"
                send_email(message, SENDER, RECIPIENT)
                print("Sale notification sent.")
                break
            time.sleep(check_frequency)