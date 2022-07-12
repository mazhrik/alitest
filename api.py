# Flask
# from typing import final
from flask import Flask, jsonify, abort, request, render_template
from flask_cors import CORS
from flask_mail import Mail, Message
import requests
import string, random, requests
import flask_excel
import json
# from azure import *

from flask_sqlalchemy import SQLAlchemy 
# SQLAlchemy Libraries
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import create_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import insert, text

from marshmallow import fields
# Data engineering libraries
# from sklearn import preprocessing
# import numpy as np

# Date libraries
import datetime
import os
from flask_marshmallow import Marshmallow 
from flask import Flask, request, jsonify
import flask_excel as excel
from flaskext.mysql import MySQL

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/test2'
# db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug=True
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        list_excel=request.get_array(field_name='file')

        print('----------------------',(list_excel))
        for item in list_excel[1:]:
         
         
            name = json.dumps(item[0])
            description = json.dumps(item[1])
            price = json.dumps(item[2])
            qty = json.dumps(item[3])

            new_product = Product(name, description, price,qty)
                
            db.session.add(new_product)
            db.session.commit() 
       
            print('doneee--')


        return jsonify({"result": list_excel})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''
@app.route('/')
def home():
   return render_template('index.html')



# insert database related code here
if __name__ == "__main__":
    excel.init_excel(app)
    app.run()
