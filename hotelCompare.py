def getCompareHotelReport(mtrHotel, rlHotel):
    mtrVillasList = mtrHotel['villasData']
    rlVillasList = rlHotel['villasData']

    reportString = ''

    for mtrVilla in mtrVillasList:

        reportString += '\t\tvilla: ' + mtrVilla['villaTitle'] + '\n'

        for rlVilla in rlVillasList:
            if mtrVilla['RLvillaID'] == rlVilla['villaID']:
                for mtrMeal in mtrVilla['meals']:

                    reportString += '\t\t\t\tmeal: ' + mtrMeal['mealName']

                    for rlMeal in rlVilla['meals']:
                        if mtrMeal['mealName'] == rlMeal['mealName']:
                            if float(mtrMeal['mealPrice']) == float(rlMeal['mealPrice']):
                                reportString += ' - OK\n'
                            else:
                                reportString += '\n\t\t\t\t\t\t' + \
                                                'Price mismatch:' + \
                                                '\n\t\t\t\t\t\t\t\t' + \
                                                'MTR price: ' + str(mtrMeal['mealPrice']) + \
                                                '\n\t\t\t\t\t\t\t\t' + \
                                                'ResortLife price: ' + str(rlMeal['mealPrice']) + '\n'
                            break
                break

    return reportString
