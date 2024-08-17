from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://coinmarketcap.com/'

response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

table = soup.find('table', class_='sc-7b3ac367-3 etbcea cmc-table')

cryptos = []
for row in table.tbody.find_all('tr'):
    try:
        name = row.find('p',class_='sc-71024e3e-0 ehyBa-d').text
        price = row.find('div',class_='sc-b3fc6b7-0 dzgUIj').text.replace("$","").replace(",","")
        market_cap = row.find('span', class_='sc-11478e5d-0 chpohi').text.replace('$','').replace(',','')

        if market_cap.endswith('T'):
            market_cap = float(market_cap[:-1]) * 1e12
        elif market_cap.endswith('B'):
            market_cap = float(market_cap[:-1]) * 1e9
        else:
            market_cap = float(market_cap)

        cryptos.append([name, float(price), float(market_cap)])

    except AttributeError:
        continue

crypto_df = pd.DataFrame(cryptos,columns=['Name', 'Price', 'Market Cap'])

print(crypto_df)

crypto_df = crypto_df.sort_values(by='Market Cap', ascending=False)
plt.figure(figsize=(12, 8))
plt.bar(crypto_df['Name'], crypto_df['Market Cap'], color='blue')
plt.xlabel('Cryptocurrency')
plt.ylabel('Market Cap ($)')
plt.title('Top Cryptocurrencies by Market Cap')
plt.xticks(rotation=90)
plt.show()