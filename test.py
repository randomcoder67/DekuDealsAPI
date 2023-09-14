#!/usr/bin/env python

import json
import DekuDealsAPI as ddAPI

a = ddAPI.PerformSearch("lego star wars")
b = ddAPI.ItemDetails("https://www.dekudeals.com/items/super-mario-odyssey")
b.pop("graphData") # I know the graphData bit is there bit it's huge so printing is annoying

#print(a["results"])

final = json.dumps(a, indent=2)

#print(final)

final2 = json.dumps(b, indent=2)
print(final2)

#print(a["results"][0].keys())
#print(b.keys())
