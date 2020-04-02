# -*- coding: utf-8 -*-

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from json import dumps
import os
import base64
import io
import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
from flask import send_file
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from google.appengine.api import app_identity
#import google.cloud.automl
#from google.cloud.automl_v1beta1 import PredictionServiceClient

credentials = GoogleCredentials.get_application_default()
api = discovery.build('ml', 'v1', credentials=credentials)
project = app_identity.get_application_id()
model_name = os.getenv('MODEL_NAME', 'babyweight')
version_name = os.getenv('VERSION_NAME', 'dnn')  


api2 = discovery.build('automl', 'v1', credentials=credentials)


app = Flask(__name__)


    
    #api_endpoint = 'https://automl.googleapis.com/v1beta1/projects/resolute-land-232921/locations/us-central1/models/ICN6626189232606019584:predict'
    #headers = {"Authorization": "Bearer "+visk}
    #r = requests.post(url = api_endpoint, json = {"payload": {"image": {"imageBytes": picture}}}, headers=headers)
    #result = json.loads(r.text)#['payload'][0]['displayName']


def get_image_class(picture):
    payload = {"payload": {"image": {"imageBytes": picture}}}
    body = dumps(payload)
    input_data = payload
    parent = 'projects/resolute-land-232921/locations/us-central1/models/ICN6626189232606019584'
    prediction = api2.projects().locations().models().predict(body=input_data, name=parent).execute()
    return prediction

def get_prediction(features):
    input_data = {'instances': [features]}
    parent = 'projects/%s/models/%s/versions/%s' % (project, model_name, version_name)
    prediction = api.projects().predict(body=input_data, name=parent).execute()
    return prediction['predictions'][0]['babyweight'][0]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def input_form():
    return render_template('form.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    def gender2str(val):
        genders = {'unknown': 'Unknown', 'male': 'True', 'female': 'False'}
        return genders[val]

    def plurality2str(val):
        pluralities = {'1': 'Single(1)', '2': 'Twins(2)', '3': 'Triplets(3)', '4': 'Quadruplets(4)', '5': 'Quintuplets'}
        if features['is_male'] == 'Unknown' and int(val) > 1:
            return 'Multiple(2+)'
        return pluralities[val]

    data = json.loads(request.data.decode())
    mandatory_items = ['baby_gender', 'mother_age',
                     'plurality', 'gestation_weeks']
    for item in mandatory_items:
        if item not in data.keys():
            return jsonify({'result': 'Set all items.'})

    #picture = base64.b64decode(data['test'])#.decode('utf8')
    picture = data['test'].decode('utf8')

    # Return image
    #return send_file(io.BytesIO(picture),attachment_filename='pic.jpeg',mimetype='image/jpg')

    def label2val(val):
        labels = {'ugly': 1, 'okay': 2, 'decent': 3, 'great': 4}
        label_val = float(labels[val])
        return label_val

    image_class = get_image_class(picture)
    image_class = image_class['payload'][0]['displayName']


    features = {}
    features['key'] = 'nokey'
    features['is_male'] = gender2str(data['baby_gender'])
    #features['mother_age'] = float(data['mother_age'])
    features['mother_age'] = label2val(image_class)
    features['plurality'] = plurality2str(data['plurality'])
    features['gestation_weeks'] = float(data['gestation_weeks'])


    # Return DNN Prediction
    prediction = get_prediction(features)
    #return jsonify({'result': data['test']})
    #return jsonify({'result': image_class})
    return jsonify({'result': '{:.2f} ARS'.format(prediction)+'\n'+str(image_class)})
