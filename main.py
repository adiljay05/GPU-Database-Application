import datetime
from flask import Flask, render_template,session
from google.cloud import datastore
import google.oauth2.id_token
from flask import Flask, render_template, request,redirect
from google.auth.transport import requests
import functions
from holder_classes import GPU_info

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

@app.route('/add_gpu', methods=['POST','GET'])
def add_gpu():
    if request.method == 'GET':
        return root()
    return render_template('add_gpu.html')

@app.route('/add_gpu_to_datastore',methods = ['POST','GET'])
def add_gpu_to_datastore():
    if request.method == 'GET':
        return root()
    return functions.add_gpu_to_datastore()

@app.route('/show_details',methods = ['POST','GET'])
def show_details_of_GPU():
    if request.method == 'GET':
        return root()
    gpu_name = request.form['gpu_name']
    gpu_data = functions.get_gpu_by_name(gpu_name)
    return render_template('GPU_Details.html',gpu_data = gpu_data)

@app.route('/edit_gpu',methods = ['POST','GET'])
def edit_gpu():
    if request.method == 'GET':
        return root()
    gpu_name = request.form['gpu_name']
    entity_key = datastore_client.key('GPUInfo', gpu_name)
    gpu_data = functions.get_gpu_by_name(gpu_name)
    return render_template('edit_gpu.html',gpu_data = gpu_data)

@app.route('/update_details',methods = ['POST','GET'])
def update_details():
    if request.method == 'GET':
        return root()
    obj = GPU_info(request.form['name'],request.form['manufacturer'],request.form['issue_date'],request.form['geometryShader'],request.form['tesselationShader'],request.form['shaderInt16'],request.form['sparseBinding'],request.form['textureCompressionETC2'],request.form['vertexPipelineStoresAndAtomics'])
    old_name = request.form['old_name']
    obj1 = functions.get_gpu_by_name(old_name)
    # entity_key = datastore_client.key('GPUInfo', old_name)
    gpu_data = functions.get_specific_GPU(obj1.key)
    if functions.update_details(obj,old_name,gpu_data) == "ok":
        return render_template('edit_gpu.html',gpu_data = gpu_data)
    else:
        return render_template('error.html',error="Record Already Exists")

@app.route('/add_filters',methods=['POST','GET'])
def add_filters():
    if request.method == 'GET':
        return root()
    return functions.show_with_filters()


@app.route('/compare',methods=['POST','GET'])
def compare():
    if request.method == 'GET':
        return root()
    GPU_list1 = functions.get_all_gpus()
    GPU_list2 = functions.get_all_gpus()
    return render_template('compare.html',GPU_list1 = GPU_list1,GPU_list2 = GPU_list2)

@app.route('/comparison',methods=['POST','GET'])
def comparison():
    if request.method == 'GET':
        return root()
    # user_info = functions.get_user_data()
    gpu1 = request.form['gpu1']
    gpu2 = request.form['gpu2']
    gpu1_data = functions.get_gpu_by_name(gpu1)
    gpu2_data = functions.get_gpu_by_name(gpu2)
    return render_template('comparison.html',gpu1 = gpu1_data,gpu2 = gpu2_data)

@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    GPU_list = None
    filters = list()
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            session['name'] = claims['name']
            session['email'] = claims['email']
            user_info = functions.get_user_data()
            if user_info == None:
                functions.createUserInfo(claims)
            GPU_list = functions.get_all_gpus()
        except ValueError as exc:
            error_message = str(exc)
    else:
        session['name'] = None
        session['email'] = None
    return render_template('index.html', error_message=error_message,GPU_list = GPU_list,filters = filters)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)