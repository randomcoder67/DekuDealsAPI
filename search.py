#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

#searches = []

def PerformSearch(keywords):
    searchTerm = keywords.replace(" ", "+")
    url = "https://www.dekudeals.com/search?q=" + searchTerm
    #thisSearch = {"searchTerm": keywords}
    #searches.insert(0, thisSearch)
    
    response = requests.get(url)
    htmlText = response.text
    soup = BeautifulSoup(htmlText, "html.parser")
    links = soup.find_all("a", {"class": "main-link"})
    
    results = []
    # Parse search results
    for link in links:
        individualResult = {}
        results.append(individualResult)
        # Parse and add title and link
        title = link.findChildren("div", {"class": "h6 name"})[0].text.replace("\n", "")
        individualResult.update({"title": title, "link": "https://www.dekudeals.com/" + link["href"]})
        
        # Parse and add price, discounted price and discount info
        price = link.next_sibling
        if price.text == "\n":
            price = price.next_sibling
            # If item is not on sale
            if price["class"] == ["text-muted"]:
                individualResult.update({"price": price.text, "discountPrice": None, "discountPercent": 0, "discountInfo": None})
            
            # If item is on sale
            else:
                # Get the discount info
                discountInfo = price.text.strip().split("\n")
                # Add price, discountPrice and discountPercent
                individualResult.update({"price": discountInfo[0], "discountPrice": discountInfo[1], "discountPercent": discountInfo[2]})
                
                # If length == 4, then the item is discounted with a special tag
                if len(discountInfo) == 4:
                    individualResult.update({"discountInfo": discountInfo[3]})
                else:
                    individualResult.update({"discountInfo": None})
                
        # Set only price
        else:
            price = price.replace("\n", "")
            individualResult.update({"price": price, "discountPrice": None, "discountPercent": None, "discountInfo": None})
        
        # Add currentPrice which is either the price or discountedPrice if the item is on sale
        if individualResult["discountPrice"] == None:
            individualResult.update({"currentPrice": individualResult["price"]})
        else:
            individualResult.update({"currentPrice": individualResult["discountPrice"]})

    return {"searchTerm": keywords, "results": results}

'''
PerformSearch("star wars")
PerformSearch("diablo 3")
PerformSearch("portal knights")

for search in searches:
    print("Search Term: " + search["searchTerm"])
    for result in search["results"]:
        if not result["discountPrice"] == None:
            print(f"Title: {result['title']}, Current Price: {result['currentPrice']}, Original Price: {result['price']}, {result['discountPercent']}", end="")
            if not result["discountInfo"] == None:
                print(f" ({result['discountInfo']}), {result['link']}")
            else:
                print("")
        else:
            print(f"Title: {result['title']}, Price: {result['currentPrice']}")
    print("\n\n")
'''
