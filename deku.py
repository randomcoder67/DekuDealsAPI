#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

urlA = "https://www.dekudeals.com/items/diablo-3"

response = requests.get(urlA)

htmlText = response.text
soup = BeautifulSoup(htmlText, "html.parser")

priceAndDiscount = soup.find_all("div", {"class": "btn btn-block btn-primary"})[0]
if len(priceAndDiscount.findChildren("span")) > 0:
    discount = priceAndDiscount.findChildren("span")[0].text
    print(f"Discount: {discount}")
for x in priceAndDiscount.strings:
    price = x.replace("\n", "")
    break
print(f"Price: {price}")
isLowest = soup.find_all("span", {"class": "badge badge-warning"})
if len(isLowest) > 0:
    print(f"Message: {isLowest[0].text}")
    
urlB = "https://www.dekudeals.com/search?q=star+wars"

response = requests.get(urlB)

htmlText = response.text
soup = BeautifulSoup(htmlText, "html.parser")

links = soup.find_all("a", {"class": "main-link"})

for link in links:
    href = link["href"]
    title = link.findChildren("div", {"class": "h6 name"})[0].text.replace("\n", "")
    price = link.next_sibling
    print(f"Title: {title}")
    if price.text == "\n":
        price = price.next_sibling
        if price["class"] == ["text-muted"]:
            print(f"Price: {price.text}")
        else:
            discountInfo = price.text.strip().split("\n")
            if len(discountInfo) == 3:
                print(f"Original Price: {discountInfo[0]}, Discounted Price: {discountInfo[1]}, Discount: {discountInfo[2]}")
            elif len(discountInfo) == 4:
                print(f"Original Price: {discountInfo[0]}, Discounted Price: {discountInfo[1]}, Discount: {discountInfo[2]} ({discountInfo[3]})")
    else:
        price = price.replace("\n", "")
        print(f"Price: {price}")
