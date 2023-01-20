from threading import Thread
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def getMtrPrices(startDate, endDate, adults, children, childAgeList):
    print('Getting MTR prices...')

    hotelsURLList = getMTRHotelsURLList(startDate, endDate, adults, children, childAgeList)

    hotelsList = []

    hotelsMTRIDList = []
    with open('docs/MTR_Hotels_IDs.csv') as f:
        lines = f.readlines()
        for line in lines:
            hotelsMTRIDList.append(line.split(';'))

    hotelsRLIDList = []
    with open('docs/hotels_IDs_mapping.csv') as f:
        lines = f.readlines()
        for line in lines:
            hotelsRLIDList.append(line.split(';'))

    for hotel in hotelsURLList:

        hotelID = 0
        for hotelIDLine in hotelsMTRIDList:
            if hotel['hotelName'].strip() == hotelIDLine[1].strip():
                hotelID = hotelIDLine[0]

        hotelRL_ID = 0
        for hotelRLID in hotelsRLIDList:
            if hotelID == hotelRLID[0]:
                if isinstance(hotelRLID[1], int):
                    hotelRL_ID = hotelRLID[1]
                elif isinstance(hotelRLID[1], str):
                    hotelRL_ID = hotelRLID[1].replace('\n', '')

        villasData = getMTRHotelVillasData(hotel['hotelURL'])
        hotelPriceData = {'hotelName': hotel['hotelName'],
                          'hotelLocalID': hotelID,
                          'hotelRLID': hotelRL_ID,
                          'villasData': villasData}

        hotelsList.append(hotelPriceData)
        print('hotel done: ' + hotel['hotelName'])

    print('Successfully received MTR hotels prices!')
    return hotelsList


def getMTRHotelVillasData(MTRHotelURL):
    priceList = []
    villasList = BeautifulSoup(urlopen(Request(MTRHotelURL, headers={"User-Agent": "Mozilla/5.0"})), "html.parser") \
        .find_all('div', {'class': 'villa-wrap'})

    for villa in villasList:
        villaTitle = villa.find('a', {'class': 'villa-title'}).text.strip()
        villaID = villa.get('data-id')
        if villaID == '':
            continue

        villaMealTypes = villa.find_all('div', {'class': 'villa-meal-item'})
        villaMealsList = []

        for mealType in villaMealTypes:
            mealName = mealType.find('input', {'class': 'meal-radio-input'}).get('value')
            mealPrice = mealType.find('input', {'class': 'meal-radio-input'}).get('data-price')
            villaMealsList.append({'mealName': mealName, 'mealPrice': mealPrice})

        MTR_RL_Mapping_List = []
        with open('docs/MTR_RL_Villas_Mapping.csv') as f:
            lines = f.readlines()
            for line in lines:
                MTR_RL_Mapping_List.append(line.split(';'))

        RLvillaID = 0
        for MTR_RL_Mapping_Line in MTR_RL_Mapping_List:
            if MTR_RL_Mapping_Line[0] == villaID:
                RLvillaID = MTR_RL_Mapping_Line[1].replace('\n', '')

        villaData = {'villaTitle': villaTitle,
                     'villaID': villaID,
                     'RLvillaID': RLvillaID,
                     'meals': villaMealsList}

        priceList.append(villaData)

    return priceList


def getMTRHotelsURLList(startDate, endDate, adults, children, childAgeList):
    print('Recieving hotels URLs for dates: ' + startDate + ' - ' + endDate)

    MTRSearchResultURL = f"https://maldivestop.uk/maldives_resorts/?start={startDate.split('/')[0]}%2F{startDate.split('/')[1]}%2F{startDate.split('/')[2]}&end={endDate.split('/')[0]}%2F{endDate.split('/')[1]}%2F{endDate.split('/')[2]}&room_num_search=1&adult_number={str(adults)}&child_number={str(children)}"

    if int(children) > 0:
        for childAge in childAgeList:
            MTRSearchResultURL = MTRSearchResultURL + '&childrens-age%5B%5D=' + str(childAge)
        print(MTRSearchResultURL)

    MTRHotelsList = []

    request_site = Request(MTRSearchResultURL, headers={"User-Agent": "Mozilla/5.0"})
    MTRNumberOfPages = BeautifulSoup(urlopen(request_site), "html.parser") \
        .find("ul", {'class': "page-numbers"}).find_all("li")[-1].text

    for pageNumber in range(1, int(MTRNumberOfPages) + 1):
        pageURL = MTRSearchResultURL + "&num_page=" + str(pageNumber)
        pageRequest = Request(pageURL, headers={"User-Agent": "Mozilla/5.0"})
        hotelOnPageList = BeautifulSoup(urlopen(pageRequest), "html.parser").find_all("div", {"class": "item-hotel"})
        hotelsOnPageCount = 0
        for hotel in hotelOnPageList:
            hotelName = hotel.find("h4", {"class": "service-title"}) \
                .find("a") \
                .text \
                .strip()

            hotelURL = hotel.find("div", {"class": "section-price"}) \
                .find("a") \
                .get("href")

            MTRHotelsList.append({'hotelName': hotelName,
                                  "hotelURL": hotelURL,
                                  "hotelID": 0})

            hotelsOnPageCount = hotelsOnPageCount + 1

        print(f"Page number {pageNumber}. Hotels on page: {hotelsOnPageCount}")
    print('mtr hotel URLs recieved')
    return MTRHotelsList
