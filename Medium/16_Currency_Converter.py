import requests

BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

def convert_currency(base): 
    try:
        url = BASE_URL + base
        response = requests.get(url) 
        data = response.json() 
        return data
    except Exception as e:
        print("Error fetching rates:", e)
        return None

while True:
    base = input("Convert from (currency ticker, e.g. USD, EUR): ").upper()
    if base == "Q":
        break

    data = convert_currency(base)
    if not data:
        continue
    
    dest = input("Convert to (currency ticker, e.g. USD, EUR): ").upper()
    if dest == "Q":
        break
    
    amount = float(input("Enter amount: "))
    
    rates = data.get("rates", {})
    rate = rates.get(dest, None)

    if rate is None:
        print(f"Currency {dest} not found.")
        continue

    print(f"{amount} {base} is equal to {amount * rate} {dest}")
