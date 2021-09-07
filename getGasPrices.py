import requests
import csv
import re
import calendar

from bs4 import BeautifulSoup
from calendar import monthrange
from datetime import date as today
from flask import jsonify


class GetHenryHubGasPrices:

    def __init__(self): 
        # Data stores & sources 
        self.dailyGasPricesPage = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"
        self.output_rows = []
        self.output_rows_dates = []  
        self.yearsForSingleDateCollection = []  

    def getHenryHubGasPrices(self):
        # Get the websites html
        r     = requests.get(self.dailyGasPricesPage,  verify=False)
        soup  = BeautifulSoup(r.text, 'html.parser')

        # Get the table which has the daily gas prices data
        table = soup.find("th", class_="G2").parent.parent

        def is_not_an_empty_row(css_class):
            return css_class == 'B6' or css_class == 'B3' 

        # Take the data rows and temporarily store them
        for table_row in table.findAll('tr'):
            columns = table_row.findAll(class_=is_not_an_empty_row)
            output_row = []
            for column in columns:
            # if len(column) != 0:
                if len(str(column.text)) == 0:
                    output_row.append('0')
                else:
                    output_row.append( str(column.text) )
            # Take away empty arrays
            if len(output_row) != 0:
                self.output_rows_dates.append(output_row[0])
                del output_row[0]
                self.output_rows.append(output_row)



    """**PREPARE & TRANSFORM THE DAILY DATES AND PRICES**"""

    def seperateDateIntoDates(self):

        self.getHenryHubGasPrices()

        # Take the array of dates
        # For each of the dates 
        # Get the month and get the range between the Months if their the same
        # Else, get the range of dynamic values between the diffrent months
        # Now we have a collection of range from the single date
        # We add it to the datesForSingleDateCollection

        # Create single dates out of the dates collection
        datesForSingleDateCollection = []

        # Go over each of the rows and store the data
        for date in self.output_rows_dates:    

            # Store the year of the two months and delete it
            year = str(date[1:6]).strip()
            self.yearsForSingleDateCollection.append(year)

            # Find the first and last month in the date
            firstMonthAndDayOfYear = date[6:14].strip()
            lastMonthAndDayOfYear  = date[-6:].strip()

            # Find the first and last dates in the month ranges
            firstDateOfTheMonth = firstMonthAndDayOfYear[-2:].strip()
            lastDateOfTheMonth  = lastMonthAndDayOfYear[-2:].strip()

            # Strip away the months and dates
            firstMonthOfTheYear = firstMonthAndDayOfYear[0:3].strip() # Jan,Mar,..
            lastMonthOfYear  = lastMonthAndDayOfYear[0:3].strip()

            # Get the range between the two first and last month
            datesOfTheMonthCollection = list(range(int(firstDateOfTheMonth),int(lastDateOfTheMonth)+1))

            # If the collection is 0, it means the range of dates are in diffrent months
            if len(datesOfTheMonthCollection) == 0:

                datesOfDiffirentMonthCollection = []

                # Get the range left between the day of the first month to it's ending
                currentYear     = int(today.today().year)
                firstMonthIndex = list(calendar.month_abbr).index(firstMonthOfTheYear)
                lastMonthIndex  = list(calendar.month_abbr).index(lastMonthOfYear)

                firstMonthWeekday, firstMonthRange = monthrange(currentYear, firstMonthIndex)
                lastMonthWeekday, lastMonthRange   = monthrange(currentYear, lastMonthIndex)
            
                for el in list(range(int(firstDateOfTheMonth), int(firstMonthRange)+1)): 
                        datesOfDiffirentMonthCollection.append(  str(el)+'-'+firstMonthOfTheYear  )

                for el in list(range(1, int(lastDateOfTheMonth)+1)): 
                        datesOfDiffirentMonthCollection.append(  str(el)+'-'+lastDateOfTheMonth  )        

                datesForSingleDateCollection.append(datesOfDiffirentMonthCollection)
                
            else:
                datesOfSameMonthCollection = []
                for el in datesOfTheMonthCollection: 
                    datesOfSameMonthCollection.append( str(el)+'-'+firstMonthOfTheYear )        

                datesForSingleDateCollection.append(datesOfSameMonthCollection)

        return datesForSingleDateCollection



    """**NORMALIZE THE DATA AND CREATE A CSV**"""

    def finalizeDataForWrite(self):

        datesCollection = self.seperateDateIntoDates()
        
        # Stores two columns of data and price
        datesAndPriceCollectionOutPutRows = []

        # Create a date and price collection
        for i in range(len(datesCollection)):
            for j in range(5):
                final = [datesCollection[i][j] + '-' +self.yearsForSingleDateCollection[i], self.output_rows[i][j]]
                datesAndPriceCollectionOutPutRows.append(final)

        # Write the dates and prices to a csv
        with open('static/henry_hub_natural_gas_daily_prices.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Price'])
            writer.writerows(datesAndPriceCollectionOutPutRows)

        return datesAndPriceCollectionOutPutRows


    def getMeHenryHubGasPrices(self):
        data = jsonify(response= self.finalizeDataForWrite() )
        print('Sucessfully got a response data')
        return data

