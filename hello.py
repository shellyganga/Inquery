from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('boilermake-8-project-firebase-adminsdk-n45vg-c326d22181.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

query_ref = db.collection(u'profdata')

app = Flask(__name__)
    
@app.route('/', methods = ['GET'])
def default():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def retrieve():
    returnData = {}
    docs = db.collection(u'profdata').stream()
    for doc in docs:
        if (u'researchArea' in doc.to_dict() and request.form[u'area'] in doc.to_dict()[u'researchArea']):
            print(f'{doc.id} => {doc.to_dict()}')
            returnData[doc.id] = doc.to_dict()
    return render_template('index.html', data = returnData)

if __name__ == '__main__':
    app.run(debug=True)
