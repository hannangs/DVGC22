from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

Datum=datetime.today().strftime('%Y-%m-%d')
giltigStart = datetime.now()
tidBer = timedelta(days=6)
giltigSlut = giltigStart + tidBer

URL = "https://www.ica.se/butiker/maxi/karlstad/maxi-ica-stormarknad-karlstad-11010/erbjudanden/"
driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
driver.set_window_size(1920, 1080)
driver.get(URL)
content = driver.page_source

Produkter=[]
extraData=[]
Pris=[]
Kategori=[]
jamfortPris_st=[]
jamfortPris_kg=[]
jamfortPris_L=[]
data=[]
giltighetsdatum="Giltigt 2022-09-12 till 2022-09-18."

driver.get('%s' % URL)

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".banner-actions-container"))).click()
except:
    print("No cookie?") 

soup = BeautifulSoup(content, features="html.parser")
Butik=soup.find('h1', attrs={'class':'store-heading'}).text

def deny():
    jamfortPris_kg.append("Data saknas")
    jamfortPris_L.append("Data saknas")

def prisKoll(info_temp0):
    if '/kg.' in info_temp0: #'Jfr pris 58:00-82:86/kg.'
        if '-' in info_temp0:
            info_temp3=info_temp0.split('-')
            info_temp4=info_temp3[1].replace('/kg.', '')
            info_temp5=info_temp4.replace(':', '.').strip()
            jamfortPris_kg.append(info_temp5)
            jamfortPris_L.append("Data saknas")
        else:
            info_temp3=info_temp0.replace('Jfr pris', '')
            info_temp4=info_temp3.replace('/kg.', '')
            info_temp5=info_temp4.replace(':', '.').strip()
            jamfortPris_kg.append(info_temp5)
    elif '/liter.' in info_temp0: #'Jfr pris 42:45/kg, 39:47-45:00/liter, 22:50-28:12/liter drickklar.' 
        if '-' in info_temp0:
            info_temp3=info_temp0.split('-')
            info_temp4=info_temp3[1].replace('/liter.', '')
            info_temp5=info_temp4.replace(':', '.').strip()
            jamfortPris_kg.append(info_temp5)
            jamfortPris_L.append("Data saknas")
        else:
            info_temp3=info_temp0.replace('Jfr pris', '')
            info_temp4=info_temp3.replace('/liter.', '')
            info_temp5=info_temp4.replace(':', '.').strip()
            jamfortPris_L.append(info_temp5)
            jamfortPris_kg.append("Data saknas")
    else:
        deny()

test=(soup.find_all('div', class_='product-info-wrapper'))
for a in soup.find_all('div', class_='product-info-wrapper'):
    temp_prisinfo=a.text
    info_temp=temp_prisinfo.split('\n')
    while '' in info_temp:
        info_temp.remove('')

    if(len(info_temp)<=5):
        data.append('/st')    
    elif(len(info_temp)==6):
        if '/kg' in info_temp[3] or '/liter.' in info_temp[3]:
            info_temp2=info_temp[3]
            prisKoll(info_temp2)
        else:
            deny()  

    elif(len(info_temp)==9):
        if '/kg' in info_temp[6] or '/liter.' in info_temp[6]:
            info_temp2=info_temp[6]
            prisKoll(info_temp2)
        else:
            deny()

    elif(len(info_temp)==10):
        if '/kg' in info_temp[7] or '/liter.' in info_temp[7]:
            info_temp2=info_temp[7]
            prisKoll(info_temp2)
        else:
            deny()

    elif(len(info_temp)==11):
        if '/kg' in info_temp[8] or '/liter.' in info_temp[8]:
                info_temp2=info_temp[8]
                prisKoll(info_temp2)
        else:
            deny()
    
    elif(len(info_temp)==12):
        if '/kg' in info_temp[9] or '/liter.' in info_temp[9]:
            info_temp2=info_temp[9]
            prisKoll(info_temp2)
        else:
            deny()
    
    elif(len(info_temp)==13):
        if '/kg' in info_temp[10] or '/liter.' in info_temp[10]:
            info_temp2=info_temp[10]
            prisKoll(info_temp2)
        else:
            deny()
    
    elif(len(info_temp)==14):
        if '/kg' in info_temp[11] or '/liter.' in info_temp[11]:
            info_temp2=info_temp[11]
            prisKoll(info_temp2)
    else:
        deny()

