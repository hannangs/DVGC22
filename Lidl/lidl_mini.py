from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

def prisKilo(vikt, pris):
    jamfortPris_kg.append(int(pris)/vikt)
    jamfortPris_L.append("information saknas")
    #print('vikt:', int(pris)/vikt)

def prisLit(volym, pris):
    jamfortPris_L.append(pris/volym)
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

URL='https://www.lidl.se/c/mandag-sondag/c4140'

driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
driver.get(URL)
content = driver.page_source

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
driver.get('%s' % URL)

time.sleep(2)
button=driver.find_element("xpath",'//*[@id="CybotCookiebotDialog"]/div/div[1]/button')
button.click()
time.sleep(2)

soup = BeautifulSoup(content, features="html.parser")

for a in soup.find_all('a', class_='ret-o-card__link nuc-a-anchor'):
    flag=0

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
        else:
            pris_temp=(price2+" "+price1)
    except:
        price2=""
    Pris.append(pris_temp)

    if 'FÖR:' in pris_temp:
        temp2=pris_temp.replace(' FÖR: ', '/')
        temp3=temp2.replace(':-', '')
        temp4=temp3.split('/')
        tal1=int(temp4[0])
        tal2=int(temp4[1])
        price1=tal2
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
        prisPerEnhet=prisPerEnhet.replace(temp3,str(int(tal1)*int(tal2)))

    if '–' in prisPerEnhet:
        temp1=prisPerEnhet.split('–')
        prisPerEnhet=temp1[1].strip()

    if '/kg' in prisPerEnhet:
        jamfortPris_kg.append(price1)
        jamfortPris_L.append('Information saknas')
        flag=1

    elif 'kg' in prisPerEnhet:
        temp4=string_to_decimal(prisPerEnhet)
        prisKilo(temp4, jmf_pris)
        flag=1

    elif ('g' in prisPerEnhet):
        temp_vikt=prisPerEnhet.replace('g', '')
        temp_vikt2=gram_to_kg(temp_vikt)
        prisKilo(temp_vikt2, int(jmf_pris))
        flag=1

    elif 'ml' in prisPerEnhet:
        temp_volym1=prisPerEnhet.replace('ml', '')
        temp_volym=gram_to_kg(temp_volym1)
        prisLit(temp_volym, jmf_pris)
        flag=1

    elif 'dl' in prisPerEnhet:
        temp_volym1=prisPerEnhet.replace('dl', '')
        if ',' in temp_volym1:
            temp_volym1=temp_volym1.replace(',', '')
        temp_volym=int(round(float(temp_volym1)))/10
        prisLit(temp_volym, jmf_pris)
        flag=1
    
    elif 'cl' in prisPerEnhet:
        temp_volym1=prisPerEnhet.replace('cl', '')
        if ',' in temp_volym1:
            temp_volym1=temp_volym1.replace(',', '')
        temp_volym=int(round(float(temp_volym1)))/1000
        prisLit(temp_volym, jmf_pris)
        flag=1

    elif 'lökar' in prisPerEnhet:
        jamfortPris_kg.append('Information saknas')
        jamfortPris_L.append('Information saknas')
        flag=1

    elif 'l' in prisPerEnhet:
        temp4=string_to_decimal(prisPerEnhet)
        prisLit(temp4, jmf_pris)
        flag=1
    else:
        jamfortPris_kg.append('Information saknas')
        jamfortPris_L.append('Information saknas')  

print("?")


    