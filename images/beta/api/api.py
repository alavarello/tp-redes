from flask import Flask
from flask_restful import Resource, Api, reqparse
from models import db, User

app = Flask(__name__)
api = Api(app)


POSTGRES = {
    'user': 'postgres',
    'pw': '123456',
    'db': 'postgres',
    'host': 'database-service',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

parser = reqparse.RequestParser()


class StudentsList(Resource):
    def get(self):
        print(User.query.all())
        return str(User.query.all())


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


class Admin(Resource):

    def post(self):
      parser.add_argument("migrate")
      parser.add_argument("secrete")
      args = parser.parse_args()

      if args['secret'] != '123456':
        return 'Bad request', 401

      if args['migrate']:
        db.create_all()
        return 'Migrated', 200

      return 'Nothing to do here', 200


api.add_resource(StudentsList, '/students/')
api.add_resource(Admin, '/admin/')


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0',  port=8888)
