import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
from time import sleep
cred = credentials.Certificate("Bear_sdk.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
doc_ref = db.collection(u'N')
doc = doc_ref.get()
if doc.exists:
    print(f'Document data: {doc.to_dict()}')
else:
    print(u'No such document!')

# Create an Event for notifying main thread.
callback_done = threading.Event()

boolValue = False

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    # for doc in doc_snapshot:
    #     Dict = doc.to_dict()
    #     Age = Dict['Age']
    #     print(f'Received document snapshot: {doc.id}, Age = {Age}')
    #     global boolValue
    #     boolValue = Age
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New city: {change.document.id}')
        elif change.type.name == 'MODIFIED':
            print(f'Modified city: {change.document.id}')
        elif change.type.name == 'REMOVED':
            print(f'Removed city: {change.document.id}')
    callback_done.set()



# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)



