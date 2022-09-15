from urllib import response
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL="https://www.coop.se/butiker-erbjudanden/coop/coop-city-karlstad/"

from selenium.webdriver.chrome.service import Service
driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
driver.get(URL)
content = driver.page_source

Butik="Coop"
Produkter=[]
Pris=[]
giltighetsdatum="nuvarande vecka"

driver.get('%s' % URL)
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmpboxbtnyes"))).click()
except:
    print("No cookie?") 
    
soup = BeautifulSoup(content, features="html.parser")
i = 0

r = requests.get('https://www.coop.se/butiker-erbjudanden/coop/coop-city-karlstad/')
soup = BeautifulSoup(r.content, 'html.parser')
len(soup.find_all('article', class_='ItemTeaser'))

#for a in soup.findAll('article',href=True, attrs={'class':'ItemTeaser'}):
#    titel=a.find('h3', attrs={'class':'ItemTeaser-heading'})
#    #titel=a.find('div', attrs={'class':'IteamTeaser-info'})
#    price=a.find('span', attrs={'class':'Splash-priceLarge'})
#    i = i+1
#    Produkter.append(titel.text)
#    Pris.append(price.text)

df = pd.DataFrame({'Kedja:': Butik,'Product Name:':Produkter,'Price:':Pris}) 
df.to_csv('products.csv', index=False, encoding='utf-8')

print(i)

#<a class="cmpboxbtn cmpboxbtnyes cmptxt_btn_yes" role="button" href="#">
#<span id="cmpbntyestxt">Acceptera alla cookies</span></a>

#test coop: https://www.coop.se/butiker-erbjudanden/coop/coop-city-karlstad/
#for a in soup.findAll('div', attrs={'class':'IteamTeaser-content'}):
    #titel=a.find('h3', attrs={'class':'IteamTeaser-heading'})
    #titel=a.find('div', attrs={'class':'IteamTeaser-info'})
    #price=a.find('span', attrs={'class':'Splash-priceLarge'})

#test ica: https://www.ica.se/butiker/kvantum/hammaro/ica-kvantum-hammaro-16102/erbjudanden/
#
#