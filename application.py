from flask import Flask, jsonify, redirect ,request, render_template
from flask_pymongo import PyMongo
import json

application = Flask(__name__)
application.config["MONGO_URI"] = "mongodb+srv://test:1234@cluster0.ibsdp.mongodb.net/test-api?retryWrites=true&w=majority"
mongo = PyMongo(application)

db_operations = mongo.db.sample


@application.route('/')
def index():
    return 'Welcome'

################ read 

@application.route('/data',methods=['GET'])
def all_data():
    users = db_operations.find()
    users = convert_dict(users)
    print(users)
    return ({'data':users})

############# read one

@application.route('/data/<int:id>',methods=['GET'])
def one_data(id):
    users = db_operations.find({'roll no':id})
    users = convert_dict(users)
    print(users)
    return ({'data':users})

############# create new record

@application.route('/create_new',methods=['POST'])
def create_new():
    roll_no = request.args.get('roll')
    name = request.args.get('name')
    dept = request.args.get('dept')

    new_data = {
        'roll no':int(roll_no),
        'name': name,
        'dept' : dept
    }
    db_operations.insert_one(new_data)
    return 'sucessfully created new record'

############# update record

@application.route('/update/<int:id>',methods=['PUT'])
def update(id):
    #roll_no = request.args.get('roll')
    name = request.args.get('name')
    dept = request.args.get('dept')
    set_data = {'$set':{'name':name,'dept':dept}}

    db_operations.update_one({'roll no':id},set_data)
    return 'sucessfully updated record'

################### delete

@application.route('/delete/<int:id>',methods=['DELETE'])
def delete(id):

    db_operations.delete_one({'roll no':id})
    return 'sucessfully Deleted record'





def convert_dict(main_dict):
    results = []
    for document in main_dict:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results



if __name__=='__main__':
    application.run(host="localhost", port=8000, debug=True)
    #application.run(host='127.0.0.1', port=8000)

# username : root
# ip : 142.93.212.17
# password : sacC2p7rFaLj
# e.g sudo ssh root@142.93.212.17