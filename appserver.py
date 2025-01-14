# -*- encoding: utf-8 -*-

"""
appserver.py  
- creates an application instance and runs the dev server
"""

import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### IMPORT COMMAND LINE INTERFACE (CLI) 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : http://click.pocoo.org/5/ 
import click

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SET LOGGER 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from log_config import log, pformat
# log.debug('>>> TESTING LOGGER')

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-SOCKETIO
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_socketio import SocketIO

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### RUN APPSERVER
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

@click.command()
@click.option('--mode', default="dev", nargs=1, help="The <mode> you need to run the app : dev (default), dev_email, prod, preprod" )
@click.option('--docker',  default="docker_off", nargs=1,  help="Are you running the app with <docker> : docker_off | docker_on" )
@click.option('--host', default="localhost", nargs=1,  help="The <host> name you want the app to run on : localhost(default) | <IP_NUMBER> " )
@click.option('--port', default="4100", nargs=1,  help="The <port> number you want the app to run on : 4100 (default) | <PORT_NUMBER>")
@click.option('--mongodb', default="local", nargs=1,  help="The <mongodb> you need to run the app : local | distant | server" )
@click.option('--rsa', default="no", nargs=1,  help="The <rsa> mode (RSA encrypt/decrypt for forms), protects '/login' + '/register' + '/password_forgotten' + '/reset_password': 'no' (default), 'yes'" )
@click.option('--anojwt', default="no", nargs=1, help="The <anojwt> mode (needs an anonymous JWT for login and register routes), affects '/login' + '/register' + '/password_forgotten' : 'no' (default), 'yes'" )
@click.option('--antispam', default="no", nargs=1, help="The <antispam> mode (add hidden field check for forms) protects '/login' + '/register' + '/password_forgotten' : 'no' (default), 'yes'" )
@click.option('--antispam_val', default="", nargs=1, help="The <antispam_val> to check in forms against spams : '' (default), <your-string-to-check>" )
@click.option('--https', default="false", nargs=1, help="The <https> mode you want the app to run on : true | false")
def app_runner(mode, docker, host, port, mongodb, rsa, anojwt, antispam, antispam_val, https) : 

  """ 
  runner for the TOKTOK backend Flask app 

  in command line just type : 
  "python appserver.py"

  you can also enter some arguments in the command line : 
  --mode : dev | dev_email | prod  | preprod
  --docker : docker_off | docker_on
  --host : localhost | <your_IP>
  --port : <your_favorite_port>
  --mongodb : local | distant | server
  --anojwt : yes | no
  --rsa : yes | no
  --antispam : yes | no
  --antispam_val  : '' | <your-string-to-check>
  --https : true | false

  """

  print()
  print("=== "*40)
  print("=== "*40)
  print("=== "*40)
  print()
  

  ### WARNING : CLIck will treat every input as string as defaults values are string too
  log.debug("\n=== CUSTOM CONFIG FROM CLI ===\n")
  log.debug("=== mode : %s", mode)
  log.debug("=== docker : %s", docker)
  log.debug("=== host : %s", host)
  log.debug("=== port : %s", port)
  log.debug("=== mongodb : %s", mongodb)
  log.debug("=== rsa : %s", rsa)
  log.debug("=== anojwt : %s", anojwt)
  log.debug("=== antispam : %s", antispam)
  log.debug("=== antispam_val : %s", antispam_val)
  log.debug("=== https   : %s", https)
  print()

  ### READ ENV VARS DEPENDING ON MODE
  if mode in ['dev', 'dev_email']:
    env_path_global = Path('.') / 'example.env.global'

    if mongodb in ['local'] : 
      env_path_mongodb = Path('.') / 'example.env.mongodb'
    else : 
      env_path_mongodb = Path('.') / '.env.mongodb'

    if mode == 'dev_email' : 
      env_path_mailing = Path('.') / '.env.mailing'
    else : 
      env_path_mailing = Path('.') / 'example.env.mailing'

  else : 
    env_path_global = Path('.') / '.env.global'
    env_path_mongodb = Path('.') / '.env.mongodb'
    env_path_mailing = Path('.') / '.env.mailing'

  load_dotenv(env_path_global, verbose=True)
  load_dotenv(env_path_mongodb, verbose=True)
  load_dotenv(env_path_mailing, verbose=True)

  ### OVERIDE AND SET UP ENV VARS FROM CLI 
  os.environ["DOMAIN_ROOT"]   = host
  os.environ["DOMAIN_PORT"]   = port
  os.environ["DOCKER_MODE"]   = docker
  os.environ["MONGODB_MODE"]  = mongodb


  log.debug("\n--- STARTING TOKTOK AUTH API ---\n")

  from auth_api.application import create_app

  app = create_app( 
    app_name='AUTH_API', 

    run_mode=mode, 
    docker_mode=docker,
    mongodb_mode=mongodb,

    RSA_mode=rsa, 
    anojwt_mode=anojwt, 
    antispam_mode=antispam,
    antispam_value=antispam_val
  )
  
  ### apply / overwrites host configuration
  if mode != "dev" : 
    log.debug("=== mode : %s", mode)
    # os.environ["FLASK_CONFIGURATION"] = str(mode)
    os.environ["RUN_MODE"] = str(mode)
    # config_name = os.getenv('FLASK_CONFIGURATION', 'dev') ### 'default' for local dev
    config_name = os.getenv('RUN_MODE', 'dev') ### 'default' for local dev
    log.debug("=== config_name : %s", config_name)

  app_debug = app.config["DEBUG"]

  ### initiate socketio
  socketio = SocketIO(app)

  # simple flask runner
  print()
  print("=== "*40)
  print("=== "*40)
  print("=== "*40)
  print()
  app.run( debug=app_debug, host=host, port=int(port), threaded=True )



if __name__ == '__main__':  

  app_runner()

else : 

  gunicorn_app = app_runner()
