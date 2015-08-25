from flask import Flask

from flask_restful import Resource, Api, fields, reqparse 

from account import *


app = Flask(__name__)

api = Api(app)



post_parser = reqparse.RequestParser()

post_parser.add_argument(

    'username', dest='username',

    location='form', required=True,

    help='The user username',

)

post_parser.add_argument(

    'email', dest='email',

    location='form',

    required=True, help='The user email',

)

post_parser.add_argument(

    'password', dest='password',

     location='form', required=True,

     help='The user password',

)

post_parser.add_argument(

     'domain', dest = 'domain',

      location = 'form', required=True,

      help = 'Domain password',

)	



class HelloWorld(Resource):

    def post(self):

 	args = post_parser.parse_args()
	create = AccountCreation(args.name, args.username, args.password, args.domain, args.email, "twentyfifteen")
	user = create.CreateUser()
	return {user : 'world'}
   			

api.add_resource(HelloWorld, '/')



if __name__ == '__main__':

    app.run(debug=True)
