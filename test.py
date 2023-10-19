#!/usr/bin/env python

import json
import DekuDealsAPI as ddAPI

# Basic example of using API and printing results

legoStarWarsSearch = ddAPI.PerformSearch("lego star wars")
superMarioOdyssey = ddAPI.ItemDetails("https://www.dekudeals.com/items/super-mario-odyssey")
superMarioOdyssey.pop("graphData") # I know the graphData bit is there bit it's huge so printing is annoying

# Printing nicely formatted
print(json.dumps(legoStarWarsSearch, indent=2))
print(json.dumps(superMarioOdyssey, indent=2))

# Printing keys
print(legoStarWarsSearch.keys())
print(legoStarWarsSearch["results"][0].keys())
print(superMarioOdyssey.keys())

# Plotting price history data with matplotlib

import matplotlib.pyplot as plt

terraria = ddAPI.ItemDetails("https://www.dekudeals.com/items/terraria")
graphDataJSON = json.loads(terraria["graphData"])
graphDates = []
graphValues = []

for entry in graphDataJSON["data"]:
    graphDates.append(entry[0])
    graphValues.append(entry[1:])

plt.plot(graphDates, graphValues)
plt.show()

