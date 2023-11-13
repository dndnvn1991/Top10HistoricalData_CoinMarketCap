# Project: Lấy lịch sử giá THEO NGÀY tại CoinMarketCap với điều kiện chỉ lấy 10 đồng coin có vốn hóa lớn nhất


import pandas as pd
import requests
from bs4 import BeautifulSoup

''' https://coinmarketcap.com/historical/   lay top 10 dong coin: tra ve thong so ten/symbol/gia/marketcap va cirrculatong '''
#Create empty lists to store data
name_list = []
symbol_list = []
marketcap_list = []
price_list = []
circulatting_list = []

#Creat an empty dataframe to help organize the data
df = pd.DataFrame()

#Create a function to scrape the data
# https://coinmarketcap.com/historical/

def scrape(date = '20211219/'):
    url = 'https://coinmarketcap.com/historical/' + date
    #Make a requset to the website and Parse the text from website
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    #Get the table row element
    tr = soup.find_all('tr', attrs={'class':'cmc-table-row'})
    
    #Loop through every row to gather the data/infomation
    count = 0
    for row in tr:
        #if the count is reached the break out of the loop
        if count == 10:
            break;
        count = count + 1 

        #Store the name of the crpto into a variable
        name_col = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'}).text.strip()
        symbol_col = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__symbol'}).text.strip()
        marketcap_col = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).text.strip()
        price_col = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).text.strip()
        circulating_col_contain_symbol = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'}).text.strip()    
        # Vi data circulation_col trong web tra ve 2 gia tri "19.077.962 BTC" nen ta Split data == . split(' ')[0] --> Split phan tu co khoan trang va chi lay phan tu dau tien
        circulating_col = circulating_col_contain_symbol.split(' ')[0]
    
        #Append data to la lists
        name_list.append(name_col)
        symbol_list.append(symbol_col)
        marketcap_list.append(marketcap_col)
        price_list.append(price_col)
        circulatting_list.append(circulating_col)

'''
#Store the data in a dataframe to help organize data

'''



#Run the function 
scrape(date = '20220626/')

#Store the data in a dataframe to help organize data: CÁCH 1
print('==========================FIRST WAY=====================================')
my_dict = { 'Name': name_list, 
            'Symbol': symbol_list, 
            'Market Cap': marketcap_list, 
            'Price': price_list, 
            'Circulating Supply': circulatting_list
        }
df_data = pd.DataFrame(my_dict)
print(df_data)

#Store the data in a dataframe to help organize data: CÁCH 2
print('============================SECOND WAY=====================================')
df['Name'] = name_list
df['Symbol'] = symbol_list
df['Market Cap']= marketcap_list
df['Price'] = price_list
df['Circulating Supply'] = circulatting_list
print(df)

#Print out DATA to the CSV or EXCEL: lấy và không lấy Index vô file và ĐẶt tên Sheet tạo ra trong file Excel
df_data.to_csv('10Coin_Firstway.csv')
df.to_csv('10Coin_Secondway.csv')

df_data.to_excel('10Coin_Firstway.xlsx')
df.to_excel('10Coin_Secondway.xlsx')

df_data.to_excel('10Coin_Firstway_Index.xlsx', index=False)
df.to_excel('10Coin_Secondway_Index.xlsx', index = False)

#Dat ten Sheet tao ra trong Excel
df.to_excel('10Coin_Secondway_Index_Sheet.xlsx', sheet_name='10Ten', index = False)
