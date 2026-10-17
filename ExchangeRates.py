'''
ExchangeRates.py
Your Name

Exchange Rate Calculator: ExchangeRates class definition and implementation
'''


class ExchangeRates:
	def __init__(self, filename):
		# Read the exchange rate file
		# utf-8-sig removes the hidden character at the start of the Date column
		file = open(filename, "r", encoding="utf-8-sig")
		lines = file.readlines()
		file.close()

		# Find the column that holds the USD/CAD exchange rate
		header = lines[0].strip().replace('"', '').split(",")
		column = header.index("FXAUSDCAD")

		# Find the USD/CAD exchange rate in the last row (skip any blank lines)
		i = len(lines) - 1
		while lines[i].strip() == "":
			i -= 1
		last_row = lines[i].strip().replace('"', '').split(",")

		self.__usd_cad = float(last_row[column])

	def convert(self, amount, from_currency, to_currency):
		# Use the exchange rate to convert the amount
		from_currency = from_currency.upper()
		to_currency = to_currency.upper()

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
		print("{:.2f} {} = {:.2f} {}".format(amount, from_currency.upper(), result, to_currency.upper()))
