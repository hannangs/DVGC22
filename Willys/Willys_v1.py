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
    driver.set_window_size(1920, 1080)
    driver.get(URL)
    content = driver.page_source
    
    Produkter=[]
    extraData=[]
    Pris=[]
    giltighetsdatum="Giltigt 2022-09-12 till 2022-09-18."

    driver.get('%s' % URL)

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".banner-actions-container"))).click()
    except:
        print("No cookie?") 

    soup = BeautifulSoup(content, features="html.parser")
    Butik=soup.find('h1', attrs={'class':'store-heading'}).text