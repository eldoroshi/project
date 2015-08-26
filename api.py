import validators

from flask import Flask

from flask_restful import Resource, Api, fields, reqparse 

from account import *

from edit_account import *

from delete_account import *


app = Flask(__name__)

api = Api(app)


def email(email_str):

	if validators.email(email_str):

		return email_str
	else:
		return "This isn't a valid email address"

def string(valid_string):

	if isalnum(valid_string):

		return string

	else:
		 return "This isn't a valid string"


def url(vdomain):

	if validators.url(vdomain):

		return vdomain
	else: 
		return "This isn't an valid url"



'''Parameters that will be posted on api '''
post_parser = reqparse.RequestParser()

post_parser.add_argument(

    'username', dest='username',

    location='form', required=True,

    help='The user username', type=string

)

post_parser.add_argument(

    'email', dest='email',

    location='form', type=email

    required=True, help='The user email',

)

post_parser.add_argument(

    'password', dest='password',

     location='form', required=True,

     help='The user password', type=string

)

post_parser.add_argument(

     'domain', dest = 'domain',

      location = 'form', required=True,

      help = 'Domain', type=url

)	

post_parser.add_argument(

     'theme', dest='theme',

      localtion = 'form', required=True,

      help = 'Select the theme will be installed', type=string

) 	



'''Post api class to execute creation account functions '''
class create(Resource):

    def post(self):

 	args = post_parser.parse_args()
	create = AccountCreation(args.name, args.username, args.password, args.domain, args.email, args.theme)
	user = create.CreateUser()
	return {user : 'created'}
   			

'''Post api class to execute editing account functions '''
class update(Resource):

    def post(self):

	args = post_parser.parse_args()
	update = AccountEditing(args.name, args.username, args.password, args.domain, args.newdomain, args.email, args.theme)
	user = update.EditUserPass()
	return {user: 'updated'}



'''Post api class to execute remove account functions'''
class remove(Resource):

    def post(self):

	args=post_parser.parse_args()
	remove = AccountDelete(args.name, args.usename, args.password, args.domain, args.theme)
	user =remove.DeleteUserDirectory()
 	return  {user: 'removed'}
	  
 

api.add_resource(create, '/create')
api.add_resource(update, '/update')
api.add_resource(remove, '/remove')


''' curl http://api.example.com -d "name=bob"-d "name=sue"-d "name=joe" '''


if __name__ == '__main__':

    app.run(debug=True)
