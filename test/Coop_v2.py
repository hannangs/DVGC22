from urllib import response
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

URL="https://www.coop.se/butiker-erbjudanden/coop/coop-city-karlstad/"

from selenium.webdriver.chrome.service import Service
driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
driver.get(URL)
content = driver.page_source

Produkter=[]
Marken=[]
extraData=[]
Pris=[]
giltighetsdatum=[]

driver.get('%s' % URL)
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmpboxbtnyes"))).click()
except:
    print("No cookie?") 
    
soup = BeautifulSoup(content, features="html.parser")
Butik=soup.find('h2', attrs={'class':'u-text1XLarge u-textFamilySecondary u-colorMidBase u-marginBz u-marginRxsm'})

for a in soup.find_all('article', class_='ItemTeaser'):
    titel=a.find('h3', attrs={'class':'ItemTeaser-heading'})
    Produkter.append(titel.text)

    try:
        marke=a.find('span', attrs={'class':'ItemTeaser-brand'})
        Marken.append(marke.text)
    except:
        Marken.append("Märke saknas")
    
    temp_info=(a.find('p', attrs={'class':'ItemTeaser-description'})).text
    temp_info2=temp_info.split('\n')[1::1]
    info=temp_info2[1].strip()
    extraData.append(info)

    price1=(a.find('span', attrs={'class':'Splash-priceLarge'})).text
    price2=(a.find('span', attrs={'class':'Splash-priceSup'}))
    try:
        if(price2.string=="\xa0"):
            price=price1
        else:
            price=price1+":"+price2.text
    except:
        price=price1
    
    price3=(a.find('span', attrs={'class':'Splash-pricePre'})).text
    if(price3==''):
        price=price

    else:
        price=price3+" "+price
    
    Pris.append(price)

antalProdukter=len(soup.find_all('article', class_='ItemTeaser'))

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)

for i in range(antalProdukter):

    data = {
        "Varumärke/ursprung": Marken[i],
        "Övrig information": extraData[i],
        "Pris": Pris[i],
        "Giltig datum": giltighetsdatum
    }

    db=firestore.client()

    def save(collection_id, document_id, data):
        db.collection(collection_id).document(document_id).set(data)

    save(
        collection_id =Butik.text,
        document_id= Produkter[i],
        data = data
    )

#test ica: https://www.ica.se/butiker/kvantum/hammaro/ica-kvantum-hammaro-16102/erbjudanden/

