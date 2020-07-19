

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


