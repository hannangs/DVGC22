from wsgiref.simple_server import demo_app
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

LankarErbjButik="https://www.willys.se/erbjudanden/butik?StoreID=2290"
URL = "https://www.willys.se/erbjudanden/butik?StoreID=2290"
driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
driver.get(URL)
Produkter=[]
extraData=[]
Pris=[]
Marken=[]
jamfortPris_st=[]
jamfortPris_kg=[]
jamfortPris_L=[]

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
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
except:
    print("ingen cookie")

soup = BeautifulSoup(driver.page_source, features="html.parser")
Butik=soup.find('h2', attrs={'class':'Headingstyles__StyledH2-sc-r7tfy8-1 cJhDBd'}).text

for a in soup.find_all(attrs='Productstyles__StyledProduct-sc-16nua0l-0 aRuiG'):
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
    temp_2="tom"

    if '•' in prisPerEnhet:
        temp1=prisPerEnhet.split('•')
        prisPerEnhet=temp1[1].strip()
    
    if '-' in prisPerEnhet:
        temp1=prisPerEnhet.split('-')

    if 'I lösvikt' in prisPerEnhet:
        print("I lösvikt")
    
    if 'Ca' in prisPerEnhet:
        prisPerEnhet=prisPerEnhet.replace('Ca', '').strip()
    
         
    if 'kg' in prisPerEnhet:
        temp4=string_to_decimal(prisPerEnhet)
        prisKilo(temp4, int(price1))

    elif 'g' in temp_2:
        temp11=temp_2.replace('g', '')
        temp12=gram_to_kg(temp11)
        prisKilo(temp12, int(price1))

    elif ('g' in prisPerEnhet):
        temp_vikt=prisPerEnhet.replace('g', '')
        temp_vikt2=gram_to_kg(temp_vikt)
        prisKilo(temp_vikt2, int(price1))

    if 'ml' in prisPerEnhet:
        temp_volym1=prisPerEnhet.replace('ml', '')
        temp_volym=gram_to_kg(temp_volym1)
        prisLit(temp_volym, int(price1))

    elif 'L' in prisPerEnhet:
        temp4=string_to_decimal(prisPerEnhet)
        prisLit(temp4, int(price1))                        

