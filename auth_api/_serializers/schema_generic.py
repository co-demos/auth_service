# -*- encoding: utf-8 -*-

"""
schema_generic.py  
- provides the model for GENERIC DATA definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal


log.debug("... loading schema_generic.py ...")

from auth_api._choices import *


### totaly raw field
class RawData(fields.Raw):
	def format(self, value):
		return value


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### generic info for updates
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
generic_data 		= fields.String(
										description	= "data about a document",
										attribute		= "data",
										example			= "new data",
										default			= 'a new data',
										required		= True,
									)
url_link				= fields.String(
										description	= "generic url_link",
										attribute		= "url_link",
										example			= "my-url-link",
										default			= '',
										required		= False,
									)
antispam				= fields.String(
										description	= "antispam field",
										attribute		= "antispam",
										example			= "antispam-string-to-check",
										default			= '',
										required		= True,
									)
antispam_field 	= {
	"antispam"	: antispam,
}

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### for document updates
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
field_raw 			= fields.Raw(
										description	= "raw data about a document",
										attribute		= "field_raw",
										example			= "raw data",
										default			= 'a new raw data',
										required		= True,
									)
field_value 		= fields.Raw(
										description	= "data about a document",
										attribute		= "data",
										example			= "new data",
										default			= 'a new data',
										required		= True,
									)
field_to_update		= fields.String(
										description	= "data about a document",
										attribute		= "field_to_update",
										example			= "infos.title",
										default			= 'a new data',
										required		= True,
									)
add_to_list			= fields.String(
										description	= "data about a document",
										attribute		= "add_to_list",
										example			= False,
										enum				= update_types_list,
										default			= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### basic informations about a document : project / licence / oid ...
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
title				= fields.String(
										description	= "title of the document",
										attribute		= "title",
										example			= "my-title",
										default			= 'title',
										required		= True,
									)
descript 			= fields.String(
										description	= "description of the document",
										attribute		= "description",
										example			= "my-description",
										default			= 'description',
										required		= False,
									)
licence 			= fields.String(
										description	= "licence of the document",
										attribute		= "licence",
										example			= "MIT",
										default			= 'MIT',
										enum			= licences_options,
										required		= True,
									)
open_level 			= fields.String(
										description	= "open level of the document",
										attribute		= "open_level",
										example			= "commons",
										default			= 'open_data',
										enum			= open_level_choices,
										required		= False,
									)
open_level_edit 	= fields.String(
										description	= "open level of the document for edit",
										attribute		= "open_level_edit",
										example			= "collective",
										default			= 'collective',
										enum			= open_level_choices,
										required		= True,
									)
open_level_show 	= fields.String(
										description	= "open level of the document for show",
										attribute		= "open_level_show",
										example			= "commons",
										default			= 'open_data',
										enum			= open_level_choices,
										required		= True,
									)
is_standard			= fields.Boolean(
										description	= "is it standard document ?",
										attribute		= "is_standard",
										example			= True,
										required		= False,
										default			= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### multilanguage
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
locale 				= fields.String(
										description	= "locale language code",
										attribute		= "locale",
										example			= "fr",
										default			= 'en',
										required		= False,
									)
field_to_translate 	= fields.String(
										description	= "code of the field to translatee",
										attribute		= "field_to_translate",
										example			= "infos.title",
										default			= 'infos.title',
										required		= False,
									)
text_translated		= fields.String(
										description	= "text to translate",
										attribute		= "text_translated",
										example			= "my-translation",
										default			= '',
										required		= False,
									)


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### tags
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
tag 				= fields.String(
										description	= "tag about the document",
										attribute		= "tag",
										example			= "my-tag",
										# default			= '',
										required		= False,
									)
tags_list 			= fields.List(
										tag, 
										description	= "list of tags about the document",
										attribute		= "tags_list", 
										default			= [] 
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### object ids
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### custom field for objectId values
class IdField(fields.Raw):
	def format(self, value):
		return str(value)

oid_field				= IdField(
										description	= "data about a document",
										attribute		= "_id",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
									)
oid 						= IdField(
										description = "oid of a document",
										attribute		= "oid",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
doc_id 					= fields.String(
										description = "oid of a document as string",
										attribute		= "doc_id",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= True,
									)
oid_usr 				= IdField(
										description = "oid of an user",
										attribute		= "oid_usr",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
created_by 			= IdField(
										description = "oid of an user",
										attribute		= "created_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
used_by 			= IdField(
										description = "oid of a document",
										attribute		= "used_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
modified_by 		= IdField(
										description = "oid of an user",
										attribute		= "modified_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
added_by 			= IdField(
										description = "oid of an user",
										attribute		= "added_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)

used_as 			= fields.String(
										description = "category of use",
										attribute		= "used_as",
										enumerate   	= doc_type_list,
										example			= "prj",
										required		= True,
									)

oid_fld 			= IdField(
										description = "oid of a field",
										attribute		= "oid_fld",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)

### store a correspondance dict of oids...
oid_dict = {
	"oid"		: { "field" : oid , 		"fullname" : "oid" } ,
	"usr" 	: { "field" : oid_usr , "fullname" : "user" } ,
}




### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### edit auth for a document
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
guests_can_see		= fields.Boolean(
										description	= "can guests see the document ?",
										attribute		= "guests_can_see",
										example			= True,
										required		= True,
										default			= True,
									)
guests_can_edit		= fields.Boolean(
										description	= "can guests edit the document ?",
										attribute		= "guests_can_edit",
										example			= False,
										required		= True,
										default			= False,
									)
edit_auth			= fields.String(
										description = "edit auth of an user",
										enum			= user_edit_auth,
										example			= "owner",
										required		= False,
										attribute		= "edit_auth", 
										default			= "editor" 
									)

public_auth 		= {
	"open_level_edit"	: open_level_edit,
	"open_level_show" 	: open_level_show,
}


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### log basics
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
is_running			= fields.Boolean(
										description	= "is the project currently running ?",
										attribute		= "is_running",
										example			= False,
										required		= True,
										default			= False,
									)

is_loaded			= fields.Boolean(
										description	= "is the project currently loaded ?",
										attribute		= "is_loaded",
										example			= False,
										required		= False,
										default			= False,
									)

is_linked_to_src	= fields.Boolean(
										description	= "is the project currently linked to the source ?",
										attribute		= "is_linked_to_src",
										example			= False,
										required		= False,
										default			= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### specs basics
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
doc_type 			= fields.String(
										description	= "category of a document",
										attribute		= "doc_type",
										enum				= doc_type_list,
										example			= "usr",
										# default		= 'usr',
										required		= True,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### preformat some generic fields
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
doc_oid 						= {
	"_id" 		: oid_field,
}

doc_basics		 				= {
	"title" 			: title,
	"description"	: descript,
}

doc_basics_licence				= {
	"title" 			: title,
	"licence"			: licence,
	"description"	: descript,
}

open_level_edit_show 		= {
	"open_level_edit"	: open_level_edit,
	"open_level_show" : open_level_show,
}
open_level_edit_ 			= {
	"open_level_edit"	: open_level_edit,
}



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### preformat some generic fields
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
update_field		= {
	"edit_auth"			: edit_auth,
	"doc_type"			: doc_type,
	"add_to_list"		: add_to_list,
	
	"field_to_update"	: field_to_update,
	"field_value" 		: field_value,
}

