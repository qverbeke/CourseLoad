from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
import numpy as np
def timeChange(num,typ):
    typ=typ.lower()
    num=int(num)
    notOk=True
    while (notOk):
        if (typ.lower()=="hours" and num>=24):           #minutes hours days weeks months
            typ="days"
            num=num/24
        elif(typ.lower()=="days" and num>=7):
            typ="weeks"
            num=num/7
        elif(typ.lower()=="weeks" and num>=5):
            typ="months"
            num=num/5
        else:
            notOk=False
    return str(typ)

filename="name.txt"
f= open(filename,'w',encoding='utf-8')
arr = []
arr.append(['course_name', 'provider', 'course_description', 'url', 'cost', 'duration'])
headers="course_name, provider, course_description, url, cost, duration\n"

f.write(headers)
my_url = 'https://www.codecademy.com/catalog/subject/web-development'
uClient = uReq(my_url)
#opening up connection, grabbing URL
page_html = uClient.read()
uClient.close()
#html parser
page_soup = soup(page_html, "html.parser")
x=page_soup.findAll("div",{"class":"_2malf9e9Ho8Bd8DPrKa47t"})
y=page_soup.findAll("div",{"class":"YazPijjubqJJih15ZRWAT"})

intensive_programs=y[0:len(x[0])]
regular_courses=y[len(x[0]):len(y)]
for program in intensive_programs:
    intensive_program_names=program.div.a.div.findChildren("div")[1].h3.text
    intensive_program_desc=program.div.a.div.findChildren("div")[1].span.text
    intensive_program_time = program.div.a.div.findChildren("div")[2].text[10:]
    url ='https://www.codecademy.com' + program.div.a["href"]

    print(intensive_program_names)
    print(intensive_program_desc)
    l=intensive_program_time.split(" ")
    print(timeChange(l[0],l[1]))
    print(url)

#WEB DEVELOPMENT
    newClient = uReq(url)
    new_page_html = newClient.read()
    new_page_soup = soup(new_page_html, "html.parser")
    #print(new_page_soup)
    cost = new_page_soup.body.findChildren("section")[5].div.div.findChildren("div")[1].div.findChildren("div")[3].p.text[1:]
    print("COST: ",cost)
    #arr.append([str(intensive_program_names), 'Codecademy', intensive_program_desc, str(url), str(cost), timeChange(l[0],l[1])])
    f.write(intensive_program_names + "," + "Codecademy," + intensive_program_desc + "," + url + "," + str(cost)+","+timeChange(l[0],l[1])+"\n")
    #print("A: ",program)

for program in regular_courses:
    regular_program_names = program.div.a.div.findChildren("div")[1].h3.text
    regular_program_desc = program.div.a.div.findChildren("div")[1].span.text
    regular_program_time = program.div.a.div.findChildren("div")[2].text[10:]
    url = program.div.a["href"]
    cost=0 #(all of these are free)
    print(regular_program_names)
    print(regular_program_desc)
    l=regular_program_time.split(" ")
    print(timeChange(l[0],l[1]))
    print(cost)
    url = 'https://www.codecademy.com' + program.div.a["href"]
    print(url)
    #arr.append([str(regular_program_names), 'Codecademy', regular_program_desc, str(url), str(cost), timeChange(l[0], l[1])])
    f.write(regular_program_names + "," + "Codecademy," + regular_program_desc + "," + url + "," + str(cost) + "," + timeChange(l[0], l[1]) + "\n")
    print("-----------------------------------------------------------------------------------------------")

#PROGRAMMING
my_url = 'https://www.codecademy.com/catalog/subject/programming'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
numOfCourses = page_soup.find("div",{"class":"_2malf9e9Ho8Bd8DPrKa47t"})
cost=0 
arr = []
for course in numOfCourses:
    course_names=course.div.a.div.findChildren("div")[1].h3.text
    course_desc = course.div.a.div.findChildren("div")[1].span.text
    course_times = course.div.a.div.findChildren("div")[2].span.span.text
    url = 'https://www.codecademy.com'+page_soup.find("a",{"class":"dDJdduG6kB9ChlJHZrNpf"})["href"]
    l=course_times.split(" ")
    arr.append([str(course_names), 'Codecademy', course_desc, str(url), str(cost), timeChange(l[0], l[1])])

#DATA SCIENCE
my_url = 'https://www.codecademy.com/catalog/subject/data-science'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
numOfCourses = page_soup.find("div",{"class":"_2malf9e9Ho8Bd8DPrKa47t"})
cost=0
for course in numOfCourses:
    course_names=course.div.a.div.findChildren("div")[1].h3.text
    course_desc = course.div.a.div.findChildren("div")[1].span.text
    course_times = course.div.a.div.findChildren("div")[2].span.span.text
    url = 'https://www.codecademy.com'+page_soup.find("a",{"class":"dDJdduG6kB9ChlJHZrNpf"})["href"]
    l=course_times.split(" ")
    arr.append([str(course_names), 'Codecademy', course_desc, str(url), str(cost), timeChange(l[0], l[1])])
#PARTNERSHIPS
my_url = 'https://www.codecademy.com/catalog/subject/partnerships'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
numOfCourses = page_soup.find("div",{"class":"_2malf9e9Ho8Bd8DPrKa47t"})
cost=0
for course in numOfCourses:
    course_names=course.div.a.div.findChildren("div")[1].h3.text
    course_desc = course.div.a.div.findChildren("div")[1].span.text
    course_times = course.div.a.div.findChildren("div")[2].span.span.text
    url = 'https://www.codecademy.com'+page_soup.find("a",{"class":"dDJdduG6kB9ChlJHZrNpf"})["href"]
    l=course_times.split(" ")
    arr.append([str(course_names), 'Codecademy', course_desc, str(url), str(cost), timeChange(l[0], l[1])])
    f.write(course_names + "," + "Codecademy," + course_desc + "," + url + "," + str(cost) + "," + timeChange(l[0], l[1]) + "\n")
links=['https://www.codecademy.com/catalog/language/html-css','https://www.codecademy.com/catalog/language/python',
       'https://www.codecademy.com/catalog/language/javascript','https://www.codecademy.com/catalog/language/java',
       'https://www.codecademy.com/catalog/language/sql','https://www.codecademy.com/catalog/language/bash',
       'https://www.codecademy.com/catalog/language/ruby']
for my_url in links:

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    numOfCourses = page_soup.find("div",{"class":"_2malf9e9Ho8Bd8DPrKa47t"})
    cost=0
    for course in numOfCourses:
        course_names=course.div.a.div.findChildren("div")[1].h3.text
        course_desc = course.div.a.div.findChildren("div")[1].span.text
        course_times = course.div.a.div.findChildren("div")[2].span.span.text
        url = 'https://www.codecademy.com'+page_soup.find("a",{"class":"dDJdduG6kB9ChlJHZrNpf"})["href"]
        print(course_names)
        print(course_desc)
        l=course_times.split(" ")
        print(timeChange(l[0],l[1]))
        print(cost)
        print(url)
        arr.append([str(course_names), 'Codecademy', course_desc,str(url), str(cost), timeChange(l[0], l[1])])
##        f.write(str(course_names) + "," + "Codecademy," + str(course_desc) + "," + url + "," + str(cost) + "," + timeChange(l[0],l[1]) + "\n")
#npyss = np.array(arr, dtype = np.string_)
#print(npyss)
#import pandas as pd
#df = pd.DataFrame(npyss)
#np.savetxt("name.csv",npyss)
#df.to_csv('dadasdf.csv')
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

import pandas as pd
df = pd.DataFrame(arr)
arr = df.values
m,n = arr.shape
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

head = ['courseName', 'provider', 'description', 'link', 'cost', 'duration', 'level']

##arr = df.values

for i in range(m):
	jsonDocument = {
		"courseName":arr[i,0],
		"provider":arr[i,1],
		"description":arr[i][2],
		"link":arr[i][3],
		"cost":float(arr[i][4]),
		"duration":arr[i][5],
        }
	newDocument = myDatabase.create_document(jsonDocument)
	if(newDocument.exists()): print("yup")

@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
	
        if request.method == "POST":
		
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)  
