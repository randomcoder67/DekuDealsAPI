#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import json
import re
import datetime

# Function to convert a string to camel case (camelCaseIsLikeThis)
# Source: https://stackoverflow.com/questions/60978672/python-string-to-camelcase (minTwin's answer)
def camelCase(s):
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])

# Function to remove everything other than the value from price (i.e. £, $, € etc)
# Source: https://stackoverflow.com/questions/27128253/remove-currency-symbols-and-literals-from-a-string-with-a-price-universal-soluti (tiago's answer)
def noSymbolPrice(s):
    trim = re.compile(r'[^\d.,]+')
    return trim.sub("", s)

def ItemDetails(url):
    # Initialise dictionary
    itemDetails = {"msrp": None, "released": None, "genre": None, "numberOfPlayers": None, "developer": None, "publisher": None, "downloadSize": None, "metacritic": None, "opencritic": None, "howLongToBeat": None, "ageRating": None, "playModes": None, "languages": None, "platforms": None}

    # Get and parse html
    response = requests.get(url)
    htmlText = response.text
    soup = BeautifulSoup(htmlText, "html.parser")

    # Get the price history section
    priceHistory = soup.find_all("div", {"id": "price-history"})

    # Get details about all time lows, and parse into itemDetails
    allTimeLowDetails = priceHistory[0].findChildren("table")[0].findAll("td")
    if len(allTimeLowDetails) == 3: # For digital only games (technically there are some physical only, like Demon Throttle, so this isn't a great solution)
        itemDetails.update({
            "digitalPrice": float(noSymbolPrice(allTimeLowDetails[1].text.strip())),
            "digitalDiscount": allTimeLowDetails[2].text.strip().strip("(").strip(")")
        })
    else: # For digital and physical games
        itemDetails.update({
            "physicalPrice": float(noSymbolPrice(allTimeLowDetails[3].text.strip())),
            "physicalDiscount": allTimeLowDetails[4].text.strip().strip("(").strip(")"),
            "digitalPrice": float(noSymbolPrice(allTimeLowDetails[5].text.strip())),
            "digitalDiscount": allTimeLowDetails[6].text.strip().strip("(").strip(")")
        })

    # Parse the price history graph data
    graphData = soup.select_one('script[id="price_history_data"]')
    itemDetails.update({"graphData": graphData.text})


    # Parse the game details
    detailsData = soup.find_all("ul", {"class": "details list-group list-group-flush"})
    #print(detailsData[0].prettify())
    #print(len(detailsData))

    for li in detailsData[0].find_all("li", {"class": "list-group-item"}):
        detailType = camelCase(li.find_all("strong")[0].text.strip().replace(":", ""))
        
        # Add msrp
        if detailType == "msrp":
            itemDetails[detailType] = float(noSymbolPrice(li.contents[1]))
        
        # Add release dates in different regions (NA, EU and JP) in format yyyymmdd for easy manipulation
        elif detailType == "released":
            regions = li.find_all("li")
            releaseDates = {}
            # If len(regions) == 0, then all regions the same
            if len(regions) == 0:
                releaseDateyyyymmdd = datetime.datetime.strptime(li.contents[1].strip(), "%B %d, %Y").strftime("%Y%m%d")
                releaseDates = {"NA": releaseDateyyyymmdd, "EU": releaseDateyyyymmdd, "JP": releaseDateyyyymmdd}
            # Otherwise add correct dates to regions
            else:
                for region in regions:
                    releaseDate = datetime.datetime.strptime(region.contents[1].text.strip(), "%B %d, %Y").strftime("%Y%m%d")
                    for split in region.contents[0].text.split("/"):
                        releaseDates.update({split.strip(":"): releaseDate})
            itemDetails[detailType] = releaseDates
        
        # Add genres as an array
        elif detailType == "genre":
            itemDetails[detailType] = li.text[7:].split(", ")
            # ADD GENRE URLS
        
        # Add number of players relative to type of gameplay
        elif detailType == "numberOfPlayers":
            numPlayers = {}
            for entry in li.find_all("li"):
                numPlayers.update({entry.contents[0].text.strip(":"): entry.contents[1].replace(" ", "")})
            itemDetails[detailType] = numPlayers
        
        # Add developer and publisher name
        elif detailType == "developer" or detailType == "publisher":
            itemDetails[detailType] = li.contents[2].text
            # ADD URLs
        
        # Add download size in MB
        elif detailType == "downloadSize":
            if "MB" in li.contents[1]:
                itemDetails[detailType] = int(li.contents[1].strip().replace(" MB", ""))
            else:
                itemDetails[detailType] = int(float(li.contents[1].strip().replace(" GB", ""))*1000)
        
        # Add metacritic url, critic score and user score
        elif detailType == "metacritic":
            criticScore = None if li.contents[2].contents[0].text == "tbd" else int(li.contents[2].contents[0].text)
            userScore = None if li.contents[2].contents[2].text == "tbd" else float(li.contents[2].contents[2].text)
            itemDetails[detailType] = {"url": li.contents[2]["href"], "criticScore": criticScore, "userScore": userScore}
        
        # Add opencritic url and score
        elif detailType == "opencritic":
            itemDetails[detailType] = {"url": li.contents[2]["href"], "score": int(li.contents[2].contents[1])}
        
        # Add How Long To Beat times
        elif detailType == "howLongToBeat":
            howLongToBeat = {"url": li.contents[0].contents[0]["href"]}
            for entry in li.find_all("li"):
                howLongToBeat.update({entry.contents[0].text.strip(":"): entry.contents[1].strip()})
            itemDetails[detailType] = howLongToBeat
        
        # Add age rating (type and rating) (rating as string for consistency, even if PEGI)
        elif detailType == "pegiRating" or detailType == "esrbRating":
            itemDetails["ageRating"] = {"type": li.contents[0].text.replace(" Rating:", ""), "rating": li.contents[1].strip()}
        
        # Add play modes and languages as arrays
        elif detailType == "playModes" or detailType == "languages":
            itemDetails[detailType] = li.contents[1].strip().split(", ")
        
        # Add playforms as array
        elif detailType == "platforms":
            if len(li.contents) == 3: # If multiple platforms, requires slightly different parsing
                itemDetails[detailType] = li.contents[2].text.strip().split(", ")
            else:
                itemDetails[detailType] = [li.contents[1].strip()]
    
    return itemDetails
