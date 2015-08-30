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

''' Call the Account Creation class to load all the creation functions '''

def creation():
	
	args = post_parser.parse_args()
	create = AccountCreation(args.name, args.username, args.password, args.domain, args.email, args.theme)
	return create

''' Call the AccountEditing class to load all the update functions '''

@requires_auth 
def updates():
	
	
	auth =  request.authorization       
	args = post_parser.parse_args()
	update = AccountEditing(auth.username, args.password, args.domain, args.newdomain, args.email, args.theme)
	return update

@requires_auth
def delete():
	
	auth = request.authorization
	args=post_parser.parse_args()
	remove = AccountDelete(auth.username, args.password, args.domain, args.email, args.theme)
	return remove	





'''Post api class to execute creation account functions '''
class create(Resource):

    
	def post(self):
	
	        create = creation()
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
   			
		''' Create user on the system '''

class createuser(Resource):

	def post(self):

		create = creation()
		user =create.CreateUser()
		return {user: 'message'} 


''' Create public directory '''
class createdir(Resource):
	
	def post(self):

		create= creation()
		directory = create.publichtml_dir()
		return {directory: 'message'}

'''Create virtual hosting configuration for apache in sites.conf'''
class createvirtualhost(Resource):
	
	def post(self):
		
                create = creation() 
		virtualhost = create.VirtualHosting()
		return {virtualhost : 'message'}


''' Create dns configuration in named.conf.local '''
class createdns(Resource):
	
	def post(self):

		create = creation()
		dns =  create.dnszone()
		return {dns : 'message'}

'''Create dns zone file '''
class createzone(Resource):
	
	def post(self):
 
		create = creation()
		dnszone = create.addzone()
		return {dnszone : 'message'}


''' Reload dns and apache configuration withouth restart the service '''
class reload(Resource):
	
	def post(self):

		create = creation()
		config =  create.loadconfig()
		return {config : 'message'}


''' Create new db for the wordpress installation '''

class createdatabase(Resource):
	
	def post(self):
	
	 	create = creation()
		db = create.createdb()
		return {db : 'message'}
 
		

class downloadwordpress(Resource):

	def post(self):
		
		create = creation()
		downloadwp = create.downloadWP()
		return {downloadwp :  'message'}

''' Install Wordpress '''

class installwordpress(Resource):
	
	def post(self):
		
		create = creation()
		installwordpress = create.installWP()
		return {installwordpress : 'message' }

''' Install Wordpress Theme '''
class installwptheme(Resource):

	def post(self):
		
		
		create = creation()
		theme = create.installtheme()
		return {theme: 'message'}



'''Post api class to execute editing account functions '''
class updatepass(Resource):
    @requires_auth	
    def post(self):

	update = updates()
	user = update.EditUserPass()
	return {user: 'updated'}

''' Update domain in sites.conf(apache), update with new domain dns and wp db  '''

class updatedomain(Resource):
    @requires_auth
    def post(self):

	update = updates()
	virtualdomain = update.EditDomainVh()
	dnszone = update.EditDomainDns()
	wpdomain = update.EditDomainWp()
        return {virtualdomain: 'update', dnszone: 'update', wpdomain : 'update'}        

class updatewpass(Resource):
    @requires_auth
    def post(self):
        
	update = updates() 
        editwppass = update.EditPassWp()
        return {editwppass : 'update'}

class updatetheme(Resource):
    @requires_auth
    def post(self):
        
	update = updates()
	editwptheme = update.EditthemeWp()
	return {editwppass : 'update' } 


'''Post api class to execute remove account functions'''

class remove(Resource):
    
	@requires_auth 	
	def post(self):

		remove =  delete()		
		user = remove.DeleteUserDirectory()
		virtualhosting = remove.DeleteVirtualHosting()
		deletednszone =  remove.DeleteDnsZone()
		deletedb =  remove.DeleteDb()
		deleteuser = remove.DeleteUser()

 		return  {user: 'removed', virtualhosting: 'message', deletednszone : 'message', deletedb : 'message', deleteuser :  'deleteuser'} 


''' Delete user directory '''
class deletedir(Resource):	  
 
	@requires_auth
	def post(self):

		remove  =  delete()	
        	user = remove.DeleteUserDirectory()
		return {user: 'removed'}
		
''' Delete virtual hosting  '''

class deletevirtualhosting(Resource):
	
	@requires_auth
	def post(self):
		
		remove = delete()
		virtualhosting  = remove.DeleteVirtualHosting()
		return {virtualhosting :  'message'} 	

''' Delete dns record zone '''

class  deletedns(Resource):
	
	@requires_auth
	def post(self):
		
		remove  = delete()
		dnszone = remove.DeleteDnszone()
		return {dnszone : 'message'}


''' Delete wordpress user database '''

class  deletedatabase(Resource):

	@requires_auth
	def post(self):

		remove = delete()
		db = remove.DeleteDb()
		return {db : 'message'}


class deleteuser(Resource):
	
	@requires_auth
	def post(self):

		remove = delete()
		user =  remove.DeleteUser()
		return {user : 'message'}


api.add_resource(create, '/create')
api.add_resource(createuser, '/createuser')
api.add_resource(createdir, '/createdir')
api.add_resource(createvirtualhost, '/createvirtualhost')
api.add_resource(createdns, '/createdns')
api.add_resource(createzone, '/createzone')
api.add_resource(reload, '/reload')
api.add_resource(createdatabase, '/createdatabase')
api.add_resource(downloadwordpress, '/downloadwordpress')
api.add_resource(installwordpress, '/installwordpress')
api.add_resource(installwptheme, '/installwptheme')
api.add_resource(updatepass, '/updatepass')
api.add_resource(updatedomain, '/updatedomain')
api.add_resource(updatewpass, '/updatewpass')
api.add_resource(updatetheme, '/updatetheme')
api.add_resource(remove, '/remove')
api.add_resource(deletedir, '/deletedir')
api.add_resource(deletevirtualhosting, '/deletevirtualhosting')
api.add_resource(deletedns, '/deletedns')
api.add_resource(deletedatabase, '/deletedatabase')
api.add_resource(deleteuser, '/deleteuser')



''' curl http://username:password@example.com -d "name=bob"-d "name=sue"-d "name=joe" '''


if __name__ == '__main__':

    app.run(debug=True)
