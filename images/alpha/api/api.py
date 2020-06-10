import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from models import db, User

app = Flask(__name__)
api = Api(app)

database_username = os.environ.get("DATABASE_USER", default="")
database_pass = os.environ.get("DATABASE_PASS", default="")
database_name = os.environ.get("DATABASE_NAME", default="")

DATABASE = {
    'user': database_username,
    'pw': database_pass,
    'db': database_name,
    'host': 'database-service',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % DATABASE
db.init_app(app)
with app.app_context():
    db.create_all()
parser = reqparse.RequestParser()


class StudentsList(Resource):
    def get(self):
        return str(User.query.all()), 200


    def post(self):
      parser.add_argument("username")
      parser.add_argument("email")
      args = parser.parse_args()

      new_user = User(
        username=args["username"],
        email=args["email"]
      )
      db.session.add(new_user)
      db.session.commit()
      return str(new_user), 201


api.add_resource(StudentsList, '/students/')


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0',  port=8888)
