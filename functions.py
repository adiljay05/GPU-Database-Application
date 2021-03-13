from google.cloud import datastore
import os
from google.auth.transport import requests
from holder_classes import GPU_info
from flask import Flask, render_template, request,redirect


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jawad1.json"

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