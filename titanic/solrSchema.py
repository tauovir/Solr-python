import json
import requests
import urllib

class SolrSchema:
    """ 
    This is a class for executing operation on Solr SChema.
      
    Attributes: 
        fullUrl (string): Complete Solr Url. 
        headers (dict): Header for Post request
        successCode (int): Sucess Status 
        errorCode (int): Error status
        response (dict): response
        field(dict) : Fields to be add/remove
    """

    fullUrl = ''
    headers = {
        'Content-type': 'application/json'
        }

    fieldRequiredKeys = ['name','type','index','stored']
    successCode = 200 # Success
    errorCode = 201 # error occur
    field = {}
    response = {'status':200,'message':''}

    def __init__(self,url,collectionName):
        """ 
        The constructor for Solr Url and  Collection/core. 
  
        Parameters: 
           real (string): The real part of complex number. 
           imag (string): The imaginary part of complex number.    
        """
        self.fullUrl = url + collectionName + '/schema'
        self.field = {}
    
  
    def addFields(self,dictionaryData):
        """
        This function takes a dictionary or a list of dictionary to add field defination inthe Solr Schema

        Parameters:
        dictionaryData(dict)/(List of dict) : add fields/ a field

        Returns: 
            JsonObject: return a json object.
        """
        # if not isinstance(dictionaryData, dict):
        #     return self.displayMessage(self.errorCode,'Data type should be Dictinary')
        if not dictionaryData:
            return self.displayMessage(self.errorCode,'Data is empty')

        self.field['add-field'] = dictionaryData
        payload = json.dumps(self.field)  
        print(payload)
        response = requests.request("POST", self.fullUrl, headers = self.headers, data = payload)
        return response
     
  
    def deleteSingleFiled(self,dictionaryData):
        """
        This function takes a dictionary to remove a field defination from  Solr Schema.

        Parameters:
        dictionaryData(dict) : delete a fields

        Returns: 
            JsonObject: return a json object.
        """
        if not isinstance(dictionaryData, dict):
            return self.displayMessage(self.errorCode,'Data type should be Dictinary')
        if not dictionaryData:
            return self.displayMessage(self.errorCode,'Data is empty')
        self.field['delete-field'] = dictionaryData
        payload = json.dumps(self.field)  
        print(payload)
        response = requests.request("POST", self.fullUrl, headers = self.headers, data = payload)
        return response

    """
    
    """
    def replaceField(self,dictionaryData):
        """
        TThis function is used to replace the defination of previous field.We must supply the full definition 
        for a field - this command will not partially modify a field’s definition.If the field does not exist in the schema an error is thrown.

        Parameters:
        dictionaryData(dict) : replace a fields

        Returns: 
            JsonObject: return a json object.
        """

        if not isinstance(dictionaryData, dict):
            return self.displayMessage(self.errorCode,'Data type should be Dictinary')
        if not dictionaryData:
            return self.displayMessage(self.errorCode,'Data is empty')

        self.field['replace-field'] = dictionaryData
        payload = json.dumps(self.field)  
        print(payload)
        response = requests.request("POST", self.fullUrl, headers = self.headers, data = payload)
        return response       
   
    def addCopyField(self,dictionaryData : dict): #requured param:,source,dest,maxChars
        """
        This function adds a new copy field rule to your schema.

        Parameters:
        dictionaryData(dict) : add copy fields

        Returns: 
            JsonObject: return a json object.
        """
        
        if not isinstance(dictionaryData, dict):
            return self.displayMessage(self.errorCode,'Data type should be Dictinary')
        if not dictionaryData:
            return self.displayMessage(self.errorCode,'Data is empty')

        self.field['add-copy-field'] = dictionaryData
        payload = json.dumps(self.field)  
        print(payload)
        response = requests.request("POST", self.fullUrl, headers = self.headers, data = payload)
        return response

   
    def deleteCopyField(self,dictionaryData : dict): #requured param:,source,dest,maxChars

        """
        This function deletes a copy field rule from your schema. If the copy field rule does not exist in the schema an error is thrown.
        The source and dest attributes are required by this command.
        Parameters:
        dictionaryData(dict) : delete copy fields

        Returns: 
            JsonObject: return a json object.

        """
        
        if not isinstance(dictionaryData, dict):
            return self.displayMessage(self.errorCode,'Data type should be Dictinary')
        if not dictionaryData:
            return self.displayMessage(self.errorCode,'Data is empty')

        self.field['add-copy-field'] = dictionaryData
        payload = json.dumps(self.field)  
        print(payload)
        response = requests.request("POST", self.fullUrl, headers = self.headers, data = payload)
        return response

    def retrieveEntrireSchema(self, wt = 'json'):
        """
        This function is used to get entire schema of a collection/core.
        Parameters:
        wt(string) :    return type(json,xml,schema.xml)

        Returns: 
            JsonObject/Xml/schema.xml: return a json/xml as per wt parameter.
        """
        response = requests.request("Get", self.fullUrl)
        return response

    
    def getFieldLists(self, fieldName = '',wt = 'json', fl = '',includeDynamic = 'false', showDefaults = 'false'):
        """
        This function is used to return FieldList or a field from schema defination.
        Supprted format: json, xml or schema.xml
        Parameters:
        wt(string) :    Defines the format of the response. The options are json or xml. If not specified, JSON will be returned by default.
        fl(string) :    Comma- or space-separated list of one or more fields to return. If not specified, all fields will be returned by default.
        includeDynamic(boolean) :    If true, and if the fl query parameter is specified or the fieldname path parameter is used, 
                                    matching dynamic fields are included in the response and identified with the dynamicBase property.
                                    If neither the fl query parameter nor the fieldname path parameter is specified, the includeDynamic query parameter is ignored.

                                    If false, the default, matching dynamic fields will not be returned.
        showDefaults(boolean) :     If true, all default field properties from each field’s field type will be included in the response 
                                    (e.g., tokenized for solr.TextField). If false, the default, only explicitly specified field properties will be included.
        Returns: 
            JsonObject: return a Json response.

        """
        args = {"wt": wt, "includeDynamic": includeDynamic,"showDefaults" : showDefaults}
        if fl != '':
            args['fl'] = fl

        if fieldName == '':
            response = requests.request("Get", self.fullUrl + "/fields?{}".format(urllib.parse.urlencode(args)))
        else:
            response = requests.request("Get", self.fullUrl + "/fields/"+fieldName)

        return response

    
    def getDynamicFieldLists(self, fieldName = '',wt = 'json',showDefaults='false'):

        """
        This function is used to return Dynamic FieldList or a field from schema defination.

        parameters:
        fieldName(string) : Field name to be retrieved
        wt(string):     Defines the format of the response. The options are json or xml. If not specified, JSON will be returned by default.
        showDefaults(boolean) :  If true, all default field properties from each dynamic field’s field type will be included in the response (
                                e.g., tokenized for solr.TextField). If false, the default, only explicitly specified field properties will be included.

        Returns: 
            JsonObject: return a Json response.

        """
        args = {"wt": wt,"showDefaults" : showDefaults}
        if fieldName == '':
            response = requests.request("Get", self.fullUrl + "/dynamicfields?{}".format(urllib.parse.urlencode(args)))
        else:
            response = requests.request("Get", self.fullUrl + "/dynamicfields/"+fieldName)
        return response

   
    def getCopyFields(self,wt = 'json',sourceFl = '',destinationFl = ''):
        """
        This Function is used to return copyField from Solr Schema.

        Parameters:
        wt(string):         Defines the format of the response. The options are json or xml. If not specified, JSON will be returned by default.
        sourceFl(string):   Comma- or space-separated list of one or more copyField source fields to include in the response - copyField directives with all 
                            other source fields will be excluded from the response. If not specified, all copyField-s will be included in the response.
        destinationFl(string):     Comma- or space-separated list of one or more copyField destination fields to include in the response. c
                                opyField directives with all other dest fields will be excluded. If not specified, all copyField-s will be included in the response.
        Returns: 
            JsonObject: return a Json response.

        """
        args = {"wt": wt}
        if sourceFl != '' and destinationFl != '':
            args['source.fl'] = sourceFl
            args['dest.fl'] = destinationFl
        response = requests.request("Get", self.fullUrl + "/copyfields?{}".format(urllib.parse.urlencode(args)))
        return response
    
    
    def getSchemaName(self, wt = 'json'):
        """
        This function return current Schema Name
        Parameter:

        wt(string):     Defines the format of the response. The options are json or xml. If not specified, JSON will be returned by default.

        Returns: 
        JsonObject: A Json Object which the name given to the schema.

        """
        args = {"wt": wt}
        response = requests.request("Get", self.fullUrl + "/name?{}".format(urllib.parse.urlencode(args)))
        return response

    
    def displayMessage(self,erroCode, message):
        """
        This function returns formated response
        Parameters:
        erroCode(int) : 200(Success) Or 2001(fail/error)
        message(string) : success or fail message
        Returns: 
        JsonObject: return a Json response.
        """
        self.response['status'] = erroCode
        self.response['message'] = message
        return self.response


class SolrCollection:
    def __init__(self,url):
        self.fullUrl = url + 'admin/collections'
    
    def createCollection(self,name, numShards,shards, replicationFactor = 1,wt = 'json'):
        """
        This function is used to create new collection;
        Parameters:
        name (string): The name of the collection to be created. This parameter is required.
        numShards(int) : The number of shards to be created as part of the collection. This is a required parameter when the router.name is compositeId.
        shards(String)  : A comma separated list of shard names, e.g., shard-x,shard-y,shard-z. This is a required parameter when the router.name is implicit.
        replicationFactor(int) : The number of replicas to be created for each shard. The default is 1.
        Returns: 
        JsonObject: A Json Object which contains Solr response 
        """
        args = {"action": 'CREATE','name':name,'numShards':numShards,'shards':shards,'replicationFactor':replicationFactor,'wt':wt}
        response = requests.request("Get", self.fullUrl + "?{}".format(urllib.parse.urlencode(args)))
        return response

    def reloadCollection(self, name, wt = 'json'):
        """
        The RELOAD action is used when you have changed a configuration in ZooKeeper.
        Parameters:
        name(string): The name of the collection to reload. This parameter is required.
        async : Request ID to track this action which will be processed asynchronously.
        Returns: 
        JsonObject: A Json Object which contains Solr response 
        """
        args = {"action": 'RELOAD','name':name,'wt':wt}
        response = requests.request("Get", self.fullUrl + "?{}".format(urllib.parse.urlencode(args)))
        return response

    def getCollectionList(self):
        """
        Fetch the names of the collections in the cluster.

        Returns: 
        JsonObject: A Json Object which contains Solr response 
        """

        args = {"action": 'LIST'}
        response = requests.request("Get", self.fullUrl + "?{}".format(urllib.parse.urlencode(args)))
        return response

    def renameCollection(self,name, target ):
        """
        Renaming a collection sets up a standard alias that points to the underlying collection, so that the same (unmodified) 
        collection can now be referred to in query, index and admin operations using the new name.
        Parameters:
        name(string) : Name of the existing SolrCloud collection or an alias that refers to exactly one collection and is not a Routed Alias.
                        Note:the existing name must be either a SolrCloud collection or a standard alias referring to a single collection. 
                        Aliases that refer to more than 1 collection are not supported.
                        The existing name must not be a Routed Alias.
                        The target name must not be an existing alias.
        target(string) : Target name of the collection. This will be the new alias that refers to the underlying SolrCloud collection. 
                        The original name (or alias) of the collection will be replaced also in the existing aliases
                        so that they also refer to the new name. Target name must not be an existing alias.
        Returns: 
        JsonObject: A Json Object which contains Solr response 
        """
        args = {"action": 'RENAME','name':name,'target':target}
        response = requests.request("Get", self.fullUrl + "?{}".format(urllib.parse.urlencode(args)))
        return response

    def deleteCollection(self,name,wt = 'json'):
        """
        This function used to delete existing collection

        Parameters:
        name(string):   The name of the collection to delete. This parameter is required.
        async       :    Request ID to track this action which will be processed asynchronously.

        Returns: 
        JsonObject:     The response will include the status of the request and the cores that were deleted. 
                    If the status is anything other than "success", an error message will explain why the request failed.

        """
        args = {"action": 'DELETE','name':name,'wt':wt}
        response = requests.request("Get", self.fullUrl + "?{}".format(urllib.parse.urlencode(args)))
        return response

    
