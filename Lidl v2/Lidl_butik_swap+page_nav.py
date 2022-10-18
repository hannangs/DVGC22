from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

URL='https://www.lidl.se/'
adresser=[]
Butiker=[]
i=0

doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Lidl')
doc = doc_ref.get()
URL1 = []
URL2 = []
URL3 = []
URL4 = []
URL5 = []
URL6 = []

for docs in doc:
    Titlar=list(docs._data.keys())
    Data=list(docs._data.values())
    Butiker.append(docs.id)
    val='Adress'
    ind=Titlar.index(val)
    adresser.append(Data[ind])

for docs in doc:
    driver = webdriver.Chrome("E:\OneDrive\Skrivbord\chromedriver.exe")
    driver.set_window_size(1920, 1080)
    driver.get(URL)
    time.sleep(2)
    try:
        button=driver.find_element("xpath",'//*[@id="CybotCookiebotDialog"]/div/div[1]/button')
        button.click()
    except: 
        print()

    time.sleep(2)
    button1=driver.find_element("xpath",'/html/body/header/div[2]/header/div/div[3]/nav/ul/li[1]/a/span')
    button1.click()
    time.sleep(2)

    Serch_butik=driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div[1]/div/div/div/input')
    Serch_butik.send_keys(adresser[i])
    i=i+1

    time.sleep(2)
    button2=driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div[1]/div/button')
    button2.click()
    time.sleep(2)
    button3=driver.find_element("xpath",'/html/body/div[1]/div/div[3]/div[4]/ul/li[1]/button')
    button3.click()
    time.sleep(2)
    button4=driver.find_element("xpath",'/html/body/div[1]/div/div[4]/div[3]/div/div/label')
    button4.click()
    time.sleep(2)
    button5=driver.find_element("xpath",'/html/body/div[1]/div/div[7]/button')
    button5.click()
    time.sleep(2)

    #Måndag - Söndag
    time.sleep(2)
    button6=driver.find_element("xpath",'/html/body/div[2]/div/section[2]/div/ul/li[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/a')
    button6.click()
    time.sleep(2)
    get_url = driver.current_url
    URL5.append(get_url)

    #Måndag-Onsdag
    time.sleep(2)
    button7=driver.find_element("xpath",'//*[@id="pageMain"]/div/div[1]/section/div/ul/li[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div/a/span[2]')
    button7.click()
    time.sleep(2)
    get_url = driver.current_url
    URL1.append(get_url)

    #Torsdag - Söndag
    time.sleep(2)
    button8=driver.find_element("xpath",'//*[@id="pageMain"]/div/div[1]/section/div/ul/li[1]/div[2]/div/div/div[2]/div/div/div[3]/div/div/a/span[2]')
    button8.click()
    time.sleep(2)
    get_url = driver.current_url
    URL2.append(get_url)

    #Lördag - Söndag
    time.sleep(2)
    button9=driver.find_element("xpath",'//*[@id="pageMain"]/div/div[1]/section/div/ul/li[1]/div[2]/div/div/div[2]/div/div/div[6]/div/div/a/span[2]')
    button9.click()
    time.sleep(2)
    get_url = driver.current_url
    URL3.append(get_url)

    #Lidl priser
    time.sleep(2)
    button10=driver.find_element("xpath",'//*[@id="pageMain"]/div/div[1]/section/div/ul/li[1]/div[2]/div/div/div[2]/div/div/div[7]/div/div/a/span[2]')
    button10.click()
    time.sleep(2)
    get_url = driver.current_url
    URL4.append(get_url)

    #Lidl plus priser
    time.sleep(2)
    button10=driver.find_element("xpath",'/html/body/div[2]/div/div[1]/section/div/ul/li[1]/div[2]/div/div/div[2]/div/div/div[4]/div/div/a/span[2]')
    button10.click()
    time.sleep(2)
    get_url = driver.current_url
    URL6.append(get_url)

    driver.quit()

antalProdukter=len(adresser)
for y in range(antalProdukter):
    data1 = {
        "Adress": adresser[y],
        "Länk M-S": URL5[y],
        "Länk M-O": URL1[y],
        "Länk T-S": URL2[y],
        "Länk L-S": URL3[y],
        "Länk lidl": URL4[y],
        "Länk lidl plus": URL6[y],
    }

    def save1(collection_id1,document_id1,collection_id, document_id, data):
        db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)
            
    save1(          
        collection_id1="store list",
        document_id1 = "Butik info",
        collection_id= "Lidl",
        document_id = Butiker[y],
        data = data1,
    )

        





