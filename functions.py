from google.cloud import datastore
import os
from google.auth.transport import requests
from holder_classes import GPU_info


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

