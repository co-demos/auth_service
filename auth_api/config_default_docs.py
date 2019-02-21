"""
config_default_docs.py  
- settings for the flask application object
"""

from log_config import log, pformat

### SYSTEM USER
default_system_user_list = [
	{
		"infos" : {
			"name" 		: "auth",
			"surname" 	: "Systems",
			"email"		: "auth.system@auth.com",
			"pseudo" 	: "system_user",
		},
		"specs" : {
			"doc_type"	: "usr",
		},
		"auth" : {
			"pwd" 		: "UNUSABLE_PASSWORD",
			"conf_usr" 	: True,
			"role"		: "system",
		}
	}
]
