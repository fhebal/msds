#***********************************************
# File: aws_restapi.py
# Desc: Python script to connect to AWS S3
# Purpose: Perform following operation:
#          1. List buckets
#          2. Bucket exists
#          3. Files get file
#          4. Query 1
#          5. Query 2
#          6. Query 3
#          7. Query 4
# Original Auth: Shreenidhi Bharadwaj
# Student Code: Ferdynand Hebal
# Date: 02/09/2020
# ALL RIGHTS RESERVED | DO NOT DISTRIBUTE
#************************************************/

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

import os
import boto3
from botocore.exceptions import ClientError
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)


@app.route('/')
def api_root():
    return '<h1>AWS S3 REST API</h1>'

@app.route('/buckets')
def api_bucket():
    return '<h2>Choose valid operation on Bucket (/list, /create, /delete, /exists)</h2>'

@app.route('/files')
def api_file():
    return '<h2>Choose valid operation on File (/upload, /download, /delete, /exists)</h2>'


@app.route('/buckets/list')
def list_buckets():
    """Connect to S3 and query all buckets

    :return: list of buckets
    """

    s3 = boto3.client('s3')

    # Call S3 to list current buckets
    resp = s3.list_buckets()

    # Get a list of all bucket names from the response
    buckets = {"buckets" : [bucket['Name'] for bucket in resp['Buckets']]}

    response = jsonify(buckets)
    response.status_code = 200

    return(response)


@app.route('/buckets/exists/<bucket_name>')
def bucket_exists(bucket_name):
    """Determine whether bucket exists and the user has permission
    to access it

    :param bucket_name: AWS S3 bucket to be searched
    :return: True if the referenced bucket_name exists, otherwise False
    """

    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=bucket_name)
        result = {"bucket_name": bucket_name, "exists" : True}

    except ClientError as e:
        result = {"bucket_name": bucket_name, "exists" : False}

    response = jsonify(result)
    response.status_code = 200

    return(response)

@app.route('/files/get')
def file_get():
    """Gets file in an S3 bucket

    :param bucket_name: AWS S3 Bucket
    :param file_name: File to be searched
    :return: file content
    """
    
    bucket_name = request.args.get("bucket_name")
    file_name   = request.args.get("file_name")
    
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    content = response['Body'].read().decode('utf-8')
    
    return content


@app.route('/files/query1')
def query_1():
    """Query 1 - show top few rows of data
    
    :return: Query 1 results
    """
    
    db_string = "postgres://postgres:password@database-1.cc4xpjv8thnk.us-east-1.rds.amazonaws.com:5432/boxrec"
    db = create_engine(db_string)

    query = ''' SELECT * FROM boxer_career LIMIT 10'''
    results = str(db.execute(query).fetchall())
    
    return results



@app.route('/files/query2')
def query_2():
    """Query 2 - Names of Boxers with most bouts (top 5)
    
    :return: Query 2 results
    """
    
    db_string = "postgres://postgres:password@database-1.cc4xpjv8thnk.us-east-1.rds.amazonaws.com:5432/boxrec"
    db = create_engine(db_string)

    query = '''
    SELECT b.opponent_name as "Boxer_name", a."#_of_bouts" FROM (
    SELECT boxer_link, COUNT('id') as "#_of_bouts"
    FROM boxer_career
    GROUP BY boxer_link
    ORDER BY "#_of_bouts" DESC) a
    LEFT JOIN (SELECT opponent_name, opponent_link FROM boxer_career) b on b.opponent_link = a.boxer_link
    WHERE boxer_link != ''
    LIMIT 5
    ;'''
    results = str(db.execute(query).fetchall())
    
    return results


@app.route('/files/query2')
def query_3():
    """Query 3 - Top 10 most popular locations sorted by # of bouts
    
    :return: Query 3 results
    """
    # Connect to boxrec database
    db_string = "postgres://postgres:password@database-1.cc4xpjv8thnk.us-east-1.rds.amazonaws.com:5432/boxrec"
    db = create_engine(db_string)

    query = '''
    SELECT * FROM (
    SELECT location, COUNT('id') as "#_of_bouts", COUNT(DISTINCT "boxer_link") "#_of_boxers"
    FROM boxer_career
    GROUP BY location
    ORDER BY "#_of_bouts" DESC) a
    WHERE location != ''
    LIMIT 10
    ;'''
    results = str(db.execute(query).fetchall()
    return results


@app.route('/files/query4')
def query_4():
    """Query 4 - Boxers sorted by result type 
    
    :return: Query 4 results
    """
    
    db_string = "postgres://postgres:password@database-1.cc4xpjv8thnk.us-east-1.rds.amazonaws.com:5432/boxrec"
    db = create_engine(db_string)

    query = '''
    SELECT b.opponent_name as "Boxer_name"
    , a.*

    FROM(
    SELECT boxer_link, result,
    ROUND(COUNT(DISTINCT id)*1./COUNT(DISTINCT "boxer_link"),2) "avg_#of_bouts_in_career"
    FROM 
    boxer_career
    WHERE boxer_link != ''
    GROUP BY boxer_link, result) a
    LEFT JOIN (SELECT opponent_name, opponent_link FROM boxer_career) b on b.opponent_link = a.boxer_link
    WHERE b.opponent_name != ''
    ORDER BY  a.result,a."avg_#of_bouts_in_career" DESC
    ;'''
    results = str(db.execute(query).fetchall())
    
    return results

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
