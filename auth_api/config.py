"""
config.py  
- settings for the flask application object
"""

import os
from datetime import timedelta

class BaseConfig(object):  

	RUN_MODE			= "dev"
	DEBUG					= True
	TEMPLATES_FOLDER 	= "/templates"
	ROOT_FOLDER				= os.getcwd()
	UPLOADS_FOLDER 		= ROOT_FOLDER+"/uploads"
	UPLOADS_IMAGES 		= UPLOADS_FOLDER+"/img"
	UPLOADS_DATA 			= UPLOADS_FOLDER+"/data_sources"
	
	# used for encryption and session management

	""" RESTPLUS CONFIG """
	SWAGGER_UI_DOC_EXPANSION 			= 'list'
	SWAGGER_UI_JSONEDITOR 				= True
	SWAGGER_UI_OPERATION_ID 			= True
	SWAGGER_UI_REQUEST_DURATION		= True

	""" APP SECRET KEY """
	SECRET_KEY						= "app_very_secret_key"

	""" SHARED JWT SECRET KEY : this key must be shared with openscraper and auth api """

	JWT_SECRET_KEY								= "a_key_youhouuuuuuu"
	JWT_HEADER_NAME								= "Authorization" #"X-API-KEY"
	JWT_TOKEN_LOCATION						= ["headers", "query_string"]
	JWT_QUERY_STRING_NAME 				= "token"
	JWT_ACCESS_TOKEN_EXPIRES 			= timedelta(minutes=720) # minutes=15
	JWT_REFRESH_TOKEN_EXPIRES 		= timedelta(days=10*365)  
	# JWT_IDENTITY_CLAIM					= "_id"
	### custom JWT expirations
	JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES			= timedelta(minutes=15)  
	JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES = timedelta(days=7)  
	JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES			= timedelta(days=1)  
	# beware not putting anything in JWT_HEADER_TYPE like 'Bearer', 
	# otherwise @jwt_required will look for an Authorization : Bearer <JWT> / 
	# not very comptatible with Flask-RestPlus authorization schemas described in _auth.authorizations.py
	JWT_HEADER_TYPE								= "" 

	JWT_RENEW_REFRESH_TOKEN_AT_LOGIN			= True 

	""" HOST """
	DOMAIN_ROOT							= "localhost" 
	DOMAIN_PORT							= "4100"
	SERVER_NAME							= "localhost:4100"  ### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
	DOMAIN_NAME							= "http://localhost:4100"
	SERVER_NAME_TEST				= "True" 

	""" MONGODB """
	MONGO_DBNAME							= 'auth'
	MONGO_URI									= 'mongodb://localhost:27017/auth'
	# collections
	MONGO_COLL_USERS					= "users"
	MONGO_COLL_JWT_BLACKLIST	= "jwt_blacklist"

	""" EMAILING """
	# email server
	MAIL_SERVER					= 'smtp.googlemail.com'
	MAIL_PORT 					= 465
	MAIL_USE_TLS 				= False
	MAIL_USE_SSL 				= True
	MAIL_USERNAME 			= os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD 			= os.environ.get('MAIL_PASSWORD')
	# administrator list
	ADMINS							= ['your-gmail-username@gmail.com']
	MAIL_DEFAULT_SENDER	= 'your-gmail-username@gmail.com'

	""" ENCRYPTION FOR CONFIRMATION EMAIL """
	SECURITY_PASSWORD_SALT 	= 'my_precious_salt_security'


class DevEmail(BaseConfig) : 

	RUN_MODE					= "dev_email"

	""" EMAILING """
	# email server
	MAIL_SERVER				= 'smtp.googlemail.com'
	MAIL_PORT 				= 465
	MAIL_USE_TLS 			= False
	MAIL_USE_SSL 			= True
	MAIL_USERNAME 		= "XXX.XXX@XXX.com" # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD 		= "XXXXX" # os.environ.get('MAIL_PASSWORD')
	# administrator list
	ADMINS							= ['XXXX.XXXX@gmail.com']
	MAIL_DEFAULT_SENDER = 'XXXX.XXXX@gmail.com'

	""" ENCRYPTION FOR CONFIRMATION EMAIL """
	SECURITY_PASSWORD_SALT 	= 'XXXXXXX'


class Prod(DevEmail) : 

	RUN_MODE				= "prod"
	DEBUG = False 

	""" HOST - prod IP and domain name"""
	DOMAIN_ROOT				= "XXX.XX.XX.XXX" 
	DOMAIN_PORT				= "4100"
	SERVER_NAME				= "XXX.XX.XX.XXX:4100"  ### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
	DOMAIN_NAME				= "http://XXXXX.com"
	SERVER_NAME_TEST	= "True" 

	""" MONGODB """
	MONGO_DBNAME			= 'auth'
	MONGO_URI					= 'mongodb://XXX.XX.XX.XXX:27017/auth'