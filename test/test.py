from urllib import response
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

URL="https://www.coop.se/butiker-erbjudanden/coop/coop-city-karlstad/"

response=requests.get(URL)
page_content = BeautifulSoup(response.content, "html.parser")

Butik="Coop"
Produkter=[]
Pris=[]
giltighetsdatum="nuvarande vecka"
driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver")
driver.get('https://www.coop.se/butiker-erbjudanden/coop/coop-city-karlstad/')
content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll('a',href=True, attrs={'class':'IteamTeaser-content'}):
    titel=a.find('div', attrs={'class':'IteamTeaser-info'})
    price=a.find('div', attrs={'class':'Splash-priceLarge'})

    Produkter.append(titel.text)
    Pris.append(price.text)

df = pd.DataFrame({'Kedja': Butik,'Product Name':Produkter,'Price':Pris}) 
df.to_csv('products.csv', index=False, encoding='utf-8')



