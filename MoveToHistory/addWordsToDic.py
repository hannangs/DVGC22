from itertools import product
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import pandas as pd
import csv

df = pd.read_excel(r'E:\OneDrive\Skrivbord\Matprodukter2.xlsx')

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()


for row in df:
    db=firestore.client()

    kategori=row[1]

    data = {
        "Kategori":kategori,
    }

    def save(collection_id1,document_id1, data):
        db.collection(collection_id1).document(document_id1).set(data)

    save(          
        collection_id1="Nyckelord",
        document_id1 =row[0],
        data = data
    )