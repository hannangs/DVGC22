
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import xlrd

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

Produkter=[]
Kategorier=[]

workbook = xlrd.open_workbook("E:\OneDrive\Skrivbord\Matprodukter3.xlsx")
worksheet = workbook.sheet_by_index(0)
for i in range(2, 889):
    for j in range(0, 1):
        if '/' in worksheet.cell_value(i, 0):
            temp=worksheet.cell_value(i, 0)
            temp=temp.replace('/', ' ')
            Produkter.append(temp)
        else:
            Produkter.append(worksheet.cell_value(i, 0))
    for j in range(1, 2):
        Kategorier.append(worksheet.cell_value(i, 1))

for i in range (1,len(Produkter)):
    data = {
        "Kategori":Kategorier[i],
    }

    def save(collection_id1,document_id1, data):
        db.collection(collection_id1).document(document_id1).set(data)

    save(          
        collection_id1="Nyckelord",
        document_id1 =Produkter[i],
        data = data
    )