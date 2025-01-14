# -*- encoding: utf-8 -*-

"""
application.py  
- creates a Flask app instance and registers the database object
"""

from log_config import log, pprint, pformat
log.debug ("... starting app ...")

from flask import Flask, g, current_app


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-EXTENDED-JWT IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : https://github.com/vimalloc/flask-jwt-extended/issues/14
from flask_jwt_extended import JWTManager

# declare JWT empty connector
jwt_manager = JWTManager()
log.debug("... jwt_manager() ...")
# log.debug(" jwt_manager() : \n%s ", pformat(jwt_manager))


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### LOGIN MANAGER 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# from    flask_login import   LoginManager, login_user, logout_user, login_required, \
#         current_user


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-ADMIN IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# from  flask_admin               import Admin, AdminIndexView
# from   flask_admin.model         import typefmt
# from   flask_admin.model.widgets import XEditableWidget


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-CORS IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_cors import CORS, cross_origin


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-PYMONGO IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_pymongo import PyMongo

# declare mongo empty connector
mongo = PyMongo()
# log.debug("... mongo : \n%s", pformat(mongo.__dict__))


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-MAIL IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_mail import Mail
mail = Mail()
# log.debug("... mail : \n%s", pformat(mail.__dict__))



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CREATE APP
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# application factory, see: http://flask.pocoo.org/docs/patterns/appfactories/

def create_app( 
                app_name='TOKTOK_AUTH_API', 

                run_mode="dev", 
                docker_mode="docker_off",
                mongodb_mode="local",

                antispam_mode="no", 
                antispam_value="", 
                RSA_mode="no", 
                anojwt_mode="no"  
              ):  

  log.debug ("... creating app ...")

  ### create Flask app
  app = Flask(app_name)


  ### load config 
  if run_mode == "prod" :   
    # app.config.from_object('auth_api.config_prod.Prod')
    app.config.from_object('auth_api.config.Prod')
  
  elif run_mode == "preprod" : 
    # app.config.from_object('auth_api.config_prod.Preprod')
    app.config.from_object('auth_api.config.Preprod')
  
  else : ### for instance "dev" or "default" or whatever not above ... mode will be considered as "dev" by the config.py file
    app.config.from_object('auth_api.config.BaseConfig')





  # ### SET UP MONGO DB URI, DB, AND CONNECTOR

  # from .config import mongodb_roots_dict, mongodb_ports_dict, mongodb_dbnames_dict

  # # directly get URI if distant
  # if mongodb_mode == 'distant' : 
  #   from .config import MONGO_DISTANT_URI, MONGO_DISTANT_URI_OPTIONS
  #   db_name = mongodb_dbnames_dict[run_mode]
  #   mongodb_uri = "{}/{}{}".format(MONGO_DISTANT_URI, db_name, MONGO_DISTANT_URI_OPTIONS)
  
  # # get local URI if server or local
  # else :

  #   mongodb_login = "" 
  #   mongodb_options = "" 

  #   if mongodb_mode == 'server' : 
  #     from .config import MONGO_USER_SERVER, MONGO_PASS_SERVER, MONGO_OPTIONS_SERVER
  #     ### get login if mongodb hosted on a server
  #     mongodb_login = "{}:{}@".format(MONGO_USER_SERVER, MONGO_PASS_SERVER)
  #     mongodb_options = MONGO_OPTIONS_SERVER ### must begin with "?"
      
  #   # else :  # if mongodb_mode == 'local' : 
  #   #   from .config import mongodb_roots_dict, mongodb_ports_dict, mongodb_dbnames_dict

  #   mongodb_root = mongodb_roots_dict[mongodb_mode][docker_mode]
  #   mongodb_port = mongodb_ports_dict[mongodb_mode]
  #   mongodb_dbname = mongodb_dbnames_dict[run_mode]

  #   mongodb_uri = "mongodb://{}{}:{}/{}{}".format(mongodb_login, mongodb_root, mongodb_port, mongodb_dbname, mongodb_options)

  # app.config["MONGO_URI"] = mongodb_uri


  ### append SALT / ANOJWT / ANTISPAM / ANTISPAM_VAL env vars to config 
  app.config["RSA_MODE"]         = RSA_mode
  app.config["ANOJWT_MODE"]      = anojwt_mode
  app.config["ANTISPAM_MODE"]    = antispam_mode
  app.config["ANTISPAM_VALUE"]   = antispam_value

  print()
  log.debug("... app.config :\n %s", pformat(app.config))
  print()


  ### init JWT manager
  log.debug("... init jwt_manager ...")
  jwt_manager.init_app(app)

  ### init mongodb client
  log.debug("... init mongo ...")
  # cf : https://flask-pymongo.readthedocs.io/en/latest/#flask_pymongo.PyMongo.init_app 
  # init_app(app, uri=None, *args, **kwargs)¶
  # If uri is None, and a Flask config variable named MONGO_URI exists, use that as the uri as above.
  # You must now use a MongoDB URI to configure Flask-PyMongo
  mongo.init_app(app)  ### 

  ### init mail client
  if run_mode != 'dev' : 
    log.debug("... init mail ...")
    mail.init_app(app)


  with app.app_context() :


    # import async functions and decorators
    from auth_api._core.async_tasks import async

    # access mongodb collections
    from auth_api._core.queries_db import ( 
        
      db_dict, db_dict_by_type,
      Query_db_list,
      Query_db_doc,
      Query_db_delete,

      mongo_users,

      mongo_jwt_blacklist,
      mongo_tags,
      mongo_licences,
      
      # mongo_corr_dicts   ### all cd are treated as ds_i
    ) 

    # import token required functions
    from auth_api._auth import authorizations #, token_required
    # from auth_api._auth.authorizations import * #, token_required

    # import emailing functions
    from auth_api._core.emailing import send_email, send_async_email 

    ## DEBUGGING / test
    print()
    find_one_user = mongo_users.find({'infos.name': "auth"})
    log.debug("DEBUG : find_one_user : \n%s", pformat(list(find_one_user)))


    ### registering all blueprints
    print()
    log.debug("... registering blueprints ...")
    from auth_api.api.api_users     import blueprint as api_users
    app.register_blueprint( api_users, url_prefix="/api/usr" )

    from auth_api.api.api_auth   import blueprint as api_auth
    app.register_blueprint( api_auth, url_prefix='/api/auth')





    ### init CORS 
    from auth_api._core.cors import CORS

    ### DEBUG
    # @app.before_request
    # def debug_stuff():
    #   # pass
    #   log.debug ("\n%s", pformat(current_app.__dict__))


  return app