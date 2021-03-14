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

datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

def get_user_data():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    return functions.retrieveUserInfo(claims)

def retrieveUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])
    entity = datastore_client.get(entity_key)
    return entity

def createUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])
    print(claims)
    entity = datastore.Entity(key = entity_key)
    entity.update({
        'email': claims['email'],
        'name': claims['name']
    })
    datastore_client.put(entity)

def add_GPU(obj):
    entity_key = datastore_client.key('GPUInfo', obj.name)
    if get_specific_GPU(entity_key) == None:
        print("adding to db")
        entity = datastore.Entity(key = entity_key)
        entity.update({
            "name": obj.name,
            'manufacturer': obj.manufacturer,
            'issued_date': obj.issued_date,
            'geometryShader' : obj.geometryShader,
            'tesselationShader' : obj.tesselationShader,
            'shaderInt16' : obj.shaderInt16,
            'sparseBinding' : obj.sparseBinding,
            'textureCompressionETC2' : obj.textureCompressionETC2,
            'vertexPipelineStoresAndAtomics' : obj.vertexPipelineStoresAndAtomics,
        })
        datastore_client.put(entity)
        return "ok"
    else:
        print("record already exists")
        return "not_ok"

def get_specific_GPU(entity_key):
    return datastore_client.get(entity_key)

def get_gpu_by_name(name):
    query = datastore_client.query(kind='GPUInfo')
    query.add_filter('name','=',name)
    for i in query.fetch():
        return i

def get_all_gpus():
    query = datastore_client.query(kind='GPUInfo')
    return query.fetch()

def update_details(obj,old_name,gpu_data):
    gpu_data['name'] = obj.name
    gpu_data['manufacturer'] = obj.manufacturer
    gpu_data['issued_date'] = obj.issued_date
    gpu_data['geometryShader'] = obj.geometryShader
    gpu_data['tesselationShader'] = obj.tesselationShader
    gpu_data['shaderInt16'] = obj.shaderInt16
    gpu_data['sparseBinding'] = obj.sparseBinding
    gpu_data['textureCompressionETC2'] = obj.textureCompressionETC2
    gpu_data['vertexPipelineStoresAndAtomics'] = obj.vertexPipelineStoresAndAtomics
    datastore_client.put(gpu_data)

def with_filters():
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
    user_info = functions.get_user_data()
    error_message = "error while fetching relevant data"
    return render_template('index.html', user_data=user_info, error_message=error_message,GPU_list = GPU_list,filters = filters)

def add_gpu_to_datastore():
    obj = GPU_info(request.form['gpu_name'],request.form['manufacturer'],request.form['issue_date'],request.form['geometryShader'],request.form['tesselationShader'],request.form['shaderInt16'],request.form['sparseBinding'],request.form['textureCompressionETC2'],request.form['vertexPipelineStoresAndAtomics'])
    check = functions.add_GPU(obj)
    if check == "ok":
        return redirect("/")
    else:
        return render_template('error.html',error="Record Already Exists")