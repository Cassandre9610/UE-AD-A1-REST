from flask import Flask, render_template, request, jsonify, make_response
import copy
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'
DB_PATH = '{}/databases/times.json'.format(".")

with open(DB_PATH, "r") as jsf:
   schedule:dict = json.load(jsf)["schedule"]


def write(new_schedule):
   global schedule
   with open(DB_PATH, "w") as f:
      full = {}
      full['schedule']=new_schedule
      json.dump(full, f)
      schedule = new_schedule


def error_not_found(message: str):
   return make_response(jsonify({"error":message}),500)


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/json", methods=['GET'])
def get_json():
   return make_response(jsonify(schedule), 200)

@app.route("/schedule/<date>/<movie_id>", methods=['POST']) #TODO voir si on passe en url ou par le body
def add_schedule(date, movie_id):
   for day in schedule:
      if day["date"] == date:
         if day["movies"].count(movie_id) == 0:
            day["movies"].append(movie_id)
            res = make_response(jsonify(day), 201)
            return res
         else :
            res = make_response({"error": "Movie already scheduled for this date"}, 500)
            return res
   # aucune date ne correspond
   new_day = {
      "date": date,
      "movies": [movie_id]
   }
   schedule.append(new_day)
   write(schedule)
   return make_response(jsonify(new_day), 201)

@app.route("/schedule/date/<date>", methods = ['GET'])
def get_by_date(date):
   for day in schedule:
      if day["date"] == date:
         return make_response(jsonify(day), 200)
   return make_response({"error": "No schedule found for this date"}, 404)

@app.route("/schedule/movie/<movie_id>", methods = ['GET'])
def get_by_movie(movie_id):
   return_json: list = []
   for day in schedule:
      if day["movies"].count(movie_id) > 0 :
         return_json.append(day)

   if len(return_json) == 0:
      return make_response({"error": "No schedule found for this date"}, 404)
   return make_response(return_json, 200)

@app.route("/schedule/<date>", methods=['DELETE'])
def delete_by_date(date):
   old_schedule = schedule
   new_schedule = [day for day in old_schedule if day["date"] != date]
   write(new_schedule)
   return make_response(jsonify(schedule), 200)

@app.route("/schedule/<date>/<movie_id>", methods=['DELETE'])
def delete_movie_from_date(date, movie_id):
   old_schedule: list[dict] = schedule
   new_schedule = []
   for day in old_schedule :
      new_day = copy.deepcopy(day)
      if new_day["date"] == date :
         new_day["movies"] = [movie for movie in new_day["movies"] if movie != movie_id]
      new_schedule.append(new_day)

   write(new_schedule)
   return make_response(jsonify(schedule), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
