from bs4 import BeautifulSoup


def getRLprices(URL):
    with open(URL, 'r', encoding="utf8") as f:
        print('Getting RL prices...')
        print('RL html opened. Waiting for parse...')
        soup = BeautifulSoup(f.read(), 'html.parser')
        print('Big RL html parse done.')
        hotelsDivsList = soup.find_all('div', {'class': 'samo-hotel'})
        print(str(len(hotelsDivsList)) + ' RL hotels found')
        hotelsList = []

        for hotel in hotelsDivsList:
            hotelName = hotel.get('data-samo-hotel-name')
            hotelID = hotel.get('data-samo-hotel')
            print('RL hotel: ' + hotelName + ' id: ' + hotelID)
            hotelOfferHTMLDivs = hotel.find_all('div', {'class': 'hotel-price'})

            hotelOffersList = []

            for hotelDiv in hotelOfferHTMLDivs:
                villaName = hotelDiv.find('span', {'class': 'type-room'}).find('b').text.strip()
                villaID = hotelDiv.find('input', {'class': 'samo-radio-room'}).get('data-samo-room')
                offerMeal = hotelDiv.find('span', {'class': 'type-room'}).find('b').findNext('b').text.strip()
                offerPrice = hotelDiv.find('input', {'class': 'samo-radio-room'}).get('data-samo-price')[:-4]

                hotelOffersList.append({'villaName': villaName,
                                        'villaID': villaID,
                                        'offerMeal': offerMeal,
                                        'offerPrice': offerPrice})

            villasNameList = []
            for hotelOffer in hotelOffersList:
                if hotelOffer['villaName'] not in villasNameList:
                    villasNameList.append({'villaName': hotelOffer['villaName'], 'villaID': hotelOffer['villaID']})

            hotelPriceList = []
            for villa in villasNameList:
                villaPriceList = {'villaTitle': villa['villaName'], 'villaID': villa['villaID'], 'meals': []}

                for hotelOffer in hotelOffersList:
                    if villa['villaName'] == hotelOffer['villaName']:
                        villaPriceList['meals'] \
                            .append({'mealName': hotelOffer['offerMeal'], 'mealPrice': hotelOffer['offerPrice']})

                hotelPriceList.append(villaPriceList)

            hotelsList.append({'hotelName': hotelName,
                               'hotelRLID': hotelID,
                               'villasData': hotelPriceList})

        print('Successfully received RL hotels prices!')
        return hotelsList
