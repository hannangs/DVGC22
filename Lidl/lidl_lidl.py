from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import datetime, timedelta

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

doc_ref2 = db.collection(u'Nyckelord')
doc2 = doc_ref2.get()
doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Lidl')
doc = doc_ref.get()
Butiker=['Lidl Rattgatan', 'Lidl Östra Infarten']

veckoStart = datetime.now()

def prisKilo(vikt, pris):
    try:
        jamfortPris_kg.append(int(pris)/vikt)
        jamfortPris_L.append("information saknas")
    except:
        info_saknas()

def prisLit(volym, pris):
    try:
        jamfortPris_L.append(int(pris)/volym)
        jamfortPris_kg.append("information saknas")
    except:
        info_saknas()

def string_to_decimal(volym):
    try: 
        if 'kg' in volym:
            volym=volym.replace('kg', '')
        else:
            volym=prisPerEnhet.replace('l', '')
        
        if ',' in volym:
            temp3=volym.split(',')
            temp2=volym.replace(',', '')
            if len(temp3[0])==1:
                temp2=int(temp2)*100
                temp4=(temp2)/1000
                return temp4
            if len(temp3[0])==2:
                temp2=int(temp2)*10
                temp4=(temp2)/1000
                return temp4
        else:
            return int(volym)
    except:
        info_saknas()

def gram_to_kg(temp):
    temp=(int(temp))/1000
    return(temp)

def info_saknas():
    jamfortPris_kg.append('Information saknas')
    jamfortPris_L.append('Information saknas') 

LankarErbjButik=[]
for docs in doc:
    Titlar=list(docs._data.keys())
    Data=list(docs._data.values())
    val='Länk lidl'
    ind=Titlar.index(val)
    Data[ind]
    LankarErbjButik.append(Data[ind])

butik_nr = 0

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
    giltigStart=[]
    giltigSlut=[]
    
    time.sleep(2)

    driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
    driver.get(i)
    content = driver.page_source

    try:
        button=driver.find_element("xpath",'//*[@id="CybotCookiebotDialog"]/div/div[1]/button')
        button.click()
        time.sleep(2)
    except:
        print()

    soup = BeautifulSoup(content, features="html.parser")

    for data in soup.find_all('span', class_='lidl-m-ribbon-item__text'):
        
        datum=data.text
        if datum=='Måndag - onsdag':
            giltigStart.append(veckoStart)
            tidBer = timedelta(days=2)
            giltigSlut.append(veckoStart + tidBer)
        elif datum=='Måndag - söndag':
            giltigStart.append(veckoStart)
            tidBer = timedelta(days=6)
            giltigSlut.append(veckoStart + tidBer)
        elif datum=='Torsdag - söndag':
            tidBer = timedelta(days=3)
            Start=veckoStart + tidBer
            giltigStart.append(veckoStart + tidBer)
            giltigSlut.append(Start + tidBer)
        elif datum=='Lördag - söndag':
            tidBer = timedelta(days=5)
            tidBer2 = timedelta(days=1)
            Start=veckoStart + tidBer
            giltigStart.append(veckoStart + tidBer)
            giltigSlut.append(Start + tidBer2)


    for a in soup.find_all('a', class_='ret-o-card__link nuc-a-anchor'):
        titel=a.find('h3', attrs={'class':'ret-o-card__headline'}).text
        if '\n' in titel:
            titel=titel.replace('\n', '')
            titel=titel.strip()
        if '/' in titel:
            titel=titel.replace('/', ' eller ')
        Produkter.append(titel)

        try:
            marke=a.find('p', attrs={'class':'ret-o-card__content'})
            if '\n' in marke.text:
                marke=marke.text
                marke=marke.replace('\n', '')
                marke=marke.strip()
            Marken.append(marke.text)
        except:
            Marken.append("Märke saknas")

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

            if  ((doc2[b].id).lower()) in ((titel.lower()) or (marke.text.str.lower())):
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
            price1=(a.find('span', attrs={'class':'lidl-m-pricebox__price'})).text
        except:
            price1="Pris saknas"
        
        try:
            price2=(a.find('div', attrs={'class':'lidl-m-pricebox__highlight'})).text
            if 'SUPERPRIS!' in price2:
                price2=""
            
            if '%' in price2:
                price2=""
                pris_temp=price1
            else:
                pris_temp=(price2+" "+price1)
        except:
            price2=""
            pris_temp=price1
        Pris.append(pris_temp)

        if 'FÖR:' in pris_temp:
            temp2=pris_temp.replace(' FÖR: ', '/')
            temp3=temp2.replace(':-', '')
            temp4=temp3.split('/')
            tal1=int(temp4[0])
            tal2=int(temp4[1])
            jamfortPris_st.append(tal2/tal1)
        else:
            pris_temp=pris_temp.replace(':', '.')
            pris_temp=pris_temp.replace('-', '0')
            jamfortPris_st.append((pris_temp))

        try:
            prisPerEnhet=a.find('div', attrs={'lidl-m-pricebox__basic-quantity'}).text
        except:
            try: prisPerEnhet=a.find('span', attrs={'lidl-m-pricebox__discount-prefix'}).text
            except: 
                prisPerEnhet="Info saknas"
        
        try:
            if ':-' in price1:
                jmf_pris=price1.replace(':-','').strip()
            elif '.' in price1:
                jmf_pris=int(round(float(price1)))
        except:
            jmf_pris=int(round(float(price1)))

        if '/förp.' in prisPerEnhet:
            prisPerEnhet=prisPerEnhet.replace('/förp.','').strip()

        if 'blad' in prisPerEnhet:
            prisPerEnhet=''
        elif 'Olika sorter' in prisPerEnhet:
            prisPerEnhet=''
        elif 'olika utföranden' in prisPerEnhet:
            prisPerEnhet=''
        elif 'timmar' in prisPerEnhet:
            prisPerEnhet=''

        if ',' in prisPerEnhet:
            temp=prisPerEnhet.split(',')
            prisPerEnhet=temp[0]

        if '/st.' in prisPerEnhet:
            prisPerEnhet=prisPerEnhet.replace('/st.','').strip()
            if '' in prisPerEnhet:
                flag=1            

        if '×' in prisPerEnhet:
            temp=prisPerEnhet.split('×')
            temp3=prisPerEnhet.split(' ')
            temp3=temp3[0]
            tal1=temp[0]
            temp2=temp[1].split(' ')
            tal2=temp2[0]
            try:
                prisPerEnhet=prisPerEnhet.replace(temp3,str(int(tal1)*int(tal2)))
            except:
                print()
        elif 'x' in prisPerEnhet:
            temp=prisPerEnhet.split('x')  
            temp3=prisPerEnhet.split(' ')
            temp3=temp3[0]
            tal1=temp[0]
            temp2=temp[1].split(' ')
            tal2=temp2[0]
            try:
                prisPerEnhet=prisPerEnhet.replace(temp3,str(int(tal1)*int(tal2)))
            except:
                print()

        if '–' in prisPerEnhet:
            temp1=prisPerEnhet.split('–')
            prisPerEnhet=temp1[1].strip()

        if '/kg' in prisPerEnhet:
            jamfortPris_kg.append(price1)
            jamfortPris_L.append('Information saknas')

        elif 'kg' in prisPerEnhet:
            temp4=string_to_decimal(prisPerEnhet)
            prisKilo(temp4, jmf_pris)

        elif ('g' in prisPerEnhet):
            temp_vikt=prisPerEnhet.replace('g', '')
            try:
                temp_vikt2=gram_to_kg(temp_vikt)
                prisKilo(temp_vikt2, int(jmf_pris))
            except:
                info_saknas() 

        elif 'ml' in prisPerEnhet:
            temp_volym1=prisPerEnhet.replace('ml', '')
            temp_volym=gram_to_kg(temp_volym1)
            prisLit(temp_volym, jmf_pris)

        elif 'dl' in prisPerEnhet:
            temp_volym1=prisPerEnhet.replace('dl', '')
            if ',' in temp_volym1:
                temp_volym1=temp_volym1.replace(',', '')
            temp_volym=int(round(float(temp_volym1)))/10
            prisLit(temp_volym, jmf_pris)
        
        elif 'cl' in prisPerEnhet:
            temp_volym1=prisPerEnhet.replace('cl', '')
            if ',' in temp_volym1:
                temp_volym1=temp_volym1.replace(',', '')
            temp_volym=int(round(float(temp_volym1)))/1000
            prisLit(temp_volym, jmf_pris)

        elif 'lökar' in prisPerEnhet:
            info_saknas()

        elif 'l' in prisPerEnhet:
            temp4=string_to_decimal(prisPerEnhet)
            prisLit(temp4, jmf_pris)
        else:
            info_saknas()     
    
    for y in range(len(soup.find_all('a', class_='ret-o-card__link nuc-a-anchor'))):

        data = {
            "info om erbj": "Lördag-söndag",
            "Varumärke/ursprung": Marken[y],
            "Pris": Pris[y],
            "Jämfört pris(st)": jamfortPris_st[y],
            "Jämfört pris(/kg)": jamfortPris_kg[y],
            "Jämfört pris(/lit)": jamfortPris_L[y],    
            "Kategori": Kategori[y],
            "Giltig start": giltigStart[y],
            "Giltig slut": giltigSlut[y],
            "Nyckelord": keyWord[y],
        }
        def save(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
        save(          
            collection_id1="Aktiva erbj.",
            document_id1 ="Lidl",
            collection_id= Butiker[butik_nr],
            document_id =Produkter[y],
            data = data,
        )

    butik_nr=butik_nr+1

    driver.quit()