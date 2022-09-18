from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from selenium import webdriver
import requests


cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Willys')
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
    driver.get(URL)
    content = driver.page_source
    
    Produkter=[]
    extraData=[]
    Pris=[]
    Marken=[]
    giltighetsdatum="Giltigt 2022-09-12 till 2022-09-18."

    driver.get('%s' % URL)
    
    time.sleep(3)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,'onetrust-accept-btn-handler'))).click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Buttonstyles__StyledButton-sc-1g4oxwr-0.dLUxJp.LoadMore__LoadMoreBtn-sc-16fjaj7-3.bnbvpm"))).click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        print("ingen cookie")

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    Butik=soup.find('h2', attrs={'class':'Headingstyles__StyledH2-sc-r7tfy8-1 cJhDBd'}).text

    for a in soup.find_all(attrs='Productstyles__StyledProduct-sc-16nua0l-0 aRuiG'):
            titel=a.find(attrs={'class':'Productstyles__StyledProductName-sc-16nua0l-5 dqhhbm'}).text
            if '/' in titel:
                titel=titel.replace('/', ' eller ')
                Produkter.append(titel)
            else:
                Produkter.append(titel)
            
            temp_info=(a.find('p', attrs={'class':'Productstyles__StyledProductDisplayVolume-sc-16nua0l-8 eyLzNX'}))
            #temp_info2=temp_info.split('\n')[1::1]
            #info=temp_info2[1].strip()
            extraData.append(temp_info)

            try:
                marke=a.find('span', attrs={'class':'Productstyles__StyledProductManufacturerBrand-sc-16nua0l-7 hnYIHY'})
                Marken.append(marke.text)
            except:
                Marken.append("Märke saknas")        
            
            try:
                price1=(a.find('span', attrs={'class':'PriceLabelstyles__StyledProductPriceText-sc-koui33-2 dzPBER'})).text
            except:
                price1=(a.find('span', attrs={'class':'Splash-text'})).text

            price2=(a.find('span', attrs={'class':'PriceLabelstyles__StyledProductPriceDecimal-sc-koui33-5 jzJfVO'}))
            try:
                if(price2.string=="\xa0"):
                    price=price1
                else:
                    price=price1+":"+price2.text
            except:
                price=price1
            
            try:
                price3=(a.find(attrs={'class':'Productstyles__StyledProductSavePrice-sc-16nua0l-14 bTZMtp'})).text
                if(price3==''):
                    price=price

                else:
                    price=price3+" "+price
            except:
                price3=0
            
            Pris.append(price)

    for i in range(len(soup.find_all(attrs='Productstyles__StyledProduct-sc-16nua0l-0 aRuiG'))):

        data = {
            "Märke/ursprung": Marken[i],
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