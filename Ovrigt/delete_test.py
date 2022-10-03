
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

lista_butiker_coop=['Coop City Karlstad', 'Coop Herrhagen', 'Coop Konsum Kronoparken', 'Coop Kroppkärr', 'Coop Norrstrand', 'Coop Råtorp', 'Coop Strand', 'Stora Coop Bergvik', 'Stora Coop Välsviken']
lista_butiker_ica=[ 'Maxi ICA Stormarknad Bergvik Karlstad', 'ICA Nära Kärnan', 'ICA Nära Viken', 'ICA Supermarket Fanfaren', 'ICA Supermarket Wallinders', 'ICA Kvantum Hammarö', 'Maxi ICA Stormarknad Välsviken','ICA Supermarket Hagahallen']
lista_butiker_lidl=[ 'Lidl Rattgatan', 'Lidl Östra Infarten']
lista_butiker_willys=[ 'Willys Karlstad Bryggudden', 'Willys Karlstad']

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        #print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

try:
    for y in lista_butiker_coop:
        doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Coop').collection(y)
        doc_butik = doc_ref_butik.get()
        count=len(doc_butik)
        if count !=0:
            delete_collection(doc_ref_butik, count)
except:
    print("Coop finns ej")

try:
    for y in lista_butiker_ica:
        doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'ICA').collection(y)
        doc_butik = doc_ref_butik.get()
        count=len(doc_butik)
        if count !=0:
            delete_collection(doc_ref_butik, count)
except:
    print("ICA finns ej")

try:
    for y in lista_butiker_willys:
        doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Willys').collection(y)
        doc_butik = doc_ref_butik.get()
        count=len(doc_butik)
        if count !=0:
            delete_collection(doc_ref_butik, count)
except:
    print("Wiilys finns ej")

try:
    for y in lista_butiker_lidl:
        doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Lidl').collection(y)
        doc_butik = doc_ref_butik.get()
        count=len(doc_butik)
        if count !=0:
            delete_collection(doc_ref_butik, count)
except:
    print("Lidl finns ej")

