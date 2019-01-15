# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_solidify.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_solidify.py ..." )

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict
from 	solidata_api._core.solidify import *


import sys

def str_to_class(classname):
	return getattr(sys.modules[__name__], classname)


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO ENRICH ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_solidify (
		ns, 
		models,
		document_type,
		doc_id,
		claims,
		roles_for_complete 	= ["admin"],
		payload 			= {}
	):

	print()
	print("-+- "*40)
	log.debug("... _core.queries_db.Query_db_solidify.py ..." )

	### get mongodb collections
	prj_collection		= db_dict_by_type['prj']
	dmt_collection		= db_dict_by_type['dmt']
	dmf_collection		= db_dict_by_type['dmf']
	dsi_collection		= db_dict_by_type['dsi']
	rec_collection		= db_dict_by_type['rec']


	### prepare marshaller 
	# marshaller = Marshaller(ns, models)

	### default values
	db_collection		= db_dict_by_type[document_type]
	document_type_full 	= doc_type_dict[document_type]
	user_id = user_oid	= None
	user_role			= "anonymous"
	document_out		= None
	message 			= None
	dft_open_level_show = ["open_data"]
	response_code		= 200

	if claims or claims!={}  :
		user_role 		= claims["auth"]["role"]
		user_id	 		= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 	= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]

	### retrieve doc (PRJ f.e.) from db
	if ObjectId.is_valid(doc_id) : 
		doc_oid			= ObjectId(doc_id)
		document 		= db_collection.find_one( {"_id": doc_oid } )
		log.debug( "document : \n%s", pformat(document) )
	else :
		response_code	= 400
		document		= None

	### sum up all query arguments
	query_resume = {
		"document_type"		: document_type,	
		"doc_id" 			: doc_id,
		"user_id" 			: user_id,
		"user_role"			: user_role,
		"is_member_of_team" : False,
		"payload" 			: payload
	}

	if document : 

		### check doc's specs : public_auth, team...
		doc_open_level_edit = document["public_auth"]["open_level_edit"]
		log.debug( "doc_open_level_edit : %s", doc_open_level_edit )
		
		### get doc's team infos
		if "team" in document : 
			team_oids = [ t["oid_usr"] for t in document["team"] ]
			log.debug( "team_oids : \n%s", pformat(team_oids) )


		### marshal out results given user's claims / doc's public_auth / doc's team ... 
		
		# for admin or members of the team --> complete infos model
		if user_role in roles_for_complete or user_oid in team_oids : 
			
			log.debug( "payload : \n%s", pformat(payload) )
			payload_data = payload[0]

			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			### OPERATIONS RELATED TO DOCUMENT
			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			documents = {
				"src_doc" : document
			}

			is_complex_rec 	= payload_data.get( "is_complex_rec", False )
			
			if is_complex_rec : 

				### get datasets from document
				datasets = document["datasets"]
				dmt_refs = datasets["dmt_list"]
				dsi_refs = datasets["dsi_list"]

				### load DMT from db
				dmt_doc 				= dmt_collection.find_one( {"_id" : dmt_refs[0]["oid_dmt"] } )
				documents["dmt_doc"]	= dmt_doc
				log.debug( "dmt_doc loaded ... " )

				dmt_dmf_refs 			= dmt_doc["datasets"]["dmf_list"]
				dmf_oids 				= [ dmf_ref["oid_dmf"] for dmf_ref in dmt_dmf_refs ]
				dmf_list_cursor 		= dmf_collection.find({"_id" : {"$in" : dmf_oids} })
				dmf_list 				= list(dmf_list_cursor)
				documents["dmf_list"]	= dmf_list
				log.debug( "dmf_list loaded ... " )

				### load DSI from db
				dsi_oids 		= [ dsi_ref["oid_dsi"] for dsi_ref in dsi_refs ]
				dsi_list_cursor = dsi_collection.find({"_id" : {"$in" : dsi_oids} })
				dsi_list 		= list(dsi_list_cursor)
				documents["dsi_list"]	= dsi_list
				log.debug( "dsi_list loaded ... " )


			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			### OPERATIONS RELATED TO RECIPE
			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

			### get recipe id to run from payload
			recipe_to_run = payload_data["id_rec"]
			log.debug( "recipe_to_run : %s", recipe_to_run )

			rec_oid = ObjectId(recipe_to_run)
			log.debug( "rec_oid : %s", rec_oid )

			### retrieve recipe params from doc's mapping
			map_rec_list = document["mapping"]["map_rec"]
			# log.debug( "map_rec_list : \n%s", pformat(map_rec_list) )
			rec_params = next( item for item in map_rec_list if item["oid_rec"] == rec_oid )
			rec_params_ = rec_params["rec_params"]
			log.debug( "rec_params_ : \n%s", pformat(rec_params_) )

			need_add_dmf = rec_params_.get('new_dmfs_list', False)
			if need_add_dmf : 
				new_dmf_oids 					= [ ObjectId(dmf_ref["oid_dmf"]) for dmf_ref in need_add_dmf ]
				new_dmf_list_cursor 			= dmf_collection.find({"_id" : {"$in" : new_dmf_oids} })
				new_dmf_list 					= list(new_dmf_list_cursor)
				rec_params_["new_dmfs_list"]	= new_dmf_list

			### retrieve recipe from db
			recipe_doc = rec_collection.find_one( { "_id" : rec_oid })
			log.debug( "recipe_doc : \n%s", pformat(recipe_doc) )
			documents["rec_doc"]	= recipe_doc

			### choose the function to run from recipe_doc in db
			recipe_map			= recipe_doc["mapping"]["map_func"][0]

			recipe_func_class 	= recipe_map["function_class"]
			log.debug( "recipe_func_class : %s", recipe_func_class )

			recipe_func_runner 	= recipe_map["function_runner"]
			log.debug( "recipe_func_runner : %s", recipe_func_runner )


			### load the function & pass the parameters

			# Get class from globals and create an instance
			# log.debug( "globals() : \n%s", pformat(globals()) )
			module = globals()[recipe_func_class]( src_docs=documents, rec_params=rec_params_, is_complex_rec=is_complex_rec)

			# Get the function (from the instance) that we need to call to run the function
			solidify_func = getattr(module, recipe_func_runner)

			### run the solidifying function
			solidify_func()



			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			### OPERATIONS RELATED TO RESPONSE
			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

			### send back updated document
			document_updated 	= db_collection.find_one( {"_id": ObjectId(doc_id) } )
			document_out 		= marshal( document_updated, models["model_doc_out"] )

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True
		
			message = "dear user, there is the complete {} you requested ".format(document_type_full)


		# for other users
		else :

			response_code	= 401
			### unvalid credentials / empty response
			message = "dear user, you don't have the credentials to solidify this {} with this oid : {}".format(document_type_full, doc_id) 



	else : 
		### no document / empty response
		response_code	= 404
		message 		= "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 

	### return response
	return {
				"msg" 	: message ,
				"data"	: document_out,
				"query"	: query_resume,
			}, response_code