# -*- encoding: utf-8 -*-

"""
_core/queries_db/__init__.py  
"""

from log_config import log, pformat
print()
log.debug(">>> _core.queries_db.__init__.py ..." )
log.debug(">>> queries_db ... loading mongodb collections as global variables")

from flask import current_app as app

from auth_api.application import mongo



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL VARIABLES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### declaring collections as app variables

mongo_users 				= mongo.db[ app.config["MONGO_COLL_USERS"] ]
mongo_jwt_blacklist = mongo.db[ app.config["MONGO_COLL_JWT_BLACKLIST"] ]


log.debug(">>> _core.queries_db.__init__.py / INDEXING COLLECTIONS ... " )

### drop previous text indexes (only one text index per collection)
main_text_fields_to_drop = '$**_text'
try :
	mongo_users.drop_index(main_text_fields_to_drop)
	mongo_jwt_blacklist.drop_index(main_text_fields_to_drop)
except:
	pass

# # create index for every collection needing it  
# # cf : https://api.mongodb.com/python/current/api/pymongo/collection.html?highlight=drop#pymongo.collection.Collection.create_index
# # cf : https://code.tutsplus.com/tutorials/full-text-search-in-mongodb--cms-24835 
# # cf (in open scraper) : self.coll_data.create_index([('$**', 'text')])
all_text_fields_index_name	= "all_fields"
all_text_fields_to_index 	= [('$**', 'text')]

main_text_fields_index_name	 = "main_fields"
main_text_fields_to_index = [
	("infos.title"				,"text") ,
	("infos.description"	,"text") ,
	("infos.licence"			,"text") ,
	("data_raw.f_code"		,"text") ,
	("data_raw.f_object"	,"text") ,
	("data_raw.f_code"		,"text") ,
	("data_raw.f_comments","text") ,
	("data_raw.f_data"		,"text") ,
	("data_raw.f_code"		,"text") ,
]


log.debug(">>> _core.queries_db.__init__.py / INDEXING COLLECTIONS : main fields... " )
mongo_users.create_index(					main_text_fields_to_index, name=main_text_fields_index_name)
mongo_jwt_blacklist.create_index(	main_text_fields_to_index, name=main_text_fields_index_name)


db_dict = {
					"mongo_users"					: mongo_users,
					"mongo_jwt_blacklist"	: mongo_jwt_blacklist,
			}
db_dict_by_type = {
					"usr"									: mongo_users,
					"jwt_blacklist"				: mongo_jwt_blacklist,
			}

def select_collection(coll_name):
	coll = db_dict[coll_name]
	return coll


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SERIALIZERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
class Marshaller :

	def __init__( self, ns, models ):
		
		self.ns 									= ns
		self.model_doc_out 				= models["model_doc_out"]
		self.model_doc_guest_out 	= models["model_doc_guest_out"]
		self.model_doc_min		 		= models["model_doc_min"]

		self.results_list					= None 

	def marshal_as_complete (self, results_list ) :

		ns 					= self.ns
		self.results_list 	= results_list
		log.debug('results_list ...' )  
		# log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_out)
		def get_results():
			return results_list
		return get_results()

	def marshal_as_guest (self, results_list ) :
	
		ns 					= self.ns
		self.results_list 	= results_list
		log.debug('results_list ...' )  
		# log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_guest_out)
		def get_results():
			return results_list
		return get_results()

	def marshal_as_min (self, results_list ) :
	
		ns 					= self.ns
		self.results_list 	= results_list
		log.debug('results_list ...' )  
		# log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_min)
		def get_results():
			return results_list
		return get_results()


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FINAL IMPORTS FOR QUERIES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from .query_doc import *
from .query_list import *
from .query_delete import *
from .query_update import *
from .query_insert_doc import *
# from .query_solidify import *
# from .query_build_dso import *

print()




"""
RESPONSE CODES 
cf : https://restfulapi.net/http-status-codes/

	200 (OK)
	201 (Created)
	202 (Accepted)
	204 (No Content)
	301 (Moved Permanently)
	302 (Found)
	303 (See Other)
	304 (Not Modified)
	307 (Temporary Redirect)
	400 (Bad Request)
	401 (Unauthorized)
	403 (Forbidden)
	404 (Not Found)
	405 (Method Not Allowed)
	406 (Not Acceptable)
	412 (Precondition Failed)
	415 (Unsupported Media Type)
	500 (Internal Server Error)
	501 (Not Implemented)

"""