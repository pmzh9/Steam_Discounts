from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

# Current Day
now = datetime.now()
day_month_year = now.strftime("%d.%m.%Y")  # DDMMYYYY

# html parser
url = "https://store.steampowered.com/search/?specials=1"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

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
    titles.append(element.span.text)
    discounts.append(element.find("div", class_="col search_discount responsive_secondrow").text)
    normal_prices.append(element.find("strike").text)
    discounted_prices.append(element.find("div", class_="col search_price discounted responsive_secondrow").contents[3])
    links.append(element.get("href"))

# structure of excel file
my_dict = {"title": titles,
           "discount": discounts,
           "normal_price": normal_prices,
           "discounted_price": discounted_prices,
           "link": links}

# creating the Excel file
df_discounts = pd.DataFrame(my_dict)
file_name = f"Steam-Discounts_{day_month_year}.xlsx"
df_discounts.to_excel(file_name)
