from flask import Flask, request,session,abort, redirect,render_template, jsonify
from flask_cors import CORS, cross_origin

from mongo import mongo_pdf, download
import base64
import json



import requests
import os
import pathlib

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


app = Flask(__name__)
app.secret_key = "GDSC"
CORS(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

current_user = "not_defined"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html', current_user_id=current_user)




@app.route('/show_projects', methods=['GET','POST'])
def show():
    if request.method == 'POST':
        pointer = request.get_data()
        
        pointer = pointer.decode('utf-8')
        with open('./static/json/pdf_name.json', 'r') as u:
            name_of_pdf = json.load(u)
            
        pdf_download_data = download(name_of_pdf[pointer])
        return pdf_download_data
    return render_template('index.html',current_user_id=current_user)
    
    
    
    
@app.route('/upload_pdf', methods=['GET', 'POST'])
def pdf():
    if request.method == 'POST':
        pdf_base64 = request.get_json()
        
        # decode = open(pdf_base64['pdf_name'], 'wb')
        # decode.write(base64.b64decode(pdf_base64['pdf']))
        
        encoded_pdf = 'data:application/pdf;base64,' + pdf_base64['pdf']
        # print(encoded_pdf)
        
        encoded_pdf_utf = encoded_pdf.encode('utf-8') 
        enc_pdf = pdf_base64['pdf'].encode('utf-8')
        
        mongo_pdf(encoded_pdf_utf, pdf_base64['pdf_name'])
        
    return render_template('upload_page.html',current_user_id=current_user)
    




if __name__ == '__main__':
    app.run()