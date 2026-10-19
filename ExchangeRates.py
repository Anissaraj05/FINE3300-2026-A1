'''
ExchangeRates.py
Anissa Raj- Assignment 1

Exchange Rate Calculator: ExchangeRates class definition and implementation
'''

import csv

class ExchangeRates:
    def __init__(self, filename):
        # Read the exchange rate file
        file = open(filename, "r")
        reader = csv.reader(file)

        rows = []
        for row in reader:
            if len(row) > 0:
                rows.append(row)
        file.close()

        # Find the column that holds the USD/CAD exchange rate
        header = rows[0]
        column = 0
        while header[column] != "FXAUSDCAD":
            column += 1

        # Find the USD/CAD exchange rate in the last row
        last_row = rows[-1]
        self.__usd_cad = float(last_row[column])

    def convert(self, amount, from_currency, to_currency):
        # Use the exchange rate to convert the amount
        if from_currency == "USD" and to_currency == "CAD":
            result = amount * self.__usd_cad
        elif from_currency == "CAD" and to_currency == "USD":
            result = amount / self.__usd_cad
        elif from_currency == to_currency and from_currency in ("USD", "CAD"):
            result = amount
        else:
            result = None

        return result


if __name__ == "__main__":
    # Create an ExchangeRates object
    rates = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")

    # Prompt the user for the amount and currencies
    amount = float(input("Enter amount: "))
    from_currency = input("Convert from (USD or CAD): ")
    to_currency = input("Convert to (USD or CAD): ")

    # Call the convert method
    result = rates.convert(amount, from_currency, to_currency)

    # Print the result
    if result is None:
        print("Invalid currency! Please enter USD or CAD.")
    else:
         print("${:,.2f} {} = ${:,.2f} {}".format(amount, from_currency, result, to_currency))

