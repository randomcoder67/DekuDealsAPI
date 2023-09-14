#!/usr/bin/env python

import json
import search
import page

a = search.PerformSearch("lego star wars")
b = page.ItemDetails("https://www.dekudeals.com/items/my-time-at-portia")

#print(a["results"])

final = json.dumps(a, indent=2)

print(final)

final2 = json.dumps(b, indent=2)
print(final2)
