import matplotlib.pyplot as plt 
import numpy as np 
import bs4
from bs4 import BeautifulSoup
import vnstock as vns
import requests
import datetime
import pandas as pd
import math

message = """

            WELCOME TO GIA HIEU'S INVESTMENT PORTFOLIO MAKER       

"""
print(message)
directory = 'C:/Users/Admin/Desktop/stock data/revenue.txt'
df = pd.read_csv('C:/Users/Admin/Desktop/stock.csv')


def scrape_usd_to_vnd():
    global vnd
    url = "https://www.exchange-rates.org/Rate/USD/VND"
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_element = soup.find('span', {'class': 'rate-to'})
    p = price_element.text.strip()
    vnd = int(p[:2]) * 1000 + int(p[3:6])

scrape_usd_to_vnd()

def gold_price():
    url = 'https://sjc.com.vn/giavang/textContent.php'
    page = requests.get(url)
    page_data = BeautifulSoup(page.content, 'html.parser')
    number_of_holding = df['gold'][0]
    data = page_data.find_all('td',attrs={'class': 'br bb bg_bl white_text'})
    giavang_Data = data[8].text
    gia_vang = int(giavang_Data[0:2])*1000000 + int(giavang_Data[3:5])*10000
    return gia_vang*number_of_holding

def stock_price(stock_name):
    
    current_time = datetime.datetime.now()
    isDate = str(current_time.date())
    yesterday = current_time.date() - datetime.timedelta(days=1)
    yesterday_str = str(yesterday)
    day_bf_yesterday = current_time.date() - datetime.timedelta(days=2)
    day_bf_yesterday_str = str(day_bf_yesterday)
    friday_date = current_time.date() - datetime.timedelta(days=3)
    friday_date_str = str(friday_date)
    try:
        
        stock_data = vns.stock_historical_data(symbol=stock_name, start_date=isDate, end_date=isDate, resolution='1D', type = 'stock',beautify=False, decor=True, source='DNSE')
        
        return stock_data.iloc[0]
    except IndexError:
        if current_time.weekday() == 6:
            
            stock_data = vns.stock_historical_data(symbol=stock_name, start_date=day_bf_yesterday_str, end_date=day_bf_yesterday_str, resolution='1D', type = 'stock',beautify=False, decor=True, source='DNSE')
        if current_time.weekday() == 0:
            stock_data = vns.stock_historical_data(symbol=stock_name, start_date=friday_date_str, end_date=friday_date_str, resolution='1D', type = 'stock',beautify=False, decor=True, source='DNSE')
        else:
            
            stock_data = vns.stock_historical_data(symbol=stock_name, start_date=yesterday_str, end_date=yesterday_str, resolution='1D', type = 'stock',beautify=False, decor=True, source='DNSE')
        return stock_data.iloc[0]

    
def combine_stock_price():
    global stock_price_list 
    global stock_shares 
    global price 
    global stock_name
    global stock_price_only
    global stock_name_only

    stock_name = []
    stock_price_list = []
    stock_shares = []
    price = []
    stock_name_only = []
    stock_price_only = []
    
    counter = 0
    for items in df['stock name']:
        if pd.isna(items):
            break

        else:
            sto = stock_price(items)
            stock_price_list.append(sto.iloc[3])
            stock_name.append(items)
            stock_name_only.append(items)
    for shares in df['share']:
        if pd.isna(shares):
            break
        else:
            stock_shares.append(shares)
    while counter < len(stock_price_list):
        stock_prices = stock_price_list[counter] * stock_shares[counter] * 1000
        price.append(int(stock_prices))
        stock_price_only.append(int(stock_prices))
        counter += 1
    return price

        

def get_revenue():
    global stock_price_original_list_real
    global gold_price_original_list
    stock_share_og = []
    gold_price_original_list = []
    stock_price_original_list = []
    stock_price_original_list_real = []
    counter = 0
    for gold_original in df['gold price original']:
        if pd.isna(gold_original):
            break
        else:
            gold_price_original_list.append(gold_original)
    for stock_original in df['stock price original']:
        if pd.isna(stock_original):
            break
        else:
            stock_price_original_list.append(stock_original)
    for share_og in df['share']:
        if pd.isna(share_og):
            break
        else: 
            stock_share_og.append(share_og)
    while counter < len(stock_price_original_list):
        stock_og_price = stock_price_original_list[counter] * stock_share_og[counter] * 1000
        stock_price_original_list_real.append(stock_og_price)
        counter += 1
    return gold_price_original_list, stock_price_original_list_real

def get_crypto_prices():
    counter_crypto_private = 0
    counter_crypto_private1 = 0
    global crypto_name_list
    # URL of the CoinGecko API endpoint for cryptocurrency prices
    crypto_price_list = []
    crypto_price_original_list = []
    crypto_name = df['crypto']
    crypto_name_list = []
    crypto_share = []
    original_crypto_price = df['crypto price original']
    cryto_price_list_user = []

    
    for crypto in crypto_name:
        
        if pd.isna(crypto):
            break
        # Sending a GET request to the API
        else:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=" + str(crypto) + "&vs_currencies=usd"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if request is unsuccessful
            data = response.json()  # Parsing the JSON response

        # Extracting prices
        
            crypto_price = data[str(crypto)]["usd"]
            crypto_price_list.append(crypto_price)
            crypto_name_list.append(crypto)
     
    for amount in df['crypto amount']:
        
        if pd.isna(amount):
            break
        else: 
            crypto_share.append(amount)
            crypto_price_user = amount * crypto_price_list[counter_crypto_private] 
            cryto_price_list_user.append(crypto_price_user)
            counter_crypto_private += 1
    for og_crypto_price in original_crypto_price:
        if pd.isna(og_crypto_price):
            break
        
        else:
            crpr = og_crypto_price * crypto_share[counter_crypto_private1]
            crypto_price_original_list.append(crpr)
            counter_crypto_private1 += 1
    array_1 = np.array(crypto_price_original_list) #ORIGINAL
    array_2 = np.array(cryto_price_list_user)    #CURRENT
    
    crypto_diff_percent = ((array_2 - array_1) / array_1) * 100
    crypto_diff_price = array_2 - array_1  
    return crypto_price_list, crypto_price_original_list, crypto_diff_percent, crypto_diff_price, cryto_price_list_user
        
combine_stock_price()

goldprice = gold_price()
cryptocurrency = get_crypto_prices()


color = "neutral"
revenue = get_revenue()
TOTAL_ASSET_ORIGINAL = int(sum(revenue[0]) * df['gold'][0] + sum(revenue[1])) + sum(cryptocurrency[1])*vnd



TOTAL_ASSET = int(goldprice) + sum(price) + sum(cryptocurrency[4])*vnd
for c in cryptocurrency[4]:
    price.append(c*vnd)
for b in crypto_name_list:
    stock_name.append(b)


rev = TOTAL_ASSET-TOTAL_ASSET_ORIGINAL
rev_percentage = ((TOTAL_ASSET-TOTAL_ASSET_ORIGINAL) / TOTAL_ASSET_ORIGINAL) * 100
rounded_rev = round(rev_percentage, 3)
revenue_display = str("You made: " + str(round(rev,2)) + "\n" + str(rev_percentage) + "%" )
if rev_percentage < 0:
    color = "red"
else:
    color = "green"
plt.figure(figsize=(8,6), frameon=True)
text_to_display = str("Total asset: " + str(round(TOTAL_ASSET)) + " VND" + "\n" + "Original asset: " + str(round(TOTAL_ASSET_ORIGINAL)) + " VND" + "\n" + str("You made: " + str(round(rev)) + " VND" + "\n" + str(rounded_rev) + "%" ))
if int(goldprice) != 0:
    price.append(int(goldprice))
    stock_name.append('Gold')

plt.pie(price, labels=stock_name, autopct='%1.1f%%', shadow =True)
plt.axis('equal')
plt.title('INVESTMENT' + "\n" + "================")
plt.text(1.3,1,text_to_display,color = color, fontsize = 12, ha = 'center')
plt.legend(loc='lower right', labels = stock_name)
plt.show()

array_1 = np.array(stock_price_only) #current price (stock)

array_2 = np.array(stock_price_original_list_real) #original price (stock)

og_gold_price = gold_price_original_list[0] * df['gold'][0] #original price (gold)

difference_stock = ((array_1 - array_2) / array_2) * 100
difference_stock_price = array_1 - array_2
difference_gold = ((goldprice - og_gold_price) / og_gold_price) * 100
counter = 0
counter_crypto = 0
day_update = datetime.datetime.now()
day_now = str(day_update)
with open(directory, 'w') as file:
    for diff_Stock in difference_stock:
        new_diff_Stock = diff_Stock.astype(float)
        file.write(stock_name_only[counter] + " -> " + str(round(new_diff_Stock, 3)) + " %. Profit: " + str(difference_stock_price[counter]) + " VND. Current price: " + str(array_1[counter]) + " VND\n")
        counter += 1

    for diff_crypto in cryptocurrency[2]:
        new_diff_crypto = diff_crypto.astype(float)
        file.write(crypto_name_list[counter_crypto] + " -> " + str(round(new_diff_crypto,3)) + " %. Profit: " + str(round(cryptocurrency[3][counter_crypto] * vnd)) + " VND. Current price: " + str(round(cryptocurrency[4][counter_crypto] * vnd)) + " VND\n")
        counter_crypto += 1
        


    file.write("Gold -> " + str(round(difference_gold, 3)) + " %. Profit: " + str((goldprice-og_gold_price)) + ". Current price: " + str(round(goldprice)) +  " VND\n")
    file.write("=====================================\n")
    file.write("Total original asset: " + str(round(TOTAL_ASSET_ORIGINAL)) + " VND\n")
    file.write("Total current asset: " + str(round(TOTAL_ASSET)) + " VND\n")
    file.write("Total profit: " + str(round(rev,4)) + " VND -> " + str(rounded_rev) + " %\n" )
    file.write("\n\nLast updated: " + day_now[:19] + "\n")
    file.write("\n\n\n\nAn investment in knowledge pays the best interest. — Benjamin Franklin")

    
print("Investment report saved to " + directory)













    

   



