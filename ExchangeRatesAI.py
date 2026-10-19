"""
ExchangeRatesAI.py
FINE 3300 - Assignment 1, Part 2 (Vibe Coding)

AI-generated USD/CAD exchange rate calculator. It reads the Bank of Canada
exchange rate file, finds the most recent USD/CAD rate, and converts amounts
between Canadian dollars (CAD) and US dollars (USD).
"""

import csv                  # Built-in library for reading CSV files
from pathlib import Path    # Makes file paths work on any operating system


class ExchangeRates:
    """Reads a Bank of Canada CSV file and converts between USD and CAD."""

    def __init__(self, filename):
        """Store the file path and load the latest USD/CAD rate from it."""
        self.filename = Path(filename)
        self.rate = self._load_latest_rate()  # 1 USD = self.rate CAD

    def _load_latest_rate(self):
        """Return the most recent USD/CAD rate (FXAUSDCAD) found in the file.

        Also saves the date of that rate in self.date.
        Raises ValueError if the column is missing or no valid rate exists.
        """
        # 'utf-8-sig' safely handles files saved with a hidden BOM character
        with self.filename.open('r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)  # Each row becomes a dictionary

            # Make sure the file has headers and includes the USD/CAD column
            if not reader.fieldnames or 'FXAUSDCAD' not in reader.fieldnames:
                raise ValueError('The CSV file does not contain an FXAUSDCAD column.')

            # Find the date column name, ignoring upper/lower case ("Date" or "date")
            date_column = None
            for name in reader.fieldnames:
                if name.strip().lower() == 'date':
                    date_column = name
                    break
            if date_column is None:
                raise ValueError('The CSV file does not contain a date column.')

            latest_date = None
            latest_rate = None

            # Go through every row and keep the rate with the newest date
            for row in reader:
                date = (row.get(date_column) or '').strip()
                rate_text = (row.get('FXAUSDCAD') or '').strip()

                # Skip rows that are blank or missing a date or rate
                if not date or not rate_text:
                    continue

                # Convert the rate from text to a number
                try:
                    rate = float(rate_text)
                except ValueError as exc:
                    raise ValueError(f'Invalid USD/CAD rate for {date}.') from exc

                # An exchange rate must be greater than zero
                if rate <= 0:
                    raise ValueError(f'Exchange rate must be positive for {date}.')

                # Dates are written YYYY-MM-DD, so comparing them as text works
                if latest_date is None or date > latest_date:
                    latest_date = date
                    latest_rate = rate

        # If no row had a usable rate, stop with a clear error
        if latest_rate is None:
            raise ValueError('No valid USD/CAD exchange rate was found.')

        self.date = latest_date
        return latest_rate

    def convert(self, amount, from_currency, to_currency):
        """Convert amount from from_currency to to_currency (USD or CAD).

        Returns the converted amount as a float.
        Raises ValueError for an unsupported currency or negative amount.
        """
        amount = float(amount)

        # Clean up the currency text so "usd " and "USD" are treated the same
        source = from_currency.strip().upper()
        target = to_currency.strip().upper()

        # Only USD and CAD are supported
        if source not in ('USD', 'CAD') or target not in ('USD', 'CAD'):
            raise ValueError('Currencies must be USD or CAD.')
        if amount < 0:
            raise ValueError('Amount cannot be negative.')

        # Same currency on both sides: no conversion needed
        if source == target:
            return amount

        # USD -> CAD: multiply by the rate (1 USD = rate CAD)
        if source == 'USD':
            return amount * self.rate

        # CAD -> USD: divide by the rate
        return amount / self.rate


def main():
    """Ask the user for an amount and two currencies, then print the result."""
    try:
        # Look for the CSV file in the same folder as this script
        csv_path = Path(__file__).with_name('BankOfCanadaExchangeRate.2026.csv')
        exchange = ExchangeRates(csv_path)

        # Collect the user's inputs
        amount = float(input('Enter amount: '))
        from_currency = input('Convert from (USD or CAD): ').strip().upper()
        to_currency = input('Convert to (USD or CAD): ').strip().upper()

        # Do the conversion
        result = exchange.convert(amount, from_currency, to_currency)

        # Show the rate used, then the result rounded to the nearest penny
        print(f'Exchange rate ({exchange.date}): 1 USD = ${exchange.rate:.4f} CAD')
        print(f'${amount:,.2f} {from_currency} = ${result:,.2f} {to_currency}')

    # Show a friendly message instead of a crash if something goes wrong
    except (OSError, ValueError) as error:
        print(f'Error: {error}')


# Run main() only when this file is run directly (not when imported)
if __name__ == '__main__':
    main()
    

