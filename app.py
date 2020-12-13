from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, model
from data import *
import Database.repository as DB
app = Flask(__name__)
api = Api(app)
db=Database()

login_data = reqparse.RequestParser()
login_data.add_argument("username", type=str, help="username")
login_data.add_argument("password", type=str, help="password")
class Login(Resource):
    def get(self):
        args = login_data.parse_args()

        user=DB.login(args['username'],args['password'])
        return user

api.add_resource(Login, "/login")

history_data = reqparse.RequestParser()
history_data.add_argument("id", type=str, help='user_id')
class History(Resource):
    def get(self):
        args = history_data.parse_args()
        his=DB.getHistory(args["id"])
        return {'data':his}

api.add_resource(History, "/history")

recommend_data = reqparse.RequestParser()
recommend_data.add_argument("id", type=str, help='user_id')
class Recommend(Resource):
    def get(self):
        args = history_data.parse_args()
        return db.get_recommend_play_list(args['id'])

api.add_resource(Recommend, "/recommend")

search_data = reqparse.RequestParser()
search_data.add_argument("content", type=str, help='content')
class Search(Resource):
    def get(self):
        args = search_data.parse_args()
        return database.search(args['content'])

api.add_resource(Search, "/search")

playlistfortrack_data = reqparse.RequestParser()
playlistfortrack_data.add_argument("content", type=str, help='content')
class PlayTrack(Resource):
    def get(self):
        args = playlistfortrack_data.parse_args()
        return database.playlistfortrack(args['content'])

api.add_resource(PlayTrack, "/playlistfortrack")

if __name__ == "__main__":
    app.run(debug=True)
    