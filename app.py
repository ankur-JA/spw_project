from pymongo import MongoClient
from flask import Flask,request,jsonify
import gridfs
app = Flask(__name__)
client = MongoClient('localhost', 27017)

db = client.school
students = db.students

@app.route("/students",methods=['POST'])
def create():
      #fs=gridfs.GridFS(db)
      #file="C:/Users/DELL/Downloads/download.jpg"
      #with open(file,'rb')as f:
            #contents=f.read()
      ##fs.put(contents,filename="file")
      input = request.get_json()
      students.insert_one(input)
      return jsonify({"success": True})

@app.route("/students",methods=['GET'])
def read():
     data = list(students.find())
     for i in range(len(data)):
       del data[i]['_id']
     print(data)
     return jsonify({"success": True})

@app.route("/students",methods=['PUT'])
def update():
      input = request.get_json()
      students.update_many(
            {"roll":input["roll"]},
            {"$set":{"name":input["name"],"dept":input["dept"]}})

      return jsonify({"success": True})

@app.route("/students",methods=['DELETE'])
def delete():
      input = request.get_json()
      students.delete_many({"roll":input["roll"]})
      return jsonify({"success": True})

if __name__ == ('__main__'):
    app.run(debug=True)