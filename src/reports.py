import requests
import json


def get_500_company_tickers() -> list:
    api_url = 'https://api.api-ninjas.com/v1/sp500'
    response = requests.get(api_url, headers={'X-Api-Key': 'iI019ChSxoTeg94zTqiChw==QhpFM6wBFh70ftUg'})
    if response.status_code == 200:
        data = response.json()
        return [item["ticker"] for item in data]
    else:
        print("Ошибка получения тикеров:", response.status_code, response.text)
        return []


def get_500_companies_price(tickers):
    responses = []
    for ticker in tickers:
    # ticker = 'FOX'
        api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(ticker)
        response = requests.get(api_url, headers={'X-Api-Key': 'iI019ChSxoTeg94zTqiChw==QhpFM6wBFh70ftUg'})
        if response.status_code == requests.codes.ok:
            print(response.text)
            return responses.append(response.text)
        else:
            print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    # print(get_500_company_tickers())
    print(get_500_companies_price(get_500_company_tickers()))
