import datetime
from flask import Flask, render_template
from google.cloud import datastore
import os
import google.oauth2.id_token
from flask import Flask, render_template, request,redirect
from google.auth.transport import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jawad1.json"

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

def retrieveUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])
    entity = datastore_client.get(entity_key)
    return entity

def createUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])
    entity = datastore.Entity(key = entity_key)
    entity.update({
    'email': claims['email'],
    'name': claims['name']
    })
    datastore_client.put(entity)

@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_info = None
    addresses = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            user_info = retrieveUserInfo(claims)
            if user_info == None:
                createUserInfo(claims)
        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', user_data=claims, error_message=error_message)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)