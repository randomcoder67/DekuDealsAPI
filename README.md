# DekuDealsAPI

An unofficial Python 3 API for the Nintendo Switch game price tracker website DekuDeals.com

[PyPi Link](https://pypi.org/project/DekuDealsAPI/0.1/)

WIP, so install and usage instructions may change

## Installation 

### Arch Linux (as pip no longer works on Arch)

`git clone https://github.com/randomcoder67/DekuDealsAPI.git` into the directory of your project

### Distros where pip still works

`pip install DekuDealsAPI`

## Usage

### Searching

``` python3
import DekuDealsAPI as ddAPI

results = ddAPI.PerformSearch("lego star wars")
```

`PerformSearch` returns a dictionary with two keys, `searchTerm` and `results`  
`searchTerm` is simply the string you passed to the function  
`results` is a list of dictionaries, the keys of which are:

`title` - Game Title  
`link` - Link to game page  
`price` - Normal price  
`discountPrice` - Discounted price (`None` if no discount currently)  
`discountPercent` - Discount percentage (`None` if no discount currently)  
`discountInfo` - Discount information (`None` is no discount currently, or if discount is not either "Lowest price ever" or "Matches previous low")  
`currentPrice` - Current price, either `price` if no discount, or `discountPrice` if there is a discount

### Getting Specific Game Details

``` python3
import DekuDealsAPI as ddAPI

itemDetails = ddAPI.ItemDetails("https://www.dekudeals.com/items/terraria")
```

`ItemDetails` returns a dictionary with the following keys (value will be `None` if not present):

`msrp` - MSRP as a float  
`released` - A dictionary of the release dates in NA, EU and JP, date expressed in yyyymmdd format (`%Y%m%d`)  
`genre` - A list of genres  
`numberOfPlayers` - A dictionary of number of players per play type (e.g. Offline, Online)  
`developer` - Developer name  
`publisher` - Publisher name  
`downloadSize` - Download size in MB as an int  
`metacritic` - Dictionary of Metacritic URL, critic-score (int) and user-score (float)  
`opencritic` - Dictionary of Opencritic URL and score (int)  
`howLongToBeat` - Dictionary of How Long to Beat URL and completion-type -> hours  
`ageRating` - Age rating type (e.g. PEGI, ESRB, CERO) and rating as a string  
`playModes` - List of play modes (e.g. TV, Tabletop, Handheld)  
`languages` - List of supported languages  
`platforms` - List of platforms  
`physicalLowestPrice` - Physical lowest ever price, if applicable  
`physicalGreatestDiscount` - Physical greatest ever discount, if applicable  
`digitalLowestPrice` - Digital lowest ever price  
`digitalGreatestDiscount` - Digital greatest ever discount  
`graphData` - JSON formatted price history data
