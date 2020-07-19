
 
from django.conf import settings
import pandas as pd

def sampleFields():
    list1 = ['Name','Sex','Age']
    return list1

def sampleDynamicFields():
    list1 = ['*_d','*_ss','*__str']
    return list1


def sampleFieldTypesFloat():
    fieldType = {}
    fieldType['name'] = 'nzfloat'
    fieldType['class'] = 'solr.FloatPointField'
    fieldType['docValues'] = 'true'
    fieldType['multiValued'] = 'false'
    fieldType['stored'] = 'false'
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


def getSalesData():
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
        row['total_sqft'] = result[5]
        row['bath'] = int(result[6])
        row['balcony'] = int(result[7])
        row['price'] = result[8]
        salesData.append(row)
    return salesData[:51]

def getReatailData():
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
    return retailData[:51]
    

def titanicData():
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
    return titanicData[:51]