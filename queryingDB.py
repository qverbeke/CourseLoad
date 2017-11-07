
#ibm cloud
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features


import json
import os
import time
user_name = "725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix"
password = "e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951"
url =  "https://725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix:e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951@725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix.cloudant.com"
token = ""


user_name_watson = "63da93ac-d845-45bc-b490-d54eac92c5b5"
password_watson = "kWyVorvR4oxm"
url_watson = "https://gateway.watsonplatform.net/natural-language-understanding/api"

def parseJson(dct):
        conceptz = dct["concepts"]
        result = []
        for i,concept in enumerate(conceptz):
            result[i] = {}
            result[i]['text'] = concept['text']
            result[i]['relevance'] = concept['relevance']
        return result
def db_watson_query():
        client = Cloudant(user_name, password, url = url)
        client.connect()
        databaseName = "catalog"
        myDatabase = client[databaseName]
        if(myDatabase.exists()):
                print("Successfully created a database {}".format(databaseName))


        result_collection = Result(myDatabase.all_docs, include_docs=True)
        print ("Retrieved full document:\n{0}\n".format(result_collection[0]))

        end_point = '{0}/{1}'.format(url, databaseName + "/_all_docs")
        params = {'include_docs': 'true'}
        response = client.r_session.get(end_point, params=params)

        #connect to Watson NLU
        natural_language_understanding = NaturalLanguageUnderstandingV1(
          username=user_name_watson,
          password=password_watson,
          version="2017-02-27")



        #feed data to watson api
        for i in range(0, 300):
                tmp = result_collection[i][0]['doc']

                response = natural_language_understanding.analyze(
                        text = tmp['description'],
                        features=[
                                Features.Concepts(
                                        # Concepts options
                                        limit=5
                                        )
                                ]
                        )
                jss = json.dumps(response, indent=2)
                parses = parseJson(response)
                mydocument = myDatabase[tmp['_id']]
                mydocument['keywords'] = parses
                mydocument.save()
        client.disconnect()
        
def getCoursesByAttribute(attribute):
        client = Cloudant(user_name, password, url = url)
        client.connect()
        databaseName = "catalog"
        myDatabase = client[databaseName]
        if(myDatabase.exists()):
                print("Successfully created a database {}".format(databaseName))


        result_collection = Result(myDatabase.all_docs, include_docs=True)
        #print ("Retrieved full document:\n{0}\n".format(result_collection[0]))

        end_point = '{0}/{1}'.format(url, databaseName + "/_all_docs")
        params = {'include_docs': 'true'}
        response = client.r_session.get(end_point, params=params)
        resultz = []
        count = 0
        for i in range(0, 150):
                tmp = result_collection[i][0]['doc']
                if('keywords' in tmp):
						dct=tmp['keywords']
						for entry in dct:
							if(attribute.lower() in entry["text"].lower()):
									resultz.append(tmp)
									count+=1
                if (count == 5):
                        break
                time.sleep(.2)
        client.disconnect()
        return resultz

        
##              
##user_name = "725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix"
##password = "e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951"
##url =  "https://725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix:e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951@725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix.cloudant.com"
##token = ""
##
##client = Cloudant(user_name, password, url = url)
##client.connect()
##
##databaseName = "catalog"
##myDatabase = client[databaseName]
##if(myDatabase.exists()):
##    print("Successfully created a database {}".format(databaseName))
####result_collection = Result(myDatabase.all_docs)
##
##result_collection = Result(myDatabase.all_docs, include_docs=True)
##print ("Retrieved full document:\n{0}\n".format(result_collection[0]))
##
##end_point = '{0}/{1}'.format(url, databaseName + "/_all_docs")
##params = {'include_docs': 'true'}
##response = client.r_session.get(end_point, params=params)
###print ("{0}\n".format(response.json()))
##
###client.disconnect()
