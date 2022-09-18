import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred=credentials.Certificate("groceryapp-b4d12-firebase-adminsdk-78m5u-b4190054f8.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

#/store list/Butik info/Coop/Coop City

#doc_ref = db.collection(u'store list').document(u'Butik info').collection(u'Coop')
#doc = doc_ref.get()

#docs = db.collection(u'store list').document(u'Butik info').collection(u'Coop').stream()

#if doc.exists:
#    Full_Name = str(doc.to_dict()['Länk erbj.'])
#    print(Full_Name)

#else:
#    print('No such document!')

#for doc in docs:
#    print(f'{doc.id} => {doc.to_dict()}')

docs = db.collection(u'vara1').stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

