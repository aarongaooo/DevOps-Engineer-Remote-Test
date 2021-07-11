# DevOps-Engineer-Remote-Test

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required package.

```bash
pipenv install
```
Note: Python interpreter version: Python 3.8.5 64-bit ('base': conda)

## Usage

```bash
cd backend
```
```bash
python app.py
```

## Project Layout
```
DevOps-Engineer-Remote-Test
└── backend                                 # backend folder including all backend files
    └── files                               # files folder including the text file that user upload
        └── sample.txt                      # the text file that user upload
    └── app.py                              # API and router
    └── data.json                           # Local json response data
└── frontend                                # frontend folder including all frontend files
    └── templates                           # Web interface
        └── index.html                      # Web interface for uploading file
        └── reports.html                    # Web interface for getting report

```

## Technology Stack Use
Linux, Python, Flask, HTML/CSS, Bootstrap

## Issues Encountered
1. Issue: The input list could be very large. So users may not be able to wait for the queries to complete, and as such, could not see the report right away.<br/>
   Solution: When the user click the Get Report button, if the report is not ready, then it will show the message to user and ask them to come back later.<br/>
   
2. Issue: Many people might use the website frequently over time. The same hash can be queried multiple times.<br/>
   Solution: There is a file called data.json, and it saved all responses locally with another attribute called time. When the program recieved the hash file from user, and the program will compare the current time, and check if the scan date is less than 1 day, and if it is more than one day, the program will call the GET API again and update the response and time in data.json file<br/>
   
3. How to check if the report is ready?<br/>
   Solution: When the user uploads the file, it will be saved locally in sample.txt file, the program will get the total hash number. When I render the report, I will check if the report number that passed from backend is equal to the total hash number.

