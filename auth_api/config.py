"""
config.py  
- settings for the flask application object
"""

import os
from datetime import timedelta

config_name    = os.getenv('FLASK_CONFIGURATION', 'dev')
config_mongodb = os.getenv('MONGODB_MODE',        'local')
config_docker  = os.getenv('DOCKER_MODE',         'docker_off')

print()
print("$ config_name : ", config_name)  
print("$ config_mongodb : ", config_mongodb)  
print("$ config_docker : ", config_docker)  

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### READ ENV VARS / MONGO
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

MONGO_ROOT_LOCAL           = os.getenv('MONGO_ROOT_LOCAL') # "localhost"
MONGO_ROOT_DOCKER          = os.getenv('MONGO_ROOT_DOCKER') # "host.docker.internal"

MONGO_PORT_LOCAL           = os.getenv('MONGO_PORT_LOCAL') # "27017"

MONGO_ROOT_SERVER          = os.getenv('MONGO_ROOT_SERVER') # "127.0.0.1" # IP depending on your server's mongoDB configuration
MONGO_PORT_SERVER          = os.getenv('MONGO_PORT_SERVER') # "27017"
MONGO_USER_SERVER          = os.getenv('MONGO_USER_SERVER') # "MY-MONGODB-SERVER-ADMIN-USER"
MONGO_PASS_SERVER          = os.getenv('MONGO_PASS_SERVER') # "MY-SERVER-MONGODB-PASSWORD"
MONGO_OPTIONS_SERVER       = os.getenv('MONGO_OPTIONS_SERVER') # ""

MONGO_DISTANT_URI          = os.getenv('MONGO_DISTANT_URI') # "mongodb://<DISTANT-USERNAME>:<DISTANT-PASSWORD>@<DISTANT-HOST>:<DISTANT-PORT>"  
MONGO_DISTANT_URI_OPTIONS  = os.getenv('MONGO_DISTANT_URI_OPTIONS') # "?ssl=true&replicaSet=<REPLICA-SET>&authSource=admin&retryWrites=true"



# temporary dicts
mongodb_roots_dict = {
  "local"  : { 
    "docker_off" : MONGO_ROOT_LOCAL,  
    "docker_on"  : MONGO_ROOT_DOCKER  
  },
  "server" : { 
    "docker_off" : MONGO_ROOT_SERVER, 
    "docker_on"  : MONGO_ROOT_DOCKER  
  },
}

mongodb_ports_dict = {
  "local"  : MONGO_PORT_LOCAL,
  "server" : MONGO_PORT_SERVER,
}
  
# mongodb_dbnames_dict = {
#   "dev"        : 'toktok',
#   "dev_email"  : 'toktok',
#   "preprod"    : 'toktok-preprod',
#   "prod"       : 'toktok-prod',
# }
mongodb_dbnames_dict = {
  "dev"       : os.getenv("MONGO_DBNAME", "toktok"),
  "dev_email" : os.getenv("MONGO_DBNAME", "toktok"),
  "preprod"   : os.getenv("MONGO_DBNAME_PREPROD", "toktok-preprod"),
  "prod"      : os.getenv("MONGO_DBNAME_PROD",    "toktok-prod")
}
### get DB name
mongodb_dbname = mongodb_dbnames_dict[config_name]

if config_mongodb == "distant" :
  mongodb_uri = "{}/{}{}".format(MONGO_DISTANT_URI, mongodb_dbname, MONGO_DISTANT_URI_OPTIONS)

else : 
  mongodb_root = mongodb_roots_dict[config_mongodb][config_docker]
  mongodb_port = mongodb_ports_dict[config_mongodb]

  ### get login if mongodb hosted on a server
  mongodb_login = "" 
  mongodb_options = "" 
  if config_name == "server" : 
    mongodb_login = "{}:{}@".format(MONGO_USER_SERVER, MONGO_PASS_SERVER)
    mongodb_options = MONGO_OPTIONS_SERVER ### must begin with "?"

  mongodb_uri = "mongodb://{}{}:{}/{}{}".format(mongodb_login, mongodb_root, mongodb_port, mongodb_dbname, mongodb_options)

print(" --- MONGODB_URI : ", mongodb_uri) 
os.environ["MONGODB_URI"] = mongodb_uri 


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

def formatEnvVar(var_name, format_type='boolean', separator=',') : 

  # print("formatEnvVar / var_name : ", var_name)
  env_var = os.getenv(var_name)
  # print("formatEnvVar / env_var : ", env_var)

  if format_type == 'boolean' : 
    if env_var in ['yes', 'Yes', 'YES', 'true', 'True', 'TRUE', '1'] : 
      return True
    else :
      return False
  
  elif format_type == 'integer' : 
    return int(env_var)

  elif format_type == 'float' : 
    return float(env_var)

  elif format_type == 'list' : 
    return env_var.split(separator)

  else : 
    if env_var in ['none', 'None', 'NONE', 'nan', 'Nan', 'NAN', 'null', 'Null','NULL', 'undefined'] : 
      return None
    else : 
      return env_var


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

class BaseConfig(object):  

  CODE_LINK = "<a target='_blank' href='https://github.com/co-demos/toktok'>TokTok</a>"

  RUN_MODE = os.getenv("RUN_MODE")

  DEBUG = formatEnvVar('DEBUG', format_type='boolean') # True


  """ HOST """
  # SERVER_NAME              = "localhost:4100"  ### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
  SERVER_NAME_TEST           = "True" 

  DOMAIN_ROOT =  os.getenv("DOMAIN_ROOT")
  DOMAIN_PORT =  formatEnvVar("DOMAIN_PORT", format_type='integer')

  if config_docker != 'docker_on' : 
    http_mode = "http"
    if formatEnvVar("HTTPS_MODE", format_type='boolean') == True : 
      http_mode = "https"

    os.environ["SERVER_NAME"]   = DOMAIN_ROOT + ":" + str(DOMAIN_PORT)
    os.environ["DOMAIN_NAME"]   = http_mode + "://" + DOMAIN_ROOT + ":" + str(DOMAIN_PORT)
    DOMAIN_NAME =  os.getenv("DOMAIN_NAME")


  TEMPLATES_FOLDER   = "/templates"
  ROOT_FOLDER        = os.getcwd()
  UPLOADS_FOLDER     = ROOT_FOLDER+"/uploads"
  UPLOADS_IMAGES     = UPLOADS_FOLDER+"/img"
  UPLOADS_DATA       = UPLOADS_FOLDER+"/data_sources"
  
  # used for encryption and session management

  """ RESTPLUS CONFIG """
  SWAGGER_UI_DOC_EXPANSION      = 'list'
  SWAGGER_UI_JSONEDITOR         = True
  SWAGGER_UI_OPERATION_ID       = True
  SWAGGER_UI_REQUEST_DURATION   = True

  """ APP SECRET KEY """
  SECRET_KEY = os.getenv("SECRET_KEY") # "app_very_secret_key"

  """ SHARED JWT SECRET KEY : this key must be shared with openscraper and auth api """

  JWT_SECRET_KEY                = os.getenv("JWT_SECRET_KEY") # "a_key_youhouuuuuuu"
  JWT_HEADER_NAME               = "Authorization" #"X-API-KEY"
  JWT_TOKEN_LOCATION            = ["headers", "query_string"]
  JWT_QUERY_STRING_NAME         = "token"

  JWT_ACCESS_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_ACCESS_TOKEN_EXPIRES", format_type='integer')
  JWT_ACCESS_TOKEN_EXPIRES      = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES_VAL) # minutes=15
  
  JWT_REFRESH_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_REFRESH_TOKEN_EXPIRES", format_type='integer')
  JWT_REFRESH_TOKEN_EXPIRES     = timedelta(days=JWT_REFRESH_TOKEN_EXPIRES_VAL*365)  

  # JWT_IDENTITY_CLAIM          = "_id"
  ### custom JWT expirations

  JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES", format_type='integer')
  JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES      = timedelta(minutes=JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_VAL)

  JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES", format_type='integer')
  JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES  = timedelta(days=JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES_VAL)

  JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES", format_type='integer')
  JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES       = timedelta(days=JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES_VAL)  
  # beware not putting anything in JWT_HEADER_TYPE like 'Bearer', 
  # otherwise @jwt_required will look for an Authorization : Bearer <JWT> / 
  # not very comptatible with Flask-RestPlus authorization schemas described in _auth.authorizations.py
  JWT_HEADER_TYPE  = "" 

  JWT_RENEW_REFRESH_TOKEN_AT_LOGIN  = formatEnvVar('JWT_RENEW_REFRESH_TOKEN_AT_LOGIN', format_type='boolean') # False 


  """ MONGODB """
  MONGO_URI  = os.getenv("MONGODB_URI")
  # collections
  MONGO_COLL_TAGS           = os.getenv("MONGO_COLL_TAGS") # "tags"
  MONGO_COLL_USERS          = os.getenv("MONGO_COLL_USERS") # "users"
  MONGO_COLL_LICENCES       = os.getenv("MONGO_COLL_LICENCES") # "licences"
  MONGO_COLL_JWT_BLACKLIST  = os.getenv("MONGO_COLL_JWT_BLACKLIST") # "jwt_blacklist"


  """ EMAILING """
  # email server
  MAIL_SERVER        = os.getenv('MAIL_SERVER') # 'smtp.googlemail.com'
  MAIL_PORT          = formatEnvVar('MAIL_PORT', format_type='integer') # 465
  MAIL_USE_TLS       = formatEnvVar('MAIL_USE_TLS', format_type='boolean') # False
  MAIL_USE_SSL       = formatEnvVar('MAIL_USE_SSL', format_type='boolean') # True
  MAIL_USERNAME      = os.getenv('MAIL_USERNAME') # "XXX.XXX@XXX.com" # os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD      = os.getenv('MAIL_PASSWORD') # "XXXXX" # os.environ.get('MAIL_PASSWORD')

  # administrator list
  ADMINS              = formatEnvVar('MAIL_ADMINS', format_type='list') # ['XXXX.XXXX@gmail.com']
  MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') # 'XXXX.XXXX@gmail.com'

  """ ENCRYPTION FOR CONFIRMATION EMAIL """
  SECURITY_PASSWORD_SALT   = os.getenv('SECURITY_PASSWORD_SALT') # 'XXXXXXX'



class Preprod(BaseConfig) : 


  REDIRECTION_FRONT  = os.getenv('REDIRECTION_FRONT_PREPROD')# "http://preprod.toktok.co-demos.com" 

  """ EMAILING """
  # MAIL_PORT        = 587
  MAIL_PORT        = formatEnvVar('MAIL_PORT', format_type='integer') # 465
  # MAIL_USE_TLS     = True
  # MAIL_USE_SSL     = False
  MAIL_USE_TLS       = formatEnvVar('MAIL_USE_TLS', format_type='boolean') # False
  MAIL_USE_SSL       = formatEnvVar('MAIL_USE_SSL', format_type='boolean') # True

  """ HOST - prod IP and domain name"""
  SERVER_NAME_TEST   = "True" 



class Prod(BaseConfig) : 


  REDIRECTION_FRONT    = os.getenv('REDIRECTION_FRONT_PROD')# "http://toktok.co-demos.com" 

  """ EMAILING """
  # MAIL_PORT        = 587
  MAIL_PORT        = formatEnvVar('MAIL_PORT', format_type='integer') # 465
  # MAIL_USE_TLS     = True
  # MAIL_USE_SSL     = False
  MAIL_USE_TLS       = formatEnvVar('MAIL_USE_TLS', format_type='boolean') # False
  MAIL_USE_SSL       = formatEnvVar('MAIL_USE_SSL', format_type='boolean') # True

  """ HOST - prod IP and domain name"""
  SERVER_NAME_TEST   = "True" 
