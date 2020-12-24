from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

client = MongoClient("mongodb://scott:tiger@3.34.252.239", 27017)
db = client.dbsparta
# CORS(app, resources={r"*" : {"origins" : "http://localhost"}})
# CORS(app, resources={r"*" : {"origins" : "http://localhost:5000"}})


@app.route("/", methods=["GET"])
def f1():
    return render_template("index.html")

@app.route("/getdata", methods=["GET"])
def f2():
    data = db.memo.find({}, {"_id" : False})
    return jsonify(list(data))

@app.route("/putdata", methods=["POST"])
def f3():
    title = request.form["title"]
    desc = request.form["desc"]
    result = db.memo.insert_one({"title" : title, "desc" : desc})
    print(result._WriteResult__acknowledged)
    return {"title" : title, "desc" : desc}

@app.route("/modify", methods=["POST"])
def f4():
    oldTitle = request.form["oldTitle"]
    oldDesc = request.form["oldDesc"]
    newTitle = request.form["newTitle"]
    newDesc = request.form["newDesc"]
    print(oldTitle)
    print(oldDesc)
    print(newTitle)
    print(newDesc)
    result = db.memo.update_one({"title" : oldTitle, "desc" : oldDesc}, {'$set': {"title" : newTitle, "desc" : newDesc}})
    print(result.modified_count)
    return {"success" : True}

@app.route("/delete", methods=["POST"])
def f5():
    title = request.form["title"]
    desc = request.form["desc"]
    print(title)
    print(desc)
    result = db.memo.delete_one({"title" : title, "desc" : desc})
    return {"success" : True}


if __name__ == "__main__": 
    app.run("0.0.0.0", port=5000, debug=True)