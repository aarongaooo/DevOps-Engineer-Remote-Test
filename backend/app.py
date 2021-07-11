from flask import Flask, render_template, request, url_for, redirect
import requests
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__, template_folder='../frontend/templates')
app.config['UPLOAD_EXTENSIONS'] = ['.txt']

ENV = 'dev'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    uploaded_file = request.files['file']
    
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return render_template('index.html', message="Not a valid file, please try again.")
    
        files_in_directory = os.listdir("../backend/files")
        filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
        for file in filtered_files:
            path_to_file = os.path.join("../backend/files", file)
            os.remove(path_to_file)
        uploaded_file.save(os.path.join("../backend/files", "sample.txt"))

    else:
        return render_template('index.html', message="Please submit a text file.")
    
    params = {'apikey': '7ca2e1b0bf6b4d50dbe4ea1fc5685656177c2b9f61e8590330ce1cb8a3e37e86'}
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'

    files = {'file': ("sample.txt", open("../backend/files/"+"sample.txt", 'rb'))}
    response = requests.post(url, files=files, params=params)
    json_response = response.json()
    return render_template('index.html', message=json_response["verbose_msg"])


@app.route('/report', methods=['GET'])
def report():
    f = open("./files/sample.txt", "r")
    Lines = f.readlines()
    resource = ""
    report=[]
    with open('./data.json') as json_data:
        data = json.load(json_data)   
    count = 0 
    for line in Lines:
        if count != len(Lines)-1 :
            line = line[:-1]
        count = count +1
        index = 0
        for record in data:
            if (record["hash"] == line):
                currentTime = datetime.now()
                prevTime = datetime.strptime(record["time"], "%m/%d/%y, %H:%M:%S")
                time_delta = (currentTime - prevTime)
                total_seconds = time_delta.total_seconds()
                if total_seconds > 84000:
                    data.pop(index)
                    resource = resource+record["hash"]+","
                else:
                    report.append(record["report"])
                break
            index = index+1
        else: 
            resource = resource+line+","
   
    resource = resource[:-1]
    print(resource)

    params = {'apikey': '7ca2e1b0bf6b4d50dbe4ea1fc5685656177c2b9f61e8590330ce1cb8a3e37e86', 'resource': resource}
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    responses = requests.get(url, params=params)
    i=0
    json_response = responses.json()
    if type(json_response) !=list:
        json_response = [json_response]
    for json_response in json_response:
        # if (json_response["response_code"] == 1):
        report.append(json_response)
        resource = json_response["resource"]
        newRecord = {
            "hash": resource,
            "report": json_response,
            "time" : datetime.strftime(datetime.now(), "%m/%d/%y, %H:%M:%S")
        }
        data.append(newRecord)
            
    print(len(report))



    jsonString = json.dumps(data)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.save(os.path.join("../backend/data.json", "sample.txt"))
    jsonFile.close()

    return render_template('reports.html', report= report, count = count) 

if __name__ == '__main__':
    app.debug = True
    app.run()
