# -*- encoding: utf-8 -*-

"""
_core/emailing/__init__.py  
- provides the EMAILING 
"""

from log_config import log, pformat
print()
log.debug(">>> _core.emailing.__init__.py ..." )
log.debug(">>> emailing ... loading emailing functions as global variables")

from threading import Thread

from flask import current_app

from flask_mail import Message

from auth_api.application import mail
from auth_api._core.async_tasks import async


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### EMAILING FUNCTIONS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html
# cf : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support 
# cf : https://stackoverflow.com/questions/11047307/run-flask-mail-asynchronously/18407455#18407455 


@async
def send_async_email(curr_app, msg):
	"""
  send an email asynchronously due to the decorator
	"""
	log.debug("... sending async email...")
	log.debug("... msg : \n%s", pformat(msg))
	
	with curr_app.app_context():
		mail.send(msg)


def send_email( subject, 
								to, 
								sender = current_app.config["MAIL_DEFAULT_SENDER"], 
								template = None ) :
	"""
	generic function to send an email 
	"""

	log.debug("... sending email...")

	msg 	= Message( 
		subject, 
		recipients	= [to], 
		sender			= sender, 
		html				= template,
	)

	app = current_app._get_current_object()
	### cf : http://flask.pocoo.org/docs/0.12/reqcontext/#notes-on-proxies

	### simple and synchronous run
	# mail.send(msg)

	### asynchronous run
	# thr = Thread(target=send_async_email, args=[app, msg])
	# thr.start()

	### asynchronous run based on send_async_email and async decorator
	send_async_email(app, msg)
