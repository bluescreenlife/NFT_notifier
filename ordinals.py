from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import smtplib
from dotenv import load_dotenv
import os

class OrdinalSaleNotifier:
    def __init__(self):
        self.listed_urls = [input("Enter the URL of a live Magic Eden listing to begin: ")]
        self.sold_urls = []

        load_dotenv()

        self.SENDER = os.getenv("SENDER")
        self.SENDER_PW = os.getenv("SENDER_PW")
        self.RECIPIENT = input("Enter your email address for sale notifications: ")

    def webdriver_init(self):
        service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def add_url (self):
        new_url = input("Enter an additional Magic Eden ordinal URL: ")
        self.listed_urls.append(new_url)

    def check_listings(self):
        driver = self.webdriver_init()
        for url in self.listed_urls:
            driver.get(url)
            sleep(5)
            try:
                element = driver.find_element(By.XPATH, "//*[@id='content']/div/div[1]/div[2]/div[3]/h3[1]")
                if element:
                    pass
            except NoSuchElementException:
                self.sold_urls.append(url)
        
        driver.close()

        if self.sold_urls:
            return True
        else:
            return False

    def send_email(self):
        if self.sold_urls:
            message = "Subject: Ordinal(s) Sale Notification\n\nThe following ordinal(s) have sold:\n"

            for url in self.sold_urls:
                message = message + f"{url}\n"
            
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=self.SENDER, password=self.SENDER_PW)
                connection.sendmail(
                    from_addr=self.SENDER, 
                    to_addrs=self.RECIPIENT, 
                    msg=message
                )
        
            self.sold_urls = []

        else:
            pass

if __name__ == "__main__":
    notifier = OrdinalSaleNotifier()

    while True:
        sleep(10)
        check = notifier.check_listings()
        if check:
            notifier.send_email()