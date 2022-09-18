from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Ica')
doc = doc_ref.get()

LankarErbjButik=[]
for docs in doc:
    Titlar=list(docs._data.keys())
    Data=list(docs._data.values())
    val='Länk erbj.'
    ind=Titlar.index(val)
    Data[ind]
    LankarErbjButik.append(Data[0])

for i in LankarErbjButik:

    URL = i
    driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
    driver.set_window_size(1920, 1080)
    driver.get(URL)
    content = driver.page_source
    
    Produkter=[]
    extraData=[]
    Pris=[]
    giltighetsdatum="Giltigt 2022-09-12 till 2022-09-18."

    driver.get('%s' % URL)

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".banner-actions-container"))).click()
    except:
        print("No cookie?") 

    soup = BeautifulSoup(content, features="html.parser")
    Butik=soup.find('h1', attrs={'class':'store-heading'}).text

 ######################################################################################################

    for a in soup.find_all('div', class_='offer-type js-open-product-info offer-type--focus-item'): #ändra?
        
        try:
            titel=a.find('h2', attrs={'class':'offer-type__product-name splash-bg icon-store-pseudo'})
            if not titel:
                titel=a.find('h2', attrs={'class':'offer-type__product-name splash-bg icon-store-pseudo no-price'})
        except:
            titel="titel saknas"
        
        try:
            titel=titel.text.replace('\n', '')
            titel=titel.strip()
        except:
            titel="titel saknas"

        if '/' in titel:
            titel=titel.replace('/', ' eller ')
            Produkter.append(titel)
        else:
            Produkter.append(titel)

        try:
            info=(a.find('p', attrs={'class':'offer-type__product-info'})).text
        except:
            info=""

        extraData.append(info)

        try:
            price1=(a.find('div', attrs={'class':'product-price__price-value'})).text
        except:
            price1="temp" #text istället för pris?

        price2=(a.find('div', attrs={'class':'product-price__decimal'})) #ören
        try:
            if(price2.string=="\xa0"):
                price=price1
            else:
                price=price1+":"+price2.text
        except:
            price=price1
        
        try:
            price3=(a.find('div', attrs={'class':'product-price__amount'})).text
            if(price3==''):
                price=price

            else:
                price=price3+" "+price
        except:
            price3=0
        
        Pris.append(price)

 ########################################################################################################

    for a in soup.find_all('div', class_='offer-type js-open-product-info offer-type--focus-item  active'): #ändra?
        
        try:
            titel=a.find('h2', attrs={'class':'offer-type__product-name splash-bg icon-store-pseudo'})
            if not titel:
                titel=a.find('h2', attrs={'class':'offer-type__product-name splash-bg icon-store-pseudo no-price'})
        except:
            titel="titel saknas"
        
        try:
            titel=titel.text.replace('\n', '')
            titel=titel.strip()
        except:
            titel="titel saknas"

        if '/' in titel:
            titel=titel.replace('/', ' eller ')
            Produkter.append(titel)
        else:
            Produkter.append(titel)

        try:
            info=(a.find('p', attrs={'class':'offer-type__product-info'})).text
        except:
            info=""

        extraData.append(info)

        try:
            price1=(a.find('div', attrs={'class':'product-price__price-value'})).text
        except:
            price1="temp" #text istället för pris?

        price2=(a.find('div', attrs={'class':'product-price__decimal'})) #ören
        try:
            if(price2.string=="\xa0"):
                price=price1
            else:
                price=price1+":"+price2.text
        except:
            price=price1
        
        try:
            price3=(a.find('div', attrs={'class':'product-price__amount'})).text
            if(price3==''):
                price=price

            else:
                price=price3+" "+price
        except:
            price3=0
        
        Pris.append(price)

 ########################################################################################################
 
    for a in soup.find_all('div', class_='offer-type js-open-product-info offer-type--regular-hit'): #ändra?
            
        try:
            titel=a.find('h2', attrs={'class':'offer-type__product-name splash-bg icon-store-pseudo'})
            if not titel:
                titel=a.find('h2', attrs={'class':'offer-type__product-name splash-bg icon-store-pseudo no-price'})
        except:
            titel="titel saknas"
            
        try:
            titel=titel.text.replace('\n', '')
            titel=titel.strip()
        except:
            titel=titel

        if '/' in titel:
            titel=titel.replace('/', ' eller ')
            Produkter.append(titel)
        else:
            Produkter.append(titel)

        try:
            info=(a.find('p', attrs={'class':'offer-type__product-info'})).text
        except:
            info=""

        extraData.append(info)

        try:
            price1=(a.find('div', attrs={'class':'product-price__price-value'})).text
        except:
            price1="temp"

        price2=(a.find('div', attrs={'class':'product-price__decimal'})) #ören
        try:
            if(price2.string=="\xa0"):
                price=price1
            else:
                price=price1+":"+price2.text
        except:
            price=price1
        
        try:
            price3=(a.find('div', attrs={'class':'product-price__amount'})).text
            if(price3==''):
                price=price

            else:
                price=price3+" "+price
        except:
            price3=0
            
        Pris.append(price)
 
 ########################################################################################################

    antalProdukter=len(soup.find_all('div', class_='offer-type__product-details'))
    
    for i in range(antalProdukter):

        data = {
            "Övrig information": extraData[i],
            "Pris": Pris[i],
            "Giltig datum": giltighetsdatum,
        }

        db=firestore.client()

        def save(collection_id, document_id, data):
            db.collection(collection_id).document(document_id).set(data)

        save(          
            collection_id =Butik,
            document_id= Produkter[i],
            data = data,
        )