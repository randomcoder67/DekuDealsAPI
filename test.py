#!/usr/bin/env python

import json
import search

a = search.PerformSearch("lego star wars")

#print(a["results"])

final = json.dumps(a, indent=2)

print(final)
