from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re

category = input('Enter Category:  ')
country = input('Enter Country: ')
start = input('Enter Page: ')


chrome_driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
u_in = f'"{category}" "{country}" "gmail.com" -intitle:"profiles" -inurl:"dir/ " site:www.linkedin.com/in/ OR site:www.linkedin.com/pub/'
url = f'https://www.google.com/search?q={u_in}&start={start}'

# Use Selenium to interact with the page
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get(url)

page_source = driver.page_source
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

emails = []
for email in re.finditer(email_pattern, page_source):
    emails.append(email.group())

for i, emai in enumerate(emails):
    print(f'{i}| {emai}')




