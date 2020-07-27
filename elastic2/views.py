from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from urllib.request import *
import simplejson
from django.conf import settings
from django.contrib import messages
import json
import requests
import urllib
from datetime import datetime
from elasticsearch import Elasticsearch,helpers
from titanic import commonUtilities



def home(request):
   
    # saleData = commonUtilities.getSalesData()
    # with open('result.json', 'w') as fp:
    #     json.dump(saleData, fp)
    # print("======completed================")
    # data = get_data_from_file('result.json')
    # print(data)
    return render(request, 'elastic/index.html', {})

def createIndex(request):
    #by default we connect to localhost:9200
    elasticObj = Elasticsearch()
    print("Create index")
    # create an index in elasticsearch, ignore status code 400 (index already exists)
    response = elasticObj.indices.create(index='retail2', ignore=400)
    print(response)
    return redirect('elasic-home')


def insert(request):
    elasticObj = Elasticsearch()
    print("===============Insert==================")
    # create an index in elasticsearch, ignore status code 400 (index already exists)
    doc = {'author': 'kimchy','text': 'Elasticsearch: cool. bonsai cool.','timestamp': datetime.now(),}
    res = elasticObj.index(index="titanic2", doc_type = 'author',id=2, body=doc)
    print(res)
   
    return redirect('elasic-home')

def checkStatus(request):
    # Elastic is running
    print("Check Elastic is running")
    res = requests.get('http://localhost:9200')
    print(res.content)
    return redirect('elasic-home')


def get_data_from_file(file_name):
    filePath = settings.BASE_DIR + "/" + file_name
    file = open(filePath, encoding="utf8", errors='ignore')
    data = [line.strip() for line in file]
    file.close()
    return data
def setBulkjsonData(json_file,_index, doc_type):
    json_list = get_data_from_file(json_file)
    for doc in json_list:
        # use a `yield` generator so that the data
        # isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }




