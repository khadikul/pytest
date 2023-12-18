import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re


class EmailScraper:
    def __init__(self, country, category):
        self.country = country
        self.category = category
        self.emails = []

    def build_url(self, start):
        u_in = f'"{self.category}" "{self.country}" "gmail.com" -intitle:"profiles" -inurl:"dir/ " site:www.linkedin.com/in/ OR site:www.linkedin.com/pub/'
        url = f'https://www.google.com/search?q={u_in}&start={start}'
        return url

    def scrape_emails(self):
        start = 0
        chrome_driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
        use_headless = True  # Initial setting for headless mode

        while True:
            url = self.build_url(start)

            # Use Selenium to interact with the page
            chrome_options = Options()
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                                        'KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

            if use_headless:
                use_headless = True
                chrome_options.add_argument('--headless')  # Run Chrome in headless mode
                chrome_options.add_argument("--use_subprocess")

            print('Email Extracting.....')
            time.sleep(5)
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            driver.get(url)
            html = driver.page_source

            # Check for CAPTCHA presence
            if 'captcha' in html:
                print('CAPTCHA Detected! Switching to non-headless mode...')
                use_headless = False
                time.sleep(30)
                driver.quit()
                continue

            # Define a regular expression pattern for matching emails
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

            for email in re.finditer(email_pattern, html):
                self.emails.append(email.group())

            # If no emails are found on the page, break the loop
            if not self.emails:
                use_headless = False
                print('Something With Wrong')
                print('Email Extract End')
                time.sleep(20)
                break

            # Increment the start parameter for the next page
            start += 10

            # Close the driver
            driver.quit()

    def print_emails(self):
        # Print the valid emails
        for i, email in enumerate(self.emails):
            print(f'{i} {email}')


if __name__ == "__main__":
    # User input
    country_input = input('Enter Country: ')
    category_input = input('Enter Category: ')

    # Create an instance of EmailScraper
    email_scraper = EmailScraper(country=country_input, category=category_input)

    # Scrape emails
    email_scraper.scrape_emails()

    # Print valid emails
    email_scraper.print_emails()
