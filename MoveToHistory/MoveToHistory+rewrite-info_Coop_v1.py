#-*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

Produkter=[]
Marken=[]
Pris=[]
jamfortPris_st=[]
jamfortPris_kg=[]
jamfortPris_L=[]
Kategori=[]
info=[]
temp3=[]
giltigStart="2022-09-12"
giltigSlut="2022-09-18"
Butik="Coop City Karlstad"
#Datum=datetime.today().strftime('%Y-%m-%d')
Datum="2022-09-12"

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

doc_ref = db.collection(u'Coop City Karlstad')
doc = doc_ref.get()
doc_ref2 = db.collection(u'Nyckelord')
doc2 = doc_ref2.get()

for docs in doc:
    Produkt=docs.id
    Titlar=list(docs._data.keys())
    Data=list(docs._data.values())
    Produkter.append(Produkt)

    valData='Övrig information'
    valPris='Pris'
    valMarken='Varumärke/ursprung'
    indData=Titlar.index(valData)
    indPris=Titlar.index(valPris)
    indMarken=Titlar.index(valMarken)

    info.append(Data[indData])
    Marken.append(Data[indMarken])
    Pris.append(Data[indPris])
    pris_temp=Data[indPris]
    info_temp=Data[indData]

    for word in doc2:
        if word.id in Produkt:
            temp=list(word._data.values())
            Kategori.append(temp[0])
        else:
            Kategori.append("Övrigt")

    if ' för ' in pris_temp:
        temp2=pris_temp.replace(' för ', '/')
        temp3=temp2.replace(':-', '')
        temp4=temp3.split('/')
        tal1=int(temp4[0])
        tal2=int(temp4[1])
        jamfortPris_st.append(tal2/tal1)
    else:
        pris_temp=pris_temp.replace(':', '.')
        pris_temp=pris_temp.replace('-', '0')
        jamfortPris_st.append(int(float(pris_temp)))
    
    if '/kg' in info_temp:
        info_temp1=info_temp.split('.')
        info_temp1.pop()
        info_temp2=info_temp1[-1]
        info_temp3=info_temp2.replace('Jfr-pris', '')
        info_temp4=info_temp3.replace('/kg', '')
        info_temp5=info_temp4.replace(':', '.')
        info_temp=info_temp5.replace('-', '0').strip()
        jamfortPris_kg.append(info_temp)
    else:
        jamfortPris_kg.append("Data saknas")
    

    if '/lit' in info_temp:
        info_temp=info_temp.split('.')
        info_temp.pop()
        info_temp=info_temp[-1]
        info_temp=info_temp.replace('Jfr-pris', '')
        info_temp=info_temp.replace('/lit', '')
        info_temp=info_temp.replace(':', '.')
        info_temp=info_temp.replace('-', '0').strip()
        jamfortPris_L.append(info_temp)
    else:
        jamfortPris_L.append("Data saknas")


for i in range(len(Produkter)):

    data = {
        "Butik":Butik,
        "Varumärke/ursprung": Marken[i],
        "Övrig info":info[i],
        "Pris": Pris[i],
        "Jämfört pris(st)": jamfortPris_st[i],
        "Jämfört pris(/kg)": jamfortPris_kg[i],
        "Jämfört pris(/lit)": jamfortPris_L[i],
        "Kategori":Kategori[i],
        "Giltig start": giltigStart,
        "Giltig slut": giltigSlut,
    }

    db=firestore.client()

    def save(collection_id1,document_id1,collection_id, document_id, data):
        db.collection(collection_id1).document(document_id1).collection(collection_id).document(document_id).set(data)

    save(          
        collection_id1="Historik",
        document_id1 =Datum,
        collection_id= Butik,
        document_id =Produkter[i],
        data = data
    )