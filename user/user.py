from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
import time

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

def write(new_users):
   with open('{}/databases/users.json'.format("."), 'w') as f:
      full = {}
      full['users']=users
      json.dump(full, f)


def error_not_found(message: str):
   return make_response(jsonify({"error":message}),500) # TODO 404 ?


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/json", methods=['GET'])
def get_json():
   res = make_response(jsonify(users), 200)
   return res

@app.route("/user/<userid>", methods=['GET'])
def get_by_id(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         res = make_response(jsonify(user),200)
         return res
      
   return error_not_found("User ID not found")

@app.route("/user/name/<username>", methods=["GET"])
def get_by_name(username):
   for user in users:
      if str(user["name"]) == str(username):
         res = make_response(jsonify(user), 200)
         return res
      
   return error_not_found("User name not found")


@app.route("/user/<userid>/name/<new_name>", methods=["PUT"])
def update_user(userid, new_name):
   for user in users:
      if str(user["id"]) == userid:
         user["name"] = new_name
         res = make_response(jsonify(user), 200)
         write(users)
         return res
      
   return error_not_found("User ID not found")

@app.route("/user/<userid>", methods=['DELETE'])
def delete_user(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         users.remove(user)
         write(users)
         return make_response(jsonify(user), 200)
      
   return error_not_found("User ID not found")

@app.route("/user/<userid>", methods=['POST'])
def create_user(userid):
   req = request.get_json()

   for user in users:
      if str(user["id"]) == str(userid):
            print(user["id"])
            print(userid)
            return make_response(jsonify({"error":"user ID already exists"}),500)

   # req["last_used"] = time.time_ns() # Pas certain de la methode
   users.append(req)
   write(users)
   res = make_response(jsonify({"message":"user added"}),200)
   return res


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
