# Currency Converter

from forex_python.converter import CurrencyRates

c = CurrencyRates()
amount = int(input("Enter the amount you want to convert\n"))
from_currency = input("From\n").upper()
to_currency = input("To\n").upper()

print(from_currency, "To", to_currency, amount)
result = c.convert(from_currency, to_currency, amount)
print(result)