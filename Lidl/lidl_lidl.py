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

def prisKilo(vikt, pris):
    jamfortPris_kg.append(int(pris)/vikt)
    jamfortPris_L.append("information saknas")
    #print('vikt:', int(pris)/vikt)

def prisLit(volym, pris):
    jamfortPris_L.append(int(pris)/volym)
    jamfortPris_kg.append("information saknas")
    #print('Lit:', int(pris)/volym)

def string_to_decimal(volym):
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

for i in LankarErbjButik:
    Produkter=[]
    Marken=[]
    Pris=[]
    jamfortPris_st=[]
    jamfortPris_kg=[]
    jamfortPris_L=[]
    Kategori=[]
    info=[]
    giltigStart = datetime.now()
    tidBer = timedelta(days=6)
    giltigSlut = giltigStart + tidBer
    #driver.get('%s' % URL)
    time.sleep(2)

    driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
    driver.get(i)
    content = driver.page_source

    button=driver.find_element("xpath",'//*[@id="CybotCookiebotDialog"]/div/div[1]/button')
    button.click()
    time.sleep(2)

    soup = BeautifulSoup(content, features="html.parser")

    for a in soup.find_all('a', class_='ret-o-card__link nuc-a-anchor'):
        titel=a.find('h3', attrs={'class':'ret-o-card__headline'}).text
        if '\n' in titel:
            titel=titel.replace('\n', '')
            titel=titel.strip()
        if '/' in titel:
            titel=titel.replace('/', ' eller ')
        Produkter.append(titel)

        for word in doc2:
            if word.id in titel:
                temp=list(word._data.values())
                Kategori.append(temp[0])
            else:
                Kategori.append("Övrigt")

        try:
            marke=a.find('p', attrs={'class':'ret-o-card__content'})
            if '\n' in marke.text:
                marke=marke.text
                marke=marke.replace('\n', '')
                marke=marke.strip()
            Marken.append(marke.text)
        except:
            Marken.append("Märke saknas")

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
            prisPerEnhet=a.find('span', attrs={'lidl-m-pricebox__discount-prefix'}).text
        
        try:
            if ':-' in price1:
                jmf_pris=price1.replace(':-','').strip()
            elif '.' in price1:
                jmf_pris=int(round(float(price1)))
        except:
            jmf_pris=int(round(float(price1)))

        if '/förp.' in prisPerEnhet:
            prisPerEnhet=prisPerEnhet.replace('/förp.','').strip()

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
            "info om erbj": "Lidl pris",
            "Varumärke/ursprung": Marken[y],
            "Pris": Pris[y],
            "Jämfört pris(st)": jamfortPris_st[y],
            "Jämfört pris(/kg)": jamfortPris_kg[y],
            "Jämfört pris(/lit)": jamfortPris_L[y],    
            "Kategori": Kategori[y],
            "Giltig start": giltigStart,
            "Giltig slut": giltigSlut,
            "Övrig info":"test", #info[y],
        }

        def save1(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
                
        save1(          
            collection_id1="Aktiva erbj.",
            document_id1 ="Lidl",
            collection_id= "Lidl Rattgatan",
            document_id =Produkter[y],
            data = data
        )

        def save2(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
                
        save2(          
            collection_id1="Aktiva erbj.",
            document_id1 ="Lidl",
            collection_id= "Lidl Östra Infarten",
            document_id =Produkter[y],
            data = data
        )

    driver.quit()