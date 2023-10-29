import torch
import numpy as np
import requests
import random
import http.client

MILVUS_HOST = 'https://in03-e0632cb9ccac3a4.api.gcp-us-west1.zillizcloud.com'
MILVUS_PORT = '19530'
MILVUS_COLLECTION = 'mentalmaps'

class milvus:

    def __init__(self):
        self.ID = 0
        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers['Authorization'] = 'Bearer 9a481fbef6077a066e52d63c4186bbfa0a65f742f5e66b05f393b7a25101a6e6fcf879c81d187de14942bea8dd8e7dc5dc6dda62'

    def store_embeddings(self, embeddingsList):
        numpy_embeddings = [embedding.detach().numpy() for embedding in embeddingsList]
        list_embeddings = [array.tolist() for array in numpy_embeddings]

        for embedding in list_embeddings:
            conn = http.client.HTTPSConnection("in03-e0632cb9ccac3a4.api.gcp-us-west1.zillizcloud.com")
            payload = "{\"collectionName\":\"mentalmaps\",\"data\":[{\"vector\":" + str(embedding) + "}]"
            headers = {
                'Authorization': "Bearer 9a481fbef6077a066e52d63c4186bbfa0a65f742f5e66b05f393b7a25101a6e6fcf879c81d187de14942bea8dd8e7dc5dc6dda62",
                'Accept': "application/json"
            }
            conn.request("POST", "/v1/vector/insert", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

        return None

    # def fetch_specific(id):
    #     host = MILVUS_HOST + '/v1/vector/query'
    #     data = [
    #         {
    #             f"filter": "id in [{id}]"
    #         }
    #     ]

    #     try:
    #         response = requests.post(host, headers=headers, json=data)
    #         print("Success")
    #         return response.data.title_vector
    #     except requests.exceptions.RequestException as e:
    #         print("Request error")
    #         return None

    # def fetch_all():
    #     host = MILVUS_HOST + '/v1/vector/query'
    #     valid_ids = [i for i in range(ID)]
    #     data = [
    #         {
    #             f"filter": "id in {valid_ids}"
    #         }
    #     ]

    #     try:
    #         response = requests.post(host, headers=headers, json=data)
    #         print("Success")
    #         return response.data.title_vector
    #     except requests.exceptions.RequestException as e:
    #         print("Request error")
    #         return None

    # def delete_all():
    #     host = MILVUS_HOST + '/v1/vector/delete'
    #     valid_ids = [i for i in range(ID)]
    #     data = [
    #         {
    #             f"id": "id in {valid_ids}"
    #         }
    #     ]
    #     ID = 0

    #     try:
    #         response = requests.post(host, headers=headers, json=data)
    #         print("Success")
    #         return response.data
    #     except requests.exceptions.RequestException as e:
    #         print("Request error")
    #         return None
