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

doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Coop')
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
    Marken=[]
    extraData=[]
    Pris=[]
    giltighetsdatum="Giltigt 2022-09-12 till 2022-09-18."

    driver.get('%s' % URL)
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmpboxbtnyes"))).click()
    except:
        print("No cookie?") 
        
    soup = BeautifulSoup(content, features="html.parser")
    Butik=soup.find('h2', attrs={'class':'u-text1XLarge u-textFamilySecondary u-colorMidBase u-marginBz u-marginRxsm'})

    for a in soup.find_all('article', class_='ItemTeaser'):
        titel=a.find('h3', attrs={'class':'ItemTeaser-heading'})
        if '/' in titel.text:
            titel=titel.text
            titel=titel.replace('/', ' eller ')
            Produkter.append(titel)
        else:
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

        try:
            price1=(a.find('span', attrs={'class':'Splash-priceLarge'})).text
        except:
            price1=(a.find('span', attrs={'class':'Splash-text'})).text

        price2=(a.find('span', attrs={'class':'Splash-priceSup'}))
        try:
            if(price2.string=="\xa0"):
                price=price1
            else:
                price=price1+":"+price2.text
        except:
            price=price1
        
        try:
            price3=(a.find('span', attrs={'class':'Splash-pricePre'})).text
            if(price3==''):
                price=price

            else:
                price=price3+" "+price
        except:
            price3=0
        
        Pris.append(price)

    antalProdukter=len(soup.find_all('article', class_='ItemTeaser'))

    for i in range(antalProdukter):

        data = {
            "Varumärke/ursprung": Marken[i],
            "Övrig information": extraData[i],
            "Pris": Pris[i],
            "Giltig datum": giltighetsdatum,
        }

        db=firestore.client()

        def save(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)

        save(          
            collection_id1="Aktiva erbj.",
            document_id1 ="Coop",
            collection_id= Butik.text,
            document_id =Produkter[i],
            data = data
        )