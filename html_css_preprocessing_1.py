from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
import json


def get_udacity_data():
    filename = "udacity.csv"
    #f = open(filename, "w")
    #headers = "course_name, provider, description, link, cost, duration, level\n"
    #f.write(headers)
    arr = []
    page_url = 'https://www.udacity.com/courses/all'
    class_link_prefix = 'https://www.udacity.com'
    client = uReq(page_url)
    page_html = client.read()
    page_soup = soup(page_html, "html.parser")
    children = page_soup.find_all("div", {"class": "course-summary-card"})
    bad_data = 0
    for child in children:
        a_tag = child.h3.a
        class_title = a_tag.text.strip()
        class_link = class_link_prefix + a_tag["href"]
        col_9 = child.findChild("div", {"class": "col-sm-9"})
        class_description = col_9.findChildren("div")[3].text.strip()
        caption_tag = col_9.findChild("span", {"class": "caption text-right"})
        class_difficulty = caption_tag.findChildren("span")[1].text.strip()
        child_client = uReq(class_link)
        child_html = child_client.read()
        child_soup = soup(child_html, "html.parser")
        class_cost = -1
        try:
            class_length = child_soup.findChild("p", {"class": "x-small"}).text.strip()
            class_length = class_length[class_length.index("in") + 3 :]
            class_length = class_length[0:-1] + "nths"
            try:
                class_cost = child_soup.findChild("div", {"class": "card__price"}).text.strip()[1:]
            except:
                pass
        except:
            try:
                section_top = child_soup.findChild("div", {"class": "section--top"})
                class_length = section_top.findChildren("h5")[1].text.strip()
                class_cost = section_top.findChildren("h5")[0].text.strip()
            except:
                try:
                    unordered_list = child_soup.findChild("ul", {"class": "nd_stats"})
                    class_length = unordered_list.h5.text.strip()
                except:
                    pass
        if "Approx. " in class_length:
            class_length = class_length[8:]
        if class_cost == "Free":
            class_cost = 0
        child_client.close()
        if len(str(class_cost)) == 0:
            continue
        if class_cost == -1:
            continue
        if class_length.isdigit():
            continue
##        print("title: " + str(class_title))
##        print("cost: " + str(class_cost))
##        print("length: " + str(class_length))
        arr.append([str(class_title), 'udacity', str(class_description), str(class_link), str(class_cost),str(class_length),  str(class_difficulty)])
        #Find all divs that have class item-container
    df2 = pd.DataFrame(np.array(arr),columns=['course_name', 'provider', 'description', 'link', 'cost', 'duration', 'level'])
    #df = pd.DataFrame(np.array(arr),header = ['course_name', 'provider', 'description', 'link', 'cost', 'duration', 'level'])
    #containers = page_soup.findAll("div", {"class" : "item-container"})
    client.close()
    df2.to_csv('temp.csv')
    return df2


df = get_udacity_data()

#ibm cloud
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey


##{
##  "username": "725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix",
##  "password":
##"e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951",
##  "host": "725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix.cloudant.com",
##  "port": 443,
##}

user_name = "725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix"
password = "e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951"
url =  "https://725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix:e71102d0e5605a5f8367d6bf4caad4758554207acaac646da972b5679e45e951@725dd567-163e-4a27-9e6e-0fe7ba0c2896-bluemix.cloudant.com"
token = ""

client = Cloudant(user_name, password, url = url)
client.connect()

databaseName = "catalog"
myDatabase = client.create_database(databaseName)

if(myDatabase.exists()):
    print("Successfully created a database {}".format(databaseName))

print(df.head())
head = ['courseName', 'provider', 'description', 'link', 'cost', 'duration', 'level']

arr = df.values

for i in range(m):
	jsonDocument = {
		"courseName":arr[i,0],
		"provider":arr[i,1],
		"description":arr[i][2],
		"link":arr[i][3],
		"cost":float(arr[i][4]),
		"duration":arr[i][5],
		"level":arr[i][6]
	}
	newDocument = myDatabase.create_document(jsonDocument)
	if(newDocument.exists()): print("yup")
