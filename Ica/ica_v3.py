from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
import time

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
driver.set_window_size(1920, 1080)

doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'ICA')
doc = doc_ref.get()
doc_ref2 = db.collection(u'Nyckelord')
doc2 = doc_ref2.get()

giltigStart = datetime.now()
tidBer = timedelta(days=6)
giltigSlut = giltigStart + tidBer

LankarErbjButik=[]
for docs in doc:
    Titlar=list(docs._data.keys())
    Data=list(docs._data.values())
    val='Länk erbj.'
    ind=Titlar.index(val)
    Data[ind]
    LankarErbjButik.append(Data[ind])

def deny():
    jamfortPris_kg.append("Data saknas")
    jamfortPris_L.append("Data saknas")

def prisKoll(info_temp0):
    try:
        if 'utan spad' in info_temp0:
            info_temp0=info_temp0.replace(' utan spad','') 
        
        if '/kg.' in info_temp0:
            if '-' in info_temp0:
                info_temp3=info_temp0.split('-')
                info_temp4=info_temp3[1].replace('/kg.', '')
                info_temp5=info_temp4.replace(':', '.').strip()
                jamfortPris_kg.append(info_temp5)
                jamfortPris_L.append("Data saknas")
            elif '/kg.' in info_temp0:
                info_temp3=info_temp0.replace('Jfr pris', '')
                info_temp4=info_temp3.replace('/kg.', '')
                info_temp5=info_temp4.replace(':', '.').strip()
                jamfortPris_kg.append(info_temp5)
                jamfortPris_L.append("Data saknas")
            else:
                deny()
                print(info_temp0)
        elif '/liter.' in info_temp0:  
            if '-' in info_temp0:
                info_temp3=info_temp0.split('-')
                info_temp4=info_temp3[1].replace('/liter.', '')
                info_temp5=info_temp4.replace(':', '.').strip()
                jamfortPris_kg.append(info_temp5)
                jamfortPris_L.append("Data saknas")
            elif '/liter.' in info_temp0:
                info_temp3=info_temp0.replace('Jfr pris', '')
                info_temp4=info_temp3.replace('/liter.', '')
                info_temp5=info_temp4.replace(':', '.').strip()
                jamfortPris_L.append(info_temp5)
                jamfortPris_kg.append("Data saknas")
            else:
                deny()
                print(info_temp0)
        else:
            deny()
            print(info_temp0)
    except:
        deny()

def hamtaData(a):
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

    for b in range (0,len(doc2)):
        temp=titel.lower()
        if('te' == temp):
            Kategori.append('Drink')
            keyWord.append('Te')
            break
        elif(temp.startswith('öl')):
            if 'korv' in temp:
                ...
            else:
                Kategori.append('Drink')
                keyWord.append('Öl')
                break
        elif('bullar'== temp):    
            Kategori.append('Ice cream, sweers & snacks')
            keyWord.append('Bullar')
            break

        if  ((doc2[b].id).lower()) in ((titel.lower())):    
            Titlar=list((doc2[b])._data.keys())
            Data=list((doc2[b])._data.values())
            ind=Titlar.index('Kategori')
            Kategori.append(Data[ind])
            keyWord.append(doc2[b].id)
            break
    
    if len(Produkter) > len(Kategori):
        Kategori.append("Övrigt")
        keyWord.append("Ord saknas")

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

    try:
        if ' för ' in price:
            temp2=price.replace(' för ', '/')
            temp3=temp2.replace(':-', '')
            temp4=temp3.split('/')
            tal1=int(temp4[0])
            tal2=int(temp4[1])
            jamfortPris_st.append(tal2/tal1)
        else:
            pris_temp=price.replace(':', '.')
            pris_temp=price.replace('-', '0')
            jamfortPris_st.append((pris_temp))
    except:
        jamfortPris_st.append((price))

for i in LankarErbjButik:
    driver.get(i)

    Produkter=[]
    extraData=[]
    Pris=[]
    Kategori=[]
    jamfortPris_st=[]
    jamfortPris_kg=[]
    jamfortPris_L=[]
    keyWord=[]

    plus=[]
    minus=[]

    driver.get('%s' % i)

    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".banner-actions-container"))).click()
    except:
        ...

    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    Butik=soup.find('h1', attrs={'class':'store-heading'}).text

    temp_produkt=len(soup.find_all('div', class_='offer-type js-open-product-info offer-type--regular-hit'))+len(soup.find_all('div', class_='offer-type js-open-product-info offer-type--focus-item'))+len(soup.find_all('div', class_='offer-type js-open-product-info offer-type--focus-item  active'))
    temp_prodikt2=len(soup.find_all('div', class_='product-info-wrapper'))

    for a in soup.find_all('div', class_='product-info-wrapper'):
        temp_prisinfo=a.text
        info_temp=temp_prisinfo.split('\n')
        while '' in info_temp:
            info_temp.remove('')

        if(len(info_temp)<=5):
            deny()
        elif(len(info_temp)==6):
            if '/kg' in info_temp[3] or '/liter.' in info_temp[3]:
                info_temp2=info_temp[3]
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'
                prisKoll(info_temp2)
            else:
                deny() 
        elif(len(info_temp)==9):
            if '/kg' in info_temp[6] or '/liter.' in info_temp[6]:
                info_temp2=info_temp[6]
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'
                prisKoll(info_temp2)
            else:
                deny()
        elif(len(info_temp)==10):
            if '/kg' in info_temp[7] or '/liter.' in info_temp[7]:
                info_temp2=info_temp[7]
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'
                prisKoll(info_temp2)
            else:
                deny()
        elif(len(info_temp)==11):
            if '/kg' in info_temp[8] or '/liter.' in info_temp[8]:
                info_temp2=info_temp[8]
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'
                prisKoll(info_temp2)
            else:
                deny()
        elif(len(info_temp)==12):
            if '/kg' in info_temp[9] or '/liter.' in info_temp[9]:
                info_temp2=info_temp[9]
                if '\xa0' in info_temp2:
                    info_temp2=info_temp2.replace('\xa0', '')
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'
                prisKoll(info_temp2)
            else:
                deny()
        elif(len(info_temp)==13):
            if '/kg' in info_temp[10] or '/liter.' in info_temp[10]:
                info_temp2=info_temp[10]
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'                    
                prisKoll(info_temp2)
            else:
                deny()
        elif(len(info_temp)==14):
            if '/kg' in info_temp[11] or '/liter.' in info_temp[11]:
                info_temp2=info_temp[11]
                if '/st' in info_temp2:
                    info_temp2=info_temp2.split(',')
                    info_temp2=info_temp2[0]+'.'
                prisKoll(info_temp2)
            else:
                deny()
        else:
            deny()

    for kateg in soup.find_all('div', class_='offer-category__body'):
        
        for u in kateg.find_all('div', class_='offer-type js-open-product-info offer-type--focus-item'): 
            hamtaData(u)

        for w in kateg.find_all('div', class_='offer-type js-open-product-info offer-type--regular-hit'):
            hamtaData(w)

    antalProdukter=len(soup.find_all('div', class_='offer-type__product-details'))
    for y in range(antalProdukter):
        data = {
            "Övrig information": extraData[y],
            "Pris": Pris[y],
            "Kategori": Kategori[y],
            "Giltig start": giltigStart,
            "Giltig slut": giltigSlut,
            "Jämfört pris(st)":jamfortPris_st[y],
            "Jämfört pris(kg)": jamfortPris_kg[y],
            "Jämfört pris(lit)": jamfortPris_L[y],
            "Nyckelord": keyWord[y],
        }

        def save1(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
        save1(          
            collection_id1="Aktiva erbj.",
            document_id1 ="ICA",
            collection_id= Butik,
            document_id =Produkter[y],
            data = data
        )