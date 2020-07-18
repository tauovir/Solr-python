from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from urllib.request import *
import simplejson
from django.conf import settings
from django.contrib import messages
import pysolr
from SolrClient import SolrClient
from titanic.solrSchema import SolrSchema,SolrCollection
from titanic import commonUtilities
import json 

"""
This function is for initiatiing solr instance
"""
def solrInitialization(collectionName):
    solr_url = settings.SOLR_BASE_URL + collectionName
    #connect to Solr Apache: # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr(solr_url , always_commit=True,)
    return solr

def home(request):
    query_search = request.GET.get('name')
    sex = request.GET.get('sex',None)
    sort_p = request.GET.get('sort',None)
    f_sex = '' if sex == None else sex
    age_sort = '' if sort_p == None else sort_p

   # Create a client instance. The timeout and authentication options are not required.
    # solr = pysolr.Solr('http://localhost:8983/solr/solrTrain', always_commit=True,)
    solr = solrInitialization(settings.SOLR_CORE)
    # Note that auto_commit defaults to False for performance. You can set
    # `auto_commit=True` to have commands always update the index immediately, make
    # an update call with `commit=True`, or use Solr's `autoCommit` / `commitWithin`
    # to have your data be committed following a particular policy.

    # Do a health check.
    solr.ping()
    print("solr conected")
    # Later, searching is easy. In the simple case, just a plain Lucene-style
    # # query is fine.
    # results = solr.search('*')
    query = '*' if not query_search else query_search 
   
    results  = solr.search(query, **{
    'start' : 0,
    'rows': 10,
    'fq' : '' if sex == None or sex == '' else 'Sex:' + f_sex , # fl is filter quere age_sort
    'sort' : '' if age_sort == None or age_sort == '' else 'Age ' + age_sort 
    # 'fl' : 'id Name Age Sex', # Filter List
        })
   
    # results = solr.search('Sex:male and orange')

    records = setData(results)
    context = {'titanicData' : records['titanic'],'retailData':records['retail']}
    return render(request, 'data.html', context)

    


def setData(results):
    """
        This function formates data so that we can use in web page
        Parameter:
        results(List):List of Dictionary
       
        Returns: 
        List:     List of Dictionary

    """
    records = {}
    retailList = []
    titanicList = []
    for result in results:
        row = {}
        if 'Cabin' in result:
            row['name'] = result['Name']
            row['sex'] = result['Sex']
            row['cabin'] = result['Cabin'] if 'Cabin' in result else 'c15'
            row['embarked'] = result['Embarked'] if 'Embarked' in result else 'C'
            row['age'] = int(result['Age']) if 'Age' in result else 30
            row['fare'] = result['Fare'] if 'Fare' in result else 300
            row['id'] = result['id']
            
            titanicList.append(row)
        elif 'InvoiceNo' in result:
            row['InvoiceNo'] = result['InvoiceNo'] if 'InvoiceNo' in result else '9999'
            row['StockCode'] = result['StockCode'] if 'StockCode' in result else '9999'
            row['Description'] = result['Description'] if 'Description' in result else 'Empty'
            row['Quantity'] = result['Quantity'] if 'Quantity' in result else 0
            row['InvoiceDate'] = result['InvoiceDate'] if 'InvoiceDate' in result else '01/01/1970'
            row['UnitPrice'] = result['UnitPrice'] if 'UnitPrice' in result else 0
            row['CustomerID'] = result['CustomerID'] if 'UnitPrice' in result else '9999'
            row['Country'] = result['Country'] if 'UnitPrice' in result else 'None'
            row['id'] = result['id']
            retailList.append(row)


    records['titanic'] = titanicList
    records['retail'] = retailList
    return records



def solrDelete(request,rowId):
    """
        This function is used to delete a row from a document
        Parameter:
        rowId(str): Unique Id of a row

    """
    solr = solrInitialization(settings.SOLR_CORE)
    solr.delete(id = rowId)
    # also in batches...
    #solr.delete(id=['doc_1', 'doc_2'])
    # ...or all documents.
    #solr.delete(q='*:*')
    return redirect('home')

"""
Save new record to Solr Apache
"""
def save(request):
    """
        This function Saves new record to Solr Apache
        Parameter:
        request(request Object): Holds various params
        Method: POST

    """
    solr = solrInitialization(settings.SOLR_CORE)
    data = {}
    data['Name']= request.POST.get('name','Blank')
    data['Sex']= request.POST.get('sex','male')
    data['Cabin'] = request.POST.get('cabin','C25')
    data['Embarked'] = request.POST.get('embarked','S')
    data['Age'] = request.POST.get('age',20)
    data['Fare'] = request.POST.get('fare',None)
    solr.add([data])
    messages.add_message(request, messages.SUCCESS, 'New record added to Solr')
    return redirect('home')



def migrate(request):
    import pandas as pd
    filePath = settings.BASE_DIR + "/solrTrain.csv"
    data = pd.read_csv(filePath)
    data.drop(data.columns[0], axis=1,inplace = True)
    records = data.values
    titanicData = []
    for result in records:
        row = {}
        row['Name'] = result[0]
        row['Sex'] = result[1]
        row['Age'] = (result[2])
        row['Fare'] = result[3]
        row['Cabin'] = result[4]
        row['Embarked'] = result[5]
        titanicData.append(row)

    solr = solrInitialization('Garden') # Initiate Core Instance
    #connect to Solr Apache: # Create a client instance. The timeout and authentication options are not required.
    # First remove All Data then index it
    # solr.delete(q='*:*')
    print("=================Migrate Data=============")
    # print(titanicData)
    solr.add(titanicData)
   
    return redirect('home')   



def createSchema(request):
    import json 
    dict1 = {}
    # Create Collection
    print("Create New Collection")
    colc = SolrCollection(settings.SOLR_BASE_URL)
    # response = colc.createCollection(name = 'freshCollection',numShards = 2,shards = 'shared101,shared102')
     # response = colc.reloadCollection(name = 'khanCloud')
    
    # After Creating Collectiion Create Schema
    
    solrSchema = SolrSchema(settings.SOLR_BASE_URL,'freshCollection')
    # schemaData = getPrepareData()
    # response = solrSchema.addFields(schemaData)
    response = solrSchema.getFieldLists()
    print("=============================Response================================")
    print(json.loads(response.content))

    print("==========================Response End==================") #getPrepareData
    return redirect('home')  


def createSchema2(request):
    import json 
    dict1 = {}
    solrSchema = SolrSchema(settings.SOLR_BASE_URL, settings.SOLR_CORE)
    # print("===================Create Schema==============")
    # response = createField() #createField()
    # print("==================Add Fields================")
    # fields = {'name':'mango30','type':'text_general','stored':True}
    # response = solrSchema.addFields(fields)
    # print("==================Replace Fields================")
    # fields = {'name':'mango30','type':'pfloat','stored':True,'multiValued':True}
    # response = solrSchema.replaceField(fields)

    # print("==================Add Copy Fields================")
    # fields = {'source':'khanishere22','dest':'location'}
    # response = solrSchema.deleteCopyField(fields)
    # response = solrSchema.retrieveEntrireSchema()
    # # dict1['name'] = 'mango30'
    # # response = solrSchema.deleteSingleFiled(dict1)
    # records = json.loads(response.content)
    # responseHeader = records['responseHeader']
    # schema = records['schema']
    # print(schema['fields'])
    
    # response = solrSchema.getFieldLists(fl = 'CompanyTag,khanAge',wt = 'xml')
    # response = solrSchema.getDynamicFieldLists(fieldName = '*_i')
    # response = solrSchema.getCopyFields()
    # response = solrSchema.getSchemaName()
    #=====================================================Collection=====================
    colc = SolrCollection(settings.SOLR_BASE_URL)
    # response = colc.createCollection(name = 'khanCloud',numShards = 2,shards = 'shared101,shared102')
    # response = colc.reloadCollection(name = 'khanCloud')
    
    # response = colc.getCollectionList()renameCollection
    # response = colc.renameCollection(name='khanCloud',target='shipCloude')
    # response = colc.renameCollection.__doc__ 
    # response = solrSchema.addFields.__doc__ 
    # help(SolrSchema) # # to access Class docstring 
    # help(SolrSchema.addFields) # # to access Class docstring 
    
    # print((response))
    # print(response.content)

    print("==========================Response End==================")
    return redirect('home')  


def createField():
        import requests
        url = "http://localhost:8983/solr/dataFromClient/schema"

        # payload = "{\"add-field\":{\"name\":\"khanishere\",\"type\":\"text_general\",\"stored\":true }}"
        headers = {
        'Content-type': 'application/json'
        }
        # payload = "{'add-field':[{'name':'OrgTag','type':'text_general','stored':True },{'name':'CompanyTag','type':'text_general','stored':True }]}"
        fieldList = []
        dict1 = {}
        add_field = {}
        dict1['name'] = 'color_name'
        dict1['type'] = 'text_general'
        dict1['stored'] = True
        fieldList.append(dict1)
        dict1 = {}
        dict1['name'] = 'animal_name'
        dict1['type'] = 'text_general'
        dict1['stored'] = True

        add_field['add-field'] = dict1
        print("Filed list")
        print(dict1)
        import json
        json_object = json.dumps(add_field)   
        print(json_object)
    
        response = requests.request("POST", url, headers=headers, data = json_object)

        # print(response.text.encode('utf8'))
        return response
        # return 0
        # print(response.text.encode('utf8'))



def getEntireSchema(request):
    """
        This function return entire schema of a collection
        Parameter:
        request(object):Http request parameter which hold query params
        Method :      Get
        Returns: 
        jsonObject:     Return a json response.

    """
    contex = {}
    print("Get Entire Eschema")
    format = request.GET.get('wt',None)
    formatType = 'json' if request.GET.get('wt',None) == None else request.GET.get('wt')
    collectionName = 'freshCollection' if request.GET.get('collection',None) == None else request.GET.get('collection')
   
    solrSchema = SolrSchema(settings.SOLR_BASE_URL,collectionName)
    response = solrSchema.getEntrireSchema(wt = formatType)
    contex['response'] = response
    contex['collections']= collectionLists()
    contex['default_collection']= 'freshCollection'
    
    return render(request, 'schema/schema.html', contex)

def collectionLists():
    """
        This function return a collection from cloude Server
        Parameter:
        
        Returns: 
        List :    List of Collection

    """
    colc = SolrCollection(settings.SOLR_BASE_URL)
    response = colc.getCollectionList()
    status= response['responseHeader']
    if status['status'] == 0:
        return response['collections']
    else:
        return ['error']
     

def fieldList(request):
    """
        This function return field List of a collection
        Parameter:
        request(object):Http request parameter which hold query params
        Method :      Get
        Returns: 
        jsonObject:     Return a json response.

    """
    context = {}
    collectionName = 'freshCollection' if request.GET.get('collection',None) == None else request.GET.get('collection')
    formatType = 'json' if request.GET.get('wt',None) == None else request.GET.get('wt')
    filedName = '' if request.GET.get('field',None) == None or request.GET.get('field') == '0' else request.GET.get('field')
    print("=================Field Name============")
    print(filedName)
    solrSchema = SolrSchema(settings.SOLR_BASE_URL,collectionName)
    response = solrSchema.getFieldLists(fieldName =filedName, wt = formatType)
    context['response'] = response
    context['collections']= collectionLists()
    context['fields']= commonUtilities.sampleFields()
    return render(request, 'schema/field-list.html', context)

def dynamicFieldList(request):
    """
        This function return Dynamic field List of a collection
        Parameter:
        request(object):Http request parameter which hold query params
        Method :      Get
        Returns: 
        JsonObject:     Return a json response.

    """
    context = {}
    collectionName = 'freshCollection' if request.GET.get('collection',None) == None else request.GET.get('collection')
    formatType = 'json' if request.GET.get('wt',None) == None else request.GET.get('wt')
    filedName = '' if request.GET.get('field',None) == None or request.GET.get('field') == '0' else request.GET.get('field')
    print("=================Dynamic Field Name============")
    print(filedName)
    solrSchema = SolrSchema(settings.SOLR_BASE_URL,collectionName)
    response = solrSchema.getDynamicFieldLists(fieldName =filedName, wt = formatType)
    context['response'] = response
    context['collections']= collectionLists()
    context['fields']= commonUtilities.sampleDynamicFields()
    return render(request, 'schema/dynamic-list.html', context)

def copyFieldList(request):
    """
        This function return Copy field List of a collection
        Parameter:
        request(object):Http request parameter which hold query params
        Method :      Get
        Returns: 
        jsonObject:     Return a json response.

    """
    context = {}
    collectionName = 'freshCollection' if request.GET.get('collection',None) == None else request.GET.get('collection')
    formatType = 'json' if request.GET.get('wt',None) == None else request.GET.get('wt')
    filedName = '' if request.GET.get('field',None) == None or request.GET.get('field') == '0' else request.GET.get('field')
   
    solrSchema = SolrSchema(settings.SOLR_BASE_URL,collectionName)
    response = solrSchema.getCopyFields(wt = formatType)
    context['response'] = response
    context['collections']= collectionLists()
    return render(request, 'schema/copy-list.html', context)

def schemaName(request):
    """
        This function return Schema name of a collection
        Parameter:
        request(object):Http request parameter which hold query params
        Method :      Get
        Returns: 
        jsonObject:     Return a json response.

    """
    context = {}
    collectionName = 'freshCollection' if request.GET.get('collection',None) == None else request.GET.get('collection')
    formatType = 'json' if request.GET.get('wt',None) == None else request.GET.get('wt')

    solrSchema = SolrSchema(settings.SOLR_BASE_URL,collectionName)
    response = solrSchema.getSchemaName(wt = formatType)
    context['response'] = response
    context['collections']= collectionLists()
    return render(request, 'schema/schema_name.html', context)


def cloudCollection(request):
    """
        This function return list of collection
        Parameter:
        request(object):Http request parameter which hold query params
        Method :      Get
        Returns: 
        Dictionary:     Return a dictionary response.

    """
    context = {}
    context['collections']= collectionLists()
    return render(request, 'collection/collection-list.html', context)

def createCollection(request):
    """
        This function is used to create collection
        Parameter:

        name    :   Collection name
        nshard  :   Number of Shards
        shard_name :    Shard names
        replica    :    Number of replicas

        Method :      PoST

    """
    colc = SolrCollection(settings.SOLR_BASE_URL)
    c_name= request.POST.get('name')
    c_numShards= request.POST.get('nshard')
    c_shards= request.POST.get('shard_name')
    c_replicationFactor = request.POST.get('replica')
    
    response = colc.createCollection(name = c_name,numShards = c_numShards,shards = c_shards,replicationFactor = c_replicationFactor)
    messages.add_message(request, messages.SUCCESS, 'New Collection created')
    
    status= response['responseHeader']
    if status['status'] == 0:
         messages.add_message(request, messages.SUCCESS, 'New Collection created')
    else:
         messages.add_message(request, messages.ERROR, 'Error Occure')
    return redirect('collection')

def deleteCollection(request,name):
    """
        This function is used to delete a collection
        Parameter:
        name    :   Collection name
        Method :      GET

    """
    colc = SolrCollection(settings.SOLR_BASE_URL)
    response = colc.deleteCollection(name)
    return redirect('collection')
   


def getPrepareData():
    
        return [
        {
            "name":"Name","type":"text_general","multiValued":False,"stored":True
        },
        {
            "name":"Sex","type":"text_general","multiValued":False,"stored":True
        },
         {
            "name":"Cabin","type":"text_general","multiValued":False,"stored":True
        },
         {
            "name":"Embarked","type":"text_general","multiValued":False,"stored":True
        },
         {
            "name":"Age","type":"text_general","default":'0',"multiValued":False,"stored":True
        },
        {
            "name":"Fare","type":"text_general","default":'0',"multiValued":False,"stored":True
        },
        ]



# def home2(request):
#     context = {}
#     print("===================khan=================")
#     # conn = urlopen('http://localhost:8983/solr/myfilms/select?q=*&wt=json')
#     conn = urlopen('http://localhost:8983/solr/titanic10/select?q=Sex:female&wt=json&start=2&rows=5')
#     rsp = simplejson.load(conn)
#     print(rsp)
#     return render(request, 'home.html', context)

    
