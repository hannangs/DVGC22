from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Coop')
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
    LankarErbjButik.append(Data[ind])

for i in LankarErbjButik:
    Produkter=[]
    Marken=[]
    Pris=[]
    jamfortPris_st=[]
    jamfortPris_kg=[]
    jamfortPris_L=[]
    Kategori=[]
    info=[]
    keyWord=[]

    URL = i
    driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
    driver.get(URL)
    content = driver.page_source

    driver.get('%s' % URL)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmpboxbtnyes"))).click()
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
            titel=titel.text

        try:
            marke=a.find('span', attrs={'class':'ItemTeaser-brand'})
            Marken.append(marke.text)
        except:
            Marken.append("Märke saknas") 
            marke=""

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

            if  ((doc2[b].id).lower()) in ((titel.lower()) or (Marken[-1].text.str.lower())):
                Titlar=list((doc2[b])._data.keys())
                Data=list((doc2[b])._data.values())
                ind=Titlar.index('Kategori')
                Kategori.append(Data[ind])
                keyWord.append(doc2[b].id)
                break
    
        if len(Produkter) > len(Kategori):
            Kategori.append("Övrigt")
            keyWord.append("Ord saknas")
     
        temp_info=(a.find('p', attrs={'class':'ItemTeaser-description'})).text
        temp_info2=temp_info.split('\n')[1::1]
        temp_info=temp_info2[1].strip()
        info.append(temp_info)
        
        try:
            if '/kg' in temp_info:
                info_temp1=temp_info.split('.')
                info_temp1.pop()
                try:
                    info_temp2=info_temp1[-1]
                    info_temp3=info_temp2.replace('Jfr-pris', '')
                    info_temp4=info_temp3.replace('/kg', '')
                    info_temp5=info_temp4.replace(':', '.')
                    info_temp=info_temp5.replace('-', '0').strip()
                    jamfortPris_kg.append(info_temp)
                except:
                    info_temp1.pop()
                    info_temp2=info_temp1[-1]
                    info_temp3=info_temp2.replace('Jfr-pris', '')
                    info_temp4=info_temp3.replace('/kg', '')
                    info_temp5=info_temp4.replace(':', '.')
                    info_temp=info_temp5.replace('-', '0').strip()
                    jamfortPris_kg.append(info_temp)
            else:
                jamfortPris_kg.append("Data saknas")
            if '/lit' in temp_info:
                info_temp=temp_info.split('.')
                info_temp.pop()
                info_temp=info_temp[-1]
                info_temp=info_temp.replace('Jfr-pris', '')
                info_temp=info_temp.replace('/lit', '')
                info_temp=info_temp.replace(':', '.')
                info_temp=info_temp.replace('-', '0').strip()
                jamfortPris_L.append(info_temp)
            else:
                jamfortPris_L.append("Data saknas")
        except:
            jamfortPris_kg.append("Data saknas")
            jamfortPris_L.append("Data saknas")
        
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

    antalProdukter=len(soup.find_all('article', class_='ItemTeaser'))
    for y in range(antalProdukter):

        data = {
            "Varumärke/ursprung": Marken[y],
            "Övrig info":info[y],
            "Pris": Pris[y],
            "Jämfört pris(st)": jamfortPris_st[y],
            "Jämfört pris(/kg)": jamfortPris_kg[y],
            "Jämfört pris(/lit)": jamfortPris_L[y],
            "Kategori":Kategori[y],
            "Giltig start": giltigStart,
            "Giltig slut": giltigSlut,
            "Nyckelord": keyWord[y],
        }

        def save1(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
                
        save1(          
            collection_id1="Aktiva erbj.",
            document_id1 ="Coop",
            collection_id= Butik.text,
            document_id =Produkter[y],
            data = data
        )

driver.close()

