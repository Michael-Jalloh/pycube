import requests

def get_coins():
    try:
        coins = ["bitcoin","ethereum","litecoin"]
        coin_data = []
        for c in coins:
            coin = requests.get(f"https://api.coingecko.com/api/v3/coins/{c}").json()
            coin_data.append(coin)
        return coin_data
    except Exception as e:
        print(e)
        return []