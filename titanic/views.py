from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from urllib.request import *
import simplejson
from django.conf import settings
from django.contrib import messages
import pysolr

"""
This function is for initiatiing solr instance
"""
def solrInitialization():
    solr_url = settings.SOLR_BASE_URL + settings.SOLR_CORE
    #connect to Solr Apache: # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr(solr_url , always_commit=True,)
    return solr

def home(request):
    query_search = request.GET.get('name')
    sex = request.GET.get('sex',None)
    f_sex = '' if sex == None else sex

   # Create a client instance. The timeout and authentication options are not required.
    # solr = pysolr.Solr('http://localhost:8983/solr/solrTrain', always_commit=True,)
    solr = solrInitialization()
    # Note that auto_commit defaults to False for performance. You can set
    # `auto_commit=True` to have commands always update the index immediately, make
    # an update call with `commit=True`, or use Solr's `autoCommit` / `commitWithin`
    # to have your data be committed following a particular policy.

    # Do a health check.
    solr.ping()
    print("solar conected")
    # Later, searching is easy. In the simple case, just a plain Lucene-style
    # # query is fine.
    # results = solr.search('*')
    query = '*' if not query_search else query_search 
   
    results  = solr.search(query, **{
    'start' : 0,
    'rows': 20,
    'fq' : '' if sex == None else 'Sex:' + f_sex , # fl is filter quere
    # 'fl' : 'id Name Age Sex', # Filter List
        })
   
    # results = solr.search('Sex:male and orange')
    print("================New result===================")
    records = setData(results)
    context = {'titanicData' : records['titanic'],'retailData':records['retail']}
    return render(request, 'data.html', context)
    # return render(request, 'home.html', context)
    

"""
Format data so that we can use in web page
"""
def setData(results):

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
            row['InvoiceNo'] = result['InvoiceNo']
            row['StockCode'] = result['StockCode']
            row['Description'] = result['Description']
            row['Quantity'] = result['Quantity']
            row['InvoiceDate'] = result['InvoiceDate']
            row['UnitPrice'] = result['UnitPrice']
            row['CustomerID'] = result['CustomerID']
            row['Country'] = result['Country']
            row['id'] = result['id']
            retailList.append(row)


    records['titanic'] = titanicList
    records['retail'] = retailList
    return records


"""
Remove Record From Solr Apache
"""
def solrDelete(request,rowId):
    solr = solrInitialization()
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
    solr = solrInitialization()
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





# def home2(request):
#     context = {}
#     print("===================khan=================")
#     # conn = urlopen('http://localhost:8983/solr/myfilms/select?q=*&wt=json')
#     conn = urlopen('http://localhost:8983/solr/titanic10/select?q=Sex:female&wt=json&start=2&rows=5')
#     rsp = simplejson.load(conn)
#     print(rsp)
#     return render(request, 'home.html', context)

    
