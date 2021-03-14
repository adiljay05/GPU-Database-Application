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
    # print(request.form['geometryShader'])
    obj = GPU_info(request.form['gpu_name'],request.form['manufacturer'],request.form['issue_date'],request.form['geometryShader'],request.form['tesselationShader'],request.form['shaderInt16'],request.form['sparseBinding'],request.form['textureCompressionETC2'],request.form['vertexPipelineStoresAndAtomics'])
    check = functions.add_GPU(obj)
    if check == "ok":
        return redirect("/")
    else:
        return render_template('error.html',error="Record Already Exists")
    # return render_template('error.html',error="Record Already Exists")

@app.route('/show_details',methods = ['POST'])
def show_details_of_GPU():
    gpu_name = request.form['gpu_name']
    print(gpu_name)
    gpu_data = functions.get_gpu_by_name(gpu_name)
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
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    return render_template('edit_gpu.html',user_data = user_info ,gpu_data = gpu_data)

@app.route('/add_filters',methods=['POST'])
def add_filters():
    filters = list()
    geometryShader = request.form['geometryShader']
    tesselationShader = request.form['tesselationShader']
    shaderInt16 = request.form['shaderInt16']
    sparseBinding = request.form['sparseBinding']
    textureCompressionETC2 = request.form['textureCompressionETC2']
    vertexPipelineStoresAndAtomics = request.form['vertexPipelineStoresAndAtomics']
    query = datastore_client.query(kind='GPUInfo')
    if geometryShader != "":
        query.add_filter('geometryShader','=',geometryShader)
        filters.append(geometryShader)
    else:
        filters.append("")
    if tesselationShader!="":
        query.add_filter('tesselationShader','=',tesselationShader)
        filters.append(tesselationShader)
    else:
        filters.append("")
    if shaderInt16 != "":
        query.add_filter('shaderInt16','=',shaderInt16)
        filters.append(shaderInt16)
    else:
        filters.append("")
    if sparseBinding!="":
        query.add_filter('sparseBinding','=',sparseBinding)
        filters.append(sparseBinding)
    else:
        filters.append("")
    if textureCompressionETC2!="":
        query.add_filter('textureCompressionETC2','=',textureCompressionETC2)
        filters.append(textureCompressionETC2)
    else:
        filters.append("")
    if vertexPipelineStoresAndAtomics != "":
        query.add_filter('vertexPipelineStoresAndAtomics','=',vertexPipelineStoresAndAtomics)
        filters.append(vertexPipelineStoresAndAtomics)
    else:
        filters.append("")
    GPU_list = query.fetch()
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    error_message = "error while fetching relevant data"
    return render_template('index.html', user_data=user_info, error_message=error_message,GPU_list = GPU_list,filters = filters)


@app.route('/compare',methods=['POST'])
def compare():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    GPU_list1 = functions.get_all_gpus()
    GPU_list2 = functions.get_all_gpus()
    return render_template('compare.html',user_data=user_info,GPU_list1 = GPU_list1,GPU_list2 = GPU_list2)

@app.route('/comparison',methods=['POST'])
def comparison():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    user_info = functions.retrieveUserInfo(claims)
    gpu1 = request.form['gpu1']
    gpu2 = request.form['gpu2']
    gpu1_data = functions.get_gpu_by_name(gpu1)
    gpu2_data = functions.get_gpu_by_name(gpu2)
    return render_template('comparison.html',user_data=user_info,gpu1 = gpu1_data,gpu2 = gpu2_data)

@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_info = None
    addresses = None
    GPU_list = None
    filters = list()
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            user_info = functions.retrieveUserInfo(claims)
            if user_info == None:
                functions.createUserInfo(claims)
            GPU_list = functions.get_all_gpus()
        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', user_data=user_info, error_message=error_message,GPU_list = GPU_list,filters = filters)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)