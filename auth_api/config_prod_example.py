"""
config_prod_example.py  
- settings for the flask application object
"""

import os
from datetime import timedelta


class BaseConfig(object):  

	CODE_LINK					= "<a target='_blank' href='https://github.com/co-demos/toktok'>TokTok</a>"

	RUN_MODE					= "dev"
	DEBUG 						= True
	TEMPLATES_FOLDER 	= "/templates"
	ROOT_FOLDER				= os.getcwd()
	UPLOADS_FOLDER 		= ROOT_FOLDER+"/uploads/"
	UPLOADS_IMAGES 		= UPLOADS_FOLDER+"img/"
	UPLOADS_DATA 			= UPLOADS_FOLDER+"data_sources/"

	# used for encryption and session management

	""" RESTPLUS CONFIG """
	SWAGGER_UI_DOC_EXPANSION 		= 'list'
	SWAGGER_UI_JSONEDITOR 			= True
	SWAGGER_UI_OPERATION_ID 		= True
	SWAGGER_UI_REQUEST_DURATION = True

	""" APP SECRET KEY """
	SECRET_KEY					= "my_app_secret_key"

	""" SHARED JWT SECRET KEY """
	JWT_SECRET_KEY								= "your_JWT_secret_key"
	JWT_HEADER_NAME								= "Authorization" #"X-API-KEY"
	JWT_TOKEN_LOCATION						= ["headers", "query_string"]
	JWT_QUERY_STRING_NAME 				= "token"
	JWT_ACCESS_TOKEN_EXPIRES 			= timedelta(minutes=1440)
	JWT_REFRESH_TOKEN_EXPIRES 		= timedelta(days=10*365)  
	# JWT_IDENTITY_CLAIM					= "_id"
	### custom JWT expirations
	JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES				= timedelta(minutes=60)  
	JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES 	= timedelta(days=3)  
	JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES				= timedelta(days=1)  
	# beware not putting anything in JWT_HEADER_TYPE like 'Bearer', 
	# otherwise @jwt_required will look for an Authorization : Bearer <JWT> / 
	# not very comptatible with Flask-RestPlus authorization schemas described in _auth.authorizations.py
	JWT_HEADER_TYPE								= "" 

	# JWT_RENEW_REFRESH_TOKEN_AT_LOGIN			= True 

	REDIRECTION_FRONT		= "http://localhost:3000" 

	""" HOST """
	DOMAIN_ROOT				= "localhost" 
	DOMAIN_PORT				= "4100"
	SERVER_NAME				= "localhost:4100"  ### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
	DOMAIN_NAME				= "http://localhost:4100"
	SERVER_NAME_TEST	= "True" 

	""" MONGODB """
	MONGO_DBNAME										= 'auth'
	MONGO_URI												= 'mongodb://localhost:27017/auth'
	# collections
	MONGO_COLL_TAGS									= "tags"
	MONGO_COLL_USERS								= "users"
	MONGO_COLL_JWT_BLACKLIST				= "jwt_blacklist"


class DevEmail(BaseConfig) : 

	RUN_MODE				= "dev_email"

	JWT_RENEW_REFRESH_TOKEN_AT_LOGIN	= True 

	""" EMAILING """
	# email server
	MAIL_SERVER				= 'smtp.googlemail.com' 		# ... for instance
	MAIL_PORT 				= 465
	MAIL_USE_TLS 			= False
	MAIL_USE_SSL 			= True
	MAIL_USERNAME 		= "your.auth-instance.email-contact@my_email.com" # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD 		= "email_password_here" 		# os.environ.get('MAIL_PASSWORD')
	# administrator list
	ADMINS						= ['your.app.email@my_email.com']
	MAIL_DEFAULT_SENDER = 'your.app.email@my_email.com'

	""" ENCRYPTION FOR CONFIRMATION EMAIL """
	SECURITY_PASSWORD_SALT 	= 'my_precious_salt_security'


class Preprod(DevEmail) : 

	RUN_MODE			= "preprod"
	DEBUG 				= False 
	
	JWT_RENEW_REFRESH_TOKEN_AT_LOGIN	= False 

	REDIRECTION_FRONT		= "http://www.my-auth-frontend-preprod.com" 

	""" HOST - real prod IP and domain name"""
	DOMAIN_ROOT				= "XXX.XX.XX.XXX" 
	DOMAIN_PORT				= "4101"
	SERVER_NAME				= "XXX.XX.XX.XXX:4101"  		### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
	DOMAIN_NAME				= "http://your-auth-preprod-instance.com"
	SERVER_NAME_TEST	= "True" 

	""" MONGODB """
	MONGO_DBNAME		= 'auth_preprod'
	MONGO_USER 			= "mongo_admin_user"
	MONGO_PASS 			= "mongo_admin_user_password"
	MONGO_URI				= 'mongodb://mongo_admin_user_password:mongo_admin_user@127.0.0.1:27017/auth_preprod'


	""" EMAILING """
	# email server
	MAIL_SERVER				= 'smtp.googlemail.com' 		# ... for instance
	MAIL_PORT 				= 465
	MAIL_USE_TLS 			= False
	MAIL_USE_SSL 			= True
	MAIL_USERNAME 		= "your.auth-instance.email-contact@my_email.com" # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD 		= "email_password_here" 		# os.environ.get('MAIL_PASSWORD')
	# administrator list
	ADMINS						= ['your.app.email@my_email.com']
	MAIL_DEFAULT_SENDER = 'your.app.email@my_email.com'

	""" ENCRYPTION FOR CONFIRMATION EMAIL """
	SECURITY_PASSWORD_SALT 	= 'my_precious_salt_security'


class Prod(DevEmail) : 

	RUN_MODE			= "prod"
	DEBUG 				= False 
	
	JWT_RENEW_REFRESH_TOKEN_AT_LOGIN	= False 

	REDIRECTION_FRONT		= "http://www.my-auth-frontend.com" 

	""" HOST - real prod IP and domain name"""
	DOMAIN_ROOT				= "XXX.XX.XX.XXX" 
	DOMAIN_PORT				= "4000"
	SERVER_NAME				= "XXX.XX.XX.XXX:4100"  		### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
	DOMAIN_NAME				= "http://your-auth-instance.com"
	SERVER_NAME_TEST	= "True" 

	""" MONGODB """
	MONGO_DBNAME		= 'auth'
	MONGO_USER 			= "mongo_admin_user"
	MONGO_PASS 			= "mongo_admin_user_password"
	MONGO_URI				= 'mongodb://mongo_admin_user_password:mongo_admin_user@127.0.0.1:27017/auth'


	""" EMAILING """
	# email server
	MAIL_SERVER			= 'smtp.googlemail.com' 		# ... for instance
	MAIL_PORT 			= 465
	MAIL_USE_TLS 		= False
	MAIL_USE_SSL 		= True
	MAIL_USERNAME 	= "your.auth-instance.email-contact@my_email.com" # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD 	= "email_password_here" 		# os.environ.get('MAIL_PASSWORD')
	# administrator list
	ADMINS					= ['your.app.email@my_email.com']
	MAIL_DEFAULT_SENDER = 'your.app.email@my_email.com'

	""" ENCRYPTION FOR CONFIRMATION EMAIL """
	SECURITY_PASSWORD_SALT 	= 'my_precious_salt_security'