
 
from django.conf import settings
import pandas as pd

def sampleFields():
    list1 = ['Name','Sex','Age']
    return list1

def sampleDynamicFields():
    list1 = ['*_d','*_ss','*__str']
    return list1

def sampleCopyFields():
    copyField = {}
    # copyField['source'] = '*_t' # the following line will copy the contents of all incoming fields that match the wildcard pattern *_t to the text field
    copyField['source'] = '*' 
    copyField['dest'] = '_text_'
    return copyField

def sampleFieldTypesFloat():
    fieldType = {}
    fieldType['name'] = 'nzfloat'
    fieldType['class'] = 'solr.FloatPointField'
    fieldType['docValues'] = 'true'
    fieldType['multiValued'] = 'false'
    fieldType['stored'] = 'true'
    fieldType['indexed'] = 'false'
    return fieldType

def sampleFieldTypesFloat2():
    fieldType = {}
    fieldType['name'] = 'nzfloat2'
    fieldType['class'] = 'solr.FloatPointField'
    fieldType['docValues'] = 'true'
    fieldType['multiValued'] = 'false'
    fieldType['stored'] = 'false'
    fieldType['indexed'] = 'false'
    return fieldType

def sampleFieldTypeInt():
    fieldType = {}
    fieldType['name'] = 'nzint'
    fieldType['class'] = 'solr.IntPointField'
    fieldType['docValues'] = 'true'
    fieldType['multiValued'] = 'false'
    fieldType['stored'] = 'true'
    fieldType['indexed'] = 'false'
    return fieldType

def sampleFieldTypesText():
    fieldType = {}
    indexAnalyser = {}
    queryAnalyzer = {}
    
    fieldType['name'] = 'nzText'
    fieldType['class'] = 'solr.TextField'
    fieldType['positionIncrementGap'] = 100
    fieldType['multiValued'] = 'true'

    #=================Filtesr and tokenizer for Index type================
    index_token, index_filter = getIndexFilterToken()
    indexAnalyser['tokenizer'] = index_token
    indexAnalyser['filters'] = index_filter
    fieldType['indexAnalyzer'] = indexAnalyser
    #=================Filtesr and tokenizer for Index type================
    query_index_token, query_index_filter = getQueryFilterToken()
    queryAnalyzer['tokenizer'] = query_index_token
    queryAnalyzer['filters'] = query_index_filter
    fieldType['queryAnalyzer'] = indexAnalyser

    return fieldType

def getAllFieldsTypes():
    allFieldTypes = []
    text = sampleFieldTypesText()
    float1 = sampleFieldTypesFloat()
    float2 = sampleFieldTypesFloat2()
    int1 = sampleFieldTypeInt()
    allFieldTypes.append(text)
    allFieldTypes.append(float1)
    allFieldTypes.append(float2)
    allFieldTypes.append(int1)

    return allFieldTypes

    
   

    
def getIndexFilterToken():
    temp = {}
    filters = []
    tokenizer = {}
    temp['class'] = 'solr.StopFilterFactory'
    temp['words'] = 'stopwords.txt'
    temp['ignoreCase'] = 'true'
    filters.append(temp)
    temp = {}
    temp['class'] = 'solr.LowerCaseFilterFactory'
    filters.append(temp)
    tokenizer['class'] = 'solr.StandardTokenizerFactory'
    return tokenizer,filters

def getQueryFilterToken():
    temp = {}
    filters = []
    tokenizer = {}
    temp['class'] = 'solr.StopFilterFactory'
    temp['words'] = 'stopwords.txt'
    temp['ignoreCase'] = 'true'
    filters.append(temp)
    temp = {}
    temp['class'] = 'solr.SynonymGraphFilterFactory'
    temp['expand'] = 'true'
    temp['ignoreCase'] = 'true'
    temp['synonyms'] = 'synonyms.txt'
    filters.append(temp)
    temp = {}
    temp['class'] = 'solr.LowerCaseFilterFactory'
    filters.append(temp)
    tokenizer['class'] = 'solr.StandardTokenizerFactory'
    return tokenizer,filters


def getSalesData(flag = 1):
    filePath = settings.BASE_DIR + "/sales_data_13000.csv"
    data = pd.read_csv(filePath)
    data.drop(data.columns[0], axis=1,inplace = True)
    records = data.values
    salesData = []
    for result in records:
        row = {}
        row['area_type'] = result[0]
        row['availability'] = result[1]
        row['location'] = (result[2])
        row['size'] = result[3]
        row['society'] = result[4]
        row['total_sqft'] = total_sqft(result[5])
        row['bath'] = int(result[6])
        row['balcony'] = int(result[7])
        row['price'] = result[8]
        salesData.append(row)
    if flag == 1:
        return salesData
    else:
        return salesData[:51]

def total_sqft(string1):
    return string1.split('-')[0]

def getReatailData(flag = 1):
    filePath = settings.BASE_DIR + "/retail_data_5000.csv"
    data = pd.read_csv(filePath)
    data.drop(data.columns[0], axis=1,inplace = True)
    records = data.values
    retailData = []
    for result in records:
        row = {}
        row['InvoiceNo'] = result[0]
        row['StockCode'] = result[1]
        row['Description'] = (result[2])
        row['Quantity'] = result[3]
        row['InvoiceDate'] = result[4]
        row['UnitPrice'] = result[5]
        row['CustomerID'] = int(result[6])
        row['Country'] = result[7]
        retailData.append(row)
    if flag == 1:
        return retailData
    else:
        return retailData[:51]
    

def titanicData(flag = 1):
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
    if flag == 1:
        return titanicData
    else:
        return titanicData[:51]


def getTitanicFields():
    
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
            "name":"Age","type":"nzfloat"
        },
        {
            "name":"Fare","type":"nzfloat2"
        },
        ]

def getRetailFields():
    
        return [
        {
            "name":"InvoiceNo","type":"text_general","multiValued":False,"stored":True
        },
        {
            "name":"StockCode","type":"text_general","multiValued":False,"stored":True
        },
         {
            "name":"Description","type":"nzText","multiValued":False,"stored":True
        },
         {
            "name":"Quantity","type":"nzint","multiValued":False,"stored":True
        },
         {
            "name":"InvoiceDate","type":"text_general","multiValued":False,"stored":True
        },
        {
            "name":"UnitPrice","type":"nzfloat2"
        },
        {
            "name":"CustomerID","type":"nzint","multiValued":False,"stored":True
        },
        {
            "name":"Country","type":"text_general","multiValued":False,"stored":True
        },
        ]

def getSalesFields():
        return [
        {
            "name":"area_type","type":"nzText","multiValued":False,"stored":True
        },
        {
            "name":"availability","type":"text_general","multiValued":False,"stored":True
        },
         {
            "name":"location","type":"text_general","multiValued":False,"stored":True
        },
         {
            "name":"size","type":"nzText","multiValued":False,"stored":True
        },
         {
            "name":"society","type":"text_general","multiValued":False,"stored":True
        },
        {
            "name":"total_sqft","type":"text_general","multiValued":False,"stored":True
        },
        {
            "name":"bath","type":"nzint","multiValued":False,"stored":True
        },
        {
            "name":"balcony","type":"nzint","default":'0',"multiValued":False,"stored":True
        },
        {
            "name":"price","type":"nzfloat","default":'0',"multiValued":False,"stored":True
        },
        ]

def writeLog(data):
    filePath = settings.BASE_DIR + "/titanic/logFile/log.txt"
    file1 = open(filePath, 'a')  # append mode
    file1.writelines(data) 
    file1.close()  
