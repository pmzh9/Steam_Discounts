from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from datetime import datetime
import time

driver = webdriver.Chrome()
# Current Day
now = datetime.now()
day_month_year = now.strftime("%d.%m.%Y")  # DDMMYYYY

# html parser
url = "https://store.steampowered.com/search/?specials=1"
driver.get(url)

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# elements with relevant information
elements = soup.find_all("a", class_="search_result_row ds_collapse_flag")

# lists to store columns
titles = []
discounts = []
normal_prices = []
discounted_prices = []
links = []

# appending elements to the lists
for element in elements:
    if element.find("span", style="color: #888888;") is not None and element.find("div", class_="col search_price discounted responsive_secondrow").contents[3] is not None:
        normal_prices.append(element.find("span", style="color: #888888;").text)
        discounted_prices.append(element.find("div", class_="col search_price discounted responsive_secondrow").contents[3])
        titles.append(element.find("span", class_="title").text)
        discounts.append(element.find("div", class_="col search_discount responsive_secondrow").text)
        links.append(element.get("href"))
    else:
        continue

# structure of excel file
my_dict = {"title": titles,
           "discount": discounts,
           "normal_price": normal_prices,
           "discounted_price": discounted_prices,
           "link": links}
print()
print(len(titles), len(discounts), len(normal_prices), len(discounted_prices), len(links))
# creating the Excel file
df_discounts = pd.DataFrame(my_dict)
file_name = f"Steam-Discounts_{day_month_year}.xlsx"
df_discounts.to_excel(file_name)

driver.quit()
