from getMTRHotels import getMtrPrices
from getRLhotels import getRLprices
from hotelCompare import getCompareHotelReport

dateslist = [
    ['1', '01/03/2023', '02/03/2023', '1', '0']
]

for selectedDate in dateslist:

    startDate = selectedDate[1]
    endDate = selectedDate[2]
    guestAdult = selectedDate[3]
    guestChildren = selectedDate[4]
    childAgeList = []

    OUTPUT_LOG_PATH = f"./logs/price-log-{guestAdult}-adults-{guestChildren}-children-{startDate.replace('/', '-')}-{endDate.replace('/', '-')}.txt "

    MTRHotelList = getMtrPrices(startDate, endDate, guestAdult, guestChildren, childAgeList)
    RLHotelsList = getRLprices(f'docs/rlHTML/{selectedDate[0]}.html')

    print('Starting prices compare...\n')

    hotelsCounter = 1

    for mtrHotel in MTRHotelList:
        for rlHotel in RLHotelsList:
            if mtrHotel['hotelRLID'] == rlHotel['hotelRLID']:
                hotelReport = getCompareHotelReport(mtrHotel, rlHotel)
                with open(OUTPUT_LOG_PATH, "a", encoding="utf-8") as file:
                    file.write(str(hotelsCounter) + '. ' + mtrHotel["hotelName"] + '\n')
                    file.write(hotelReport)
                hotelsCounter = hotelsCounter + 1
                break
