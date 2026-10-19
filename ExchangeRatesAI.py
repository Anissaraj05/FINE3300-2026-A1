"""FINE 3300 — AI-generated USD/CAD exchange rate calculator."""

import csv
from pathlib import Path


class ExchangeRates:
    def __init__(self, filename):
        self.filename = Path(filename)
        self.rate = self._load_latest_rate()

    def _load_latest_rate(self):
        with self.filename.open('r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or 'FXAUSDCAD' not in reader.fieldnames:
                raise ValueError('The CSV file does not contain an FXAUSDCAD column.')

            latest_date = None
            latest_rate = None
            for row in reader:
                date = row.get('Date', '').strip()
                rate_text = row.get('FXAUSDCAD', '').strip()
                if not date or not rate_text:
                    continue
                try:
                    rate = float(rate_text)
                except ValueError as exc:
                    raise ValueError(f'Invalid USD/CAD rate for {date}.') from exc
                if rate <= 0:
                    raise ValueError(f'Exchange rate must be positive for {date}.')
                if latest_date is None or date > latest_date:
                    latest_date = date
                    latest_rate = rate

            if latest_rate is None:
                raise ValueError('No valid USD/CAD exchange rate was found.')
            self.date = latest_date
            return latest_rate

    def convert(self, amount, from_currency, to_currency):
        amount = float(amount)
        source = from_currency.strip().upper()
        target = to_currency.strip().upper()
        if source not in ('USD', 'CAD') or target not in ('USD', 'CAD'):
            raise ValueError('Currencies must be USD or CAD.')
        if amount < 0:
            raise ValueError('Amount cannot be negative.')
        if source == target:
            return amount
        if source == 'USD':
            return amount * self.rate
        return amount / self.rate


def main():
    try:
        csv_path = Path(__file__).with_name('BankOfCanadaExchangeRate.2026.csv')
        exchange = ExchangeRates(csv_path)
        amount = float(input('Enter amount: '))
        from_currency = input('Enter from currency (USD or CAD): ')
        to_currency = input('Enter to currency (USD or CAD): ')
        result = exchange.convert(amount, from_currency, to_currency)
        print(f'Exchange rate ({exchange.date}): 1 USD = {exchange.rate:.4f} CAD')
        print(f'{amount:,.2f} {from_currency.strip().upper()} = '
              f'{result:,.2f} {to_currency.strip().upper()}')
    except (OSError, ValueError) as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    main()
