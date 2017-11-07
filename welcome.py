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
		result+=(i["text"]+", ")
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
def parse_dict(query):
	result_dicts=getCoursesByAttribute(query)
	result_ary=[]
	for result_dict in result_dicts:
		result_ary.append(query_correlation(result_dict["provider"], result_dict["link"], result_dict["courseName"], result_dict["description"], result_dict["keywords"]))
	return result_ary

@app.route('/')
def Welcome():
	return render_template('index.html', a = 0)

@app.route('/searchresults', methods=['POST'])
def searchResults():	
	query=request.form['query']
	mcbq=parse_dict(query)
	return render_template('searchresults.html', resultslist=mcbq)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
