import datetime
from flask import Flask, render_template
from google.cloud import datastore
import os
import google.oauth2.id_token
from flask import Flask, render_template, request,redirect
from google.auth.transport import requests
import functions
from holder_classes import GPU_info

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jawad1.json"

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

@app.route('/add_gpu', methods=['POST'])
def add_gpu():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    return render_template('add_gpu.html', user_data=user_info)

@app.route('/add_gpu_to_datastore',methods = ['POST'])
def add_gpu_to_datastore():
    obj = GPU_info(request.form['gpu_name'],request.form['manufacturer'],request.form['issue_date'],request.form['geometryShader'],request.form['tesselationShader'],request.form['shaderInt16'],request.form['sparseBinding'],request.form['textureCompressionETC2'],request.form['vertexPipelineStoresAndAtomics'])
    check = functions.add_GPU(obj)
    if check == "ok":
        return redirect("/")
    else:
        return render_template('error.html',error="Record Already Exists")

@app.route('/show_details',methods = ['POST'])
def show_details_of_GPU():
    gpu_name = request.form['gpu_name']
    entity_key = datastore_client.key('GPUInfo', gpu_name)
    gpu_data = functions.get_specific_GPU(entity_key)
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    return render_template('GPU_Details.html',user_data = user_info ,gpu_data = gpu_data)

@app.route('/edit_gpu',methods = ['POST'])
def edit_gpu():
    gpu_name = request.form['gpu_name']
    entity_key = datastore_client.key('GPUInfo', gpu_name)
    gpu_data = functions.get_specific_GPU(entity_key)
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    return render_template('edit_gpu.html',user_data = user_info ,gpu_data = gpu_data)

@app.route('/update_details',methods = ['POST'])
def update_details():
    obj = GPU_info(request.form['name'],request.form['manufacturer'],request.form['issue_date'],request.form['geometryShader'],request.form['tesselationShader'],request.form['shaderInt16'],request.form['sparseBinding'],request.form['textureCompressionETC2'],request.form['vertexPipelineStoresAndAtomics'])
    old_name = request.form['old_name']
    entity_key = datastore_client.key('GPUInfo', old_name)
    gpu_data = functions.get_specific_GPU(entity_key)
    functions.update_details(obj,old_name,gpu_data)
    return redirect('/')

@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_info = None
    addresses = None
    GPU_list = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            user_info = functions.retrieveUserInfo(claims)
            if user_info == None:
                functions.createUserInfo(claims)
            GPU_list = functions.get_all_gpus()
        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', user_data=user_info, error_message=error_message,GPU_list = GPU_list)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)