
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

lista_butiker_coop=[u'Coop City', u'Coop Herrhagen', u'Coop Kronoparken', u'Coop Kroppkärr', u'Coop Norrstrand', u'Coop Råtorp', u'Coop Strand', u'Stora Coop Bergvik', u'Stora Coop Välsviken']
lista_butiker_ica=[ u'Maxi ICA Stormarknad Bergvik Karlstad', u'ICA Nära Kärnan', u'ICA Nära Viken', u'ICA Supermarket Fanfaren', u'ICA Supermarket Wallinders', u'Ica Kvantum Hammarö', u'Maxi ICA Stormarknad Välsviken']
lista_butiker_willys=[ u'Lidl Rattgatan', u'Lidl Östra Infarten']
lista_butiker_ldl=[ u'Willys Karlstad Bryggudden', u'Willys Karlstad']

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

for y in lista_butiker_coop:
    doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Coop').collection(lista_butiker_coop[y])
    doc_butik = doc_ref_butik.get()
    count=len(doc_butik)
    delete_collection(doc_ref_butik, count)

for y in lista_butiker_ica:
    doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Ica').collection(lista_butiker_ica[y])
    doc_butik = doc_ref_butik.get()
    count=len(doc_butik)
    delete_collection(doc_ref_butik, count)

for y in lista_butiker_willys:
    doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Willys').collection(lista_butiker_willys[y])
    doc_butik = doc_ref_butik.get()
    count=len(doc_butik)
    delete_collection(doc_ref_butik, count)

for y in lista_butiker_ldl:
    doc_ref_butik = db.collection(u'Aktiva erbj.').document(u'Lidl').collection(lista_butiker_ldl[y])
    doc_butik = doc_ref_butik.get()
    count=len(doc_butik)
    delete_collection(doc_ref_butik, count)


