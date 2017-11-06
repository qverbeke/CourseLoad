# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, render_template, request
import json
from queryingDB import getCoursesByAttribute
app = Flask(__name__)
companies={"codecademy":"Codecademy", "coursera":"Coursera","edx":"edX", "lynda":"Lynda", "mit":"MIT", "openculture":"Open Culture", "udacity":"Udacity"}
def getKeywordList(keywords):
	result = ""
	for i in keywords:
		result+=(i+", ")
	return result
class query_correlation:
	def __init__(self, provider, link, courseName, description, keywords):
		self.provider=provider
		self.company=companies[provider]
		self.link=link
		self.courseName=courseName
		self.description=description
		self.keywords=getKeywordList(keywords)
keywords_list=[]
mcbq=[]
mcbq.append(query_correlation("codecademy", "http://www.google.com","Java Information", "Description of java", {"Java":"cool", "Programming":"lame"}))
mcbq.append(query_correlation("coursera", "http://www.google.com","Learning Java", "This is the course description", {"Coding":"cool", "Learning":"lame"}))
mcbq.append(query_correlation("edx", "http://www.google.com","Java course for beginners", "Describe java course", {"Java":"cool", "Coding":"lame"}))
mcbq.append(query_correlation("mit", "http://www.google.com","An introduction to java", "Java Description", {"Coding in Java":"cool", "Java":"lame"}))
mcbq.append(query_correlation("openculture", "http://www.google.com","Java Basics", "The basics of java: a description", {"Java coding":"cool", "google":"lame"}))

"""
def parse_dict(query):
	result_dict=getCoursesByAttribute(query)
	print result_dict
	result_ary=[]
	for i in result_dict:
		result_ary.append(query_correlation(str(i["provider"]), str(i["link"]), str(i["courseName"]), str(i["description"])))
	return result_ary
"""
@app.route('/')
def Welcome():
	return render_template('index.html', a = 0)

@app.route('/searchresults', methods=['POST'])
def searchResults():	
	query=request.form['query']
	return render_template('searchresults.html', results_list=mcbq)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
