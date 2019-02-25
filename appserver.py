# -*- encoding: utf-8 -*-

"""
appserver.py  
- creates an application instance and runs the dev server
"""

import os

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
@click.option('--mode', 				default="dev", 	nargs=1,	help="The <mode> you need to run the app : dev (default), dev_email, prod, preprod" )
@click.option('--port', 				default="None", nargs=1,	help="The <port> number you want the app to run on : 4100 (default=None) | <PORT_NUMBER>")
@click.option('--host', 				default="None", nargs=1,	help="The <host> name you want the app to run on : localhost(default=None) | <IP_NUMBER> " )
@click.option('--rsa', 					default="no", 	nargs=1,	help="The <rsa> mode (RSA encrypt/decrypt for forms), 												 protects '/login' + '/register' + '/password_forgotten' + '/reset_password': 'no' (default), 'yes'" )
@click.option('--anojwt', 			default="no", 	nargs=1,	help="The <anojwt> mode (needs an anonymous JWT for login and register routes), affects '/login' + '/register' + '/password_forgotten' : 'no' (default), 'yes'" )
@click.option('--antispam', 		default="no",		nargs=1,	help="The <antispam> mode (add hidden field check for forms)									 protects '/login' + '/register' + '/password_forgotten' : 'no' (default), 'yes'" )
@click.option('--antispam_val', default="", 		nargs=1,	help="The <antispam_val> to check in forms against spams : '' (default), <your-string-to-check>" )
def app_runner(mode, host, port, rsa, anojwt, antispam, antispam_val) : 

	""" 
	runner for the TOKTOK backend Flask app 

	in command line just type : 
	"python appserver.py"

	you can also enter some arguments in the command line : 
	--mode 					: dev | prod | dev_email 
	--host					: localhost | <your_IP>
	--port					: <your_favorite_port>
	--anojwt 				: yes | no
	--rsa 					: yes | no
	--antispam			: yes | no
	--antispam_val	: '' | <your-string-to-check>

	"""

	print()
	print("=== "*40)
	print("=== "*40)
	print("=== "*40)
	print()
	

	### WARNING : CLIck will treat every input as string as defaults values are string too
	log.debug("\n=== CUSTOM CONFIG FROM CLI ===\n")
	log.debug("=== mode			: %s", mode)
	log.debug("=== host 		: %s", host)
	log.debug("=== port 		: %s", port)
	log.debug("=== rsa 			: %s", rsa)
	log.debug("=== anojwt 	: %s", anojwt)
	log.debug("=== antispam 		: %s", antispam)
	log.debug("=== antispam_val : %s", antispam_val)
	print()


	log.debug("\n--- STARTING TOKTOK AUTH API ---\n")

	from auth_api.application import create_app

	app = create_app( 
		app_name='AUTH_API', 
		run_mode=mode, 
		RSA_mode=rsa, 
		anojwt_mode=anojwt, 
		antispam_mode=antispam,
		antispam_value=antispam_val
	)
	
	### apply / overwrites host configuration
	if host == "None" : 
		app_host 	= app.config["DOMAIN_ROOT"]
	else : 
		app_host 	= host

	### apply / overwrites port configuration
	if port == "None" : 
		app_port 	= int(app.config["DOMAIN_PORT"])
	else : 
		app_port 	= port

	app_debug = app.config["DEBUG"]

	### initiate socketio
	socketio = SocketIO(app)

	# simple flask runner
	print()
	print("=== "*40)
	print("=== "*40)
	print("=== "*40)
	print()
	app.run( debug=app_debug, host=app_host, port=app_port, threaded=True )



if __name__ == '__main__':  

	app_runner()

else : 

	gunicorn_app = app_runner()
