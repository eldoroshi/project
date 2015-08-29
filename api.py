import validators

from itsdangerous import (TimedJSONWebSignatureSerializer 
				
			   as Serializer, BadSignature, SignatureExpired)

from functools import wraps

from flask import request, Response

from flask import Flask

from flask_restful import Resource, Api, fields, reqparse 

from account import *

from edit_account import *

from delete_account import *


app = Flask(__name__)

api = Api(app)

''' This is the secret key that will be used to encrypt token '''

app.config['SECRET_KEY'] = 'Look at me mother fucker'


''' Check the authentication that will be connected with db '''
def check_auth(username_token, password):

    '''This function is called to check if a username /

    password combination is valid.

    '''
    user = verify_token(username_token)

    if not user:		

    # Check username and password from db 
    
    	return username_token == 'ocean' and password == 'secret'
    
    else:	
		
	if user == '2':

    		return username_token == 'ocean'



def authenticate():

    "Sends a 401 response that enables basic auth"

    return Response(

    'Could not verify your access level for that URL.\n'

    'You have to login with proper credentials', 401,

    {'WWW-Authenticate': 'Basic realm="Login Required"'})


'''Get the authentication credentials '''
def requires_auth(f):

    @wraps(f)

    def decorated(*args, **kwargs):

        auth = request.authorization

        if not auth or not check_auth(auth.username, auth.password):

            return authenticate()

        return f(*args, **kwargs)

    return decorated


''' Generate the token for the authentetication '''
@app.route('/api/token')
@requires_auth
def generate_auth_token():

	s = Serializer(app.config['SECRET_KEY'], expires_in=3600)

        token = s.dumps({"id": "2"})
	
	return token


''' Verify the token if its the right one '''
@app.route('/api/check')
def verify_token(token):

	s = Serializer(app.config['SECRET_KEY'])

	try:
	 	data = s.loads(token)
		
	except:	
		 return None
	
	return data.get("id")

#Get username from the token	
def get_username():
	
	token = generate_auth_token()
        result = verify_token(token)
	if result != '2':
		return False
	return username ==  'admin'


def email(email_str):

	if validators.email(email_str):

		return email_str
	else:

	    return False


def string(valid_string):

	if valid_string.isalnum():

		return valid_string
	else:
	 	return False

def url(vdomain):

	if validators.url(vdomain):

		return vdomain
	else:
		return False
		



'''Parameters that will be posted on api'''
post_parser = reqparse.RequestParser()


post_parser.add_argument(

    'name', dest='name',
     
    location='form', help='The account name', 

    type=string


)

post_parser.add_argument(

    'username', dest='username',

    location='form', required=True,

    help='The user username', type=string

)

post_parser.add_argument(

    'email', dest='email',

    location='form', type=email,

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

     'newdomain', dest = 'newdomain',
     
     location = 'form', 
    
     help = 'The new domain', type = url	
		
	
)

post_parser.add_argument(

     'theme', dest='theme',

      location = 'form', required=True,

      help = 'Select the theme will be installed', type=string

) 	



'''Post api class to execute creation account functions '''
class create(Resource):

    
    def post(self):
        
	args = post_parser.parse_args()
        create = AccountCreation(args.name, args.username, args.password, args.domain, args.email, args.theme)        
	user = create.CreateUser()
        public_dir = create.publichtml_dir()
        virtualhosting = create.VirtualHosting()
        dnszone = create.dnszone()
        addzone = create.addzone()
        loadconfig = create.loadconfig()
 	createdb = create.createdb()
        downloadwp = create.downloadWP()
	installwp = create.installWP()
	installtheme = create.installtheme()
	 
	return {user : 'created'}
   			

'''Post api class to execute editing account functions '''
class updatepass(Resource):
    @requires_auth	
    def post(self):
	auth =  request.authorization       
	args = post_parser.parse_args()
	update = AccountEditing(auth.username, args.password, args.domain, args.newdomain, args.email, args.theme)
	user = update.EditUserPass()
	return {user: 'updated'}

class updatedomain(Resource):
    @requires_auth
    def post(self):
	auth = request.authorization
	args = post_parser.parse_args()
	update = AccountEditing(auth.username, args.password, args.domain, args.newdomain, args.theme)			
	virtualdomain = update.EditDomainVh()
	dnszone = update.EditDomainDns()
	wpdomain = update.EditDomainWp()
        return {virtualdomain: 'update', dnszone: 'update', wpdomain : 'update'}        

class updatewpass(Resource):
    @requires_auth
    def post(self):
        auth = request.authorization
	args = post_parser.parse_args()
        update = AccountEditing(auth.username, args.password, args.domain, args.newdomain, args.theme)  
        editwppass = update.EditPassWp()
        return {editwppass : 'update'}

class updatetheme(Resource):
    @requires_auth
    def post(self):
        auth = request.authorization
	args =post_parser.parse_args()
	update = AccountEditing(auth.username, args.password, args.domain, args.newdomain,  args.email, args.theme)	
	editwptheme = update.EditthemeWp()
	return {editwppass : 'update' } 


'''Post api class to execute remove account functions'''

class remove(Resource):
    
    @requires_auth 	
    def post(self):
	auth = request.authorization
	args=post_parser.parse_args()
	remove = AccountDelete(auth.username, args.password, args.domain, args.email, args.theme)
	user =remove.DeleteUserDirectory()
 	return  {user: 'removed'} 
	  
 
api.add_resource(create, '/create')
api.add_resource(updatepass, '/updatepass')
api.add_resource(updatedomain, '/updatedomain')
api.add_resource(updatewpass, '/updatewpass')
api.add_resource(updatetheme, '/updatetheme')
api.add_resource(remove, '/remove')


''' curl http://username:password@example.com -d "name=bob"-d "name=sue"-d "name=joe" '''


if __name__ == '__main__':

    app.run(debug=True)
