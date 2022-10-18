from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import datetime, timedelta

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Willys')
doc = doc_ref.get()
doc_ref2 = db.collection(u'Nyckelord')
doc2 = doc_ref2.get()

giltigStart = datetime.now()
tidBer = timedelta(days=6)
giltigSlut = giltigStart + tidBer

def deny():
    jamfortPris_L.append("information saknas")
    jamfortPris_kg.append("information saknas")

def prisKilo(vikt, pris):
    jamfortPris_kg.append(pris/vikt)
    jamfortPris_L.append("information saknas")

def prisLit(volym, pris):
    jamfortPris_L.append(pris/volym)
    jamfortPris_kg.append("information saknas")

def string_to_decimal(volym):
    if 'kg' in volym:
        volym=prisPerEnhet.replace('kg', '')
    else:
        volym=prisPerEnhet.replace('L', '')
    
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

def gram_to_kg(temp):
    temp=(int(temp))/1000
    return(temp)

LankarErbjButik=[]
for docs in doc:
    Titlar=list(docs._data.keys())
    Data=list(docs._data.values())
    val='Länk erbj.'
    ind=Titlar.index(val)
    Data[ind]
    LankarErbjButik.append(Data[ind])


for i in LankarErbjButik:

    URL = i
    driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
    driver.get(URL)
    
    Produkter=[]
    extraData=[]
    Pris=[]
    Marken=[]
    jamfortPris_st=[]
    jamfortPris_kg=[]
    jamfortPris_L=[]
    Kategori=[]
    keyWord=[]

    driver.get('%s' % URL)
    
    time.sleep(3)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,'onetrust-accept-btn-handler'))).click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Buttonstyles__StyledButton-sc-1g4oxwr-0.dLUxJp.LoadMore__LoadMoreBtn-sc-16fjaj7-3.bnbvpm"))).click()
    except:
        ...

    for a in range (0,6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    Butik=soup.find('h2', attrs={'class':'Headingstyles__StyledH2-sc-r7tfy8-1 cJhDBd'}).text

    for a in soup.find_all(attrs='Productstyles__StyledProduct-sc-16nua0l-0 aRuiG'):
        titel=a.find(attrs={'class':'Productstyles__StyledProductName-sc-16nua0l-5 dqhhbm'}).text
        if '/' in titel:
            titel=titel.replace('/', ' eller ')
            Produkter.append(titel)
        else:
            Produkter.append(titel)

        try:
            marke=a.find('span', attrs={'class':'Productstyles__StyledProductManufacturerBrand-sc-16nua0l-7 hnYIHY'})
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
        
        temp_info=(a.find(attrs={'class':'Productstyles__StyledProductDisplayVolume-sc-16nua0l-8 eyLzNX'})).text
        extraData.append(temp_info)

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
                price3=price3.replace('\n', '').strip()
                price=price3+" "+price
        except:
            price3=0
        
        Pris.append(price)

        if 'för' in price:
            price2=price.replace('för', '/').strip()
            temp4=price2.split('/')
            temp4[1]=temp4[1].replace(':00', '')
            tal1=int(temp4[0])
            tal2=int(temp4[1])
            jamfortPris_st.append(tal2/tal1)
        else:
            pris_temp=price.replace(':', '.')
            jamfortPris_st.append((pris_temp))
    
        prisPerEnhet=(a.find('span', attrs={'class':'Productstyles__StyledProductDisplayVolume-sc-16nua0l-8 eyLzNX'})).text
        flag=0
        
        try:
            if 'x' in prisPerEnhet:
                temp=prisPerEnhet
                temp1=prisPerEnhet.split('x')
                tal1=temp1[0]
                tal2=temp1[1]
                if 'g' in tal2:
                    temp4 = 'g'
                    tal2=tal2.replace('g','')
                elif 'ml' in tal2:
                    temp4 = 'ml'
                    tal2=tal2.replace('ml','')
                elif 'l' in tal2:
                    temp4 = 'l'
                    tal2=tal2.replace('l','')
                elif 'kg' in tal2:
                    temp4 = 'kg'
                    tal2=tal2.replace('kg','')

                nyMangd= str((int(tal1)*int(tal2)))+temp4
                try:
                    prisPerEnhet=prisPerEnhet.replace(temp,nyMangd)
                except:
                    print()
            if '•' in prisPerEnhet:
                temp1=prisPerEnhet.split('•')
                prisPerEnhet=temp1[1].strip()
            if '-' in prisPerEnhet:
                temp1=prisPerEnhet.split('-')
                prisPerEnhet=temp1[1].strip()
            if 'I lösvikt' in prisPerEnhet:
                jamfortPris_L.append("information saknas")
                jamfortPris_kg.append("information saknas")
                flag=1
            if 'Ca' in prisPerEnhet:
                prisPerEnhet=prisPerEnhet.replace('Ca', '').strip()    
            if 'Från' in prisPerEnhet:
                prisPerEnhet=prisPerEnhet.replace('Från', '').strip()   
            
            
            if 'p/' in prisPerEnhet:
                if 'cl' in prisPerEnhet:
                    temp=prisPerEnhet.replace('cl', '')
                elif 'L' in prisPerEnhet:
                    temp=prisPerEnhet.replace('L', '')
                temp1=temp.split('/')
                tal1=temp1[0].replace('p','')
                tal2=temp1[1]
                nyMangd= str((int(tal1)*int(tal2)))
                prisPerEnhet=prisPerEnhet.replace(temp,nyMangd)
            elif '/' in prisPerEnhet:
                temp1=prisPerEnhet.split('/')
                prisPerEnhet=temp1[1]

            if 'kg' in prisPerEnhet:
                temp4=string_to_decimal(prisPerEnhet)
                prisKilo(temp4, int(price1))
                flag=1

            elif ('g' in prisPerEnhet):
                temp_vikt=prisPerEnhet.replace('g', '')
                temp_vikt2=gram_to_kg(temp_vikt)
                prisKilo(temp_vikt2, int(price1))
                flag=1

            if 'ml' in prisPerEnhet:
                temp_volym1=prisPerEnhet.replace('ml', '')
                temp_volym=gram_to_kg(temp_volym1)
                prisLit(temp_volym, int(price1))
                flag=1

            elif 'dl' in prisPerEnhet:
                temp_volym1=prisPerEnhet.replace('dl', '')
                if ',' in temp_volym1:
                    temp_volym1=temp_volym1.replace(',', '')
                temp_volym=int(round(float(temp_volym1)))/10
                prisLit(temp_volym, int(price1))
                flag=1
            
            elif 'cl' in prisPerEnhet:
                temp_volym1=prisPerEnhet.replace('cl', '')
                if ',' in temp_volym1:
                    temp_volym1=temp_volym1.replace(',', '')
                temp_volym=int(round(float(temp_volym1)))/1000
                prisLit(temp_volym, int(price1))
                flag=1

            elif 'L' in prisPerEnhet:
                temp4=string_to_decimal(prisPerEnhet)
                prisLit(temp4, int(price1))
                flag=1

            if flag==0:
                deny()
        except:
            deny()


    for y in range(len(soup.find_all(attrs='Productstyles__StyledProduct-sc-16nua0l-0 aRuiG'))):

        data = {
            "Märke/ursprung": Marken[y],
            "Övrig information": extraData[y],
            "Pris": Pris[y],
            "Kategori": Kategori[y],
            "Giltig start": giltigStart,
            "Giltig slut": giltigSlut,
            "Jämfört pris(st)": jamfortPris_st[y],
            "Jämfört pris(kg)": jamfortPris_kg[y],
            "Jämfört pris(lit)": jamfortPris_L[y],
            "Nyckelord": keyWord[y],
        }

        def save1(collection_id1,document_id1,collection_id, document_id, data):
            db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
                
        save1(          
            collection_id1="Aktiva erbj.",
            document_id1 ="Willys",
            collection_id= Butik,
            document_id =Produkter[y],
            data = data
        )




        