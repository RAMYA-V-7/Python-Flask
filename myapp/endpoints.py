import logging
from json2html import *
from flask_pymongo import pymongo
from flask import jsonify, request,render_template
import pandas as pd
con_string = "mongodb+srv://ramya:ramya@cluster0.mzymasp.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_string)
db = client.get_database('flaskappdb')
user_collection = pymongo.collection.Collection(db, 'flaskappcollection') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")

def project_api_routes(endpoints):
    @endpoints.route('/not',methods=['GET'])
    def home():
          return render_template("index.html")
      
    @endpoints.route('/storedata', methods=['POST'])
    def storedata():
        resp = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)            
            print("Employee Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"Employee Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/readdata',methods=['GET'])
    def readdata():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"Employee Data Retrieved Successfully from the Database."
            }
            output = [{
                'id':user['id'],'FirstName' : user['FirstName'], 'LastName' : user['LastName'] , 'AID':user['AID'], 'Age':user['Age'],'Place':user['Place'],'BloodGroup':user['BloodGroup'],'Nationality':user['Nationality']} for user in users]   #list comprehension
            output = json2html.convert(json = output)
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/updatedata',methods=['PUT'])
    def updatedata():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"id":req_body['id']}, {"$set": req_body['updateddata']})
            print("Employee Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"Employee Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    


    @endpoints.route('/deletedata',methods=['DELETE'])
    def deletedata():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"Employee Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    return endpoints