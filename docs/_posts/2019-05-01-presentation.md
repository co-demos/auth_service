---
title : PRESENTATION
categories:
  - general
tags:
  - documentation
  - configuration
  - deployment
  - ecosystem
toc: true
toc_label: "contents"
toc_sticky: true
---

-----

{% include figure image_path="/static/logos/logo_auth_microservice.png" alt="toktok logo" %}

## TOKTOK

**TokTok** is a microservice (a REST API) for users management and authentication based on access and refresh JSON Web Tokens (JWT)

- this auth server was extracted / insulated / forked / adapted from **[solidata_backend](https://github.com/entrepreneur-interet-general/solidata_backend)** project.
- compatible with the **TADATA!** sofware suite ( [ApiViz](https://github.com/co-demos/apiviz-frontend) / [Solidata_frontend](https://github.com/entrepreneur-interet-general/solidata_frontend) / [OpenScraper](https://github.com/entrepreneur-interet-general/OpenScraper) )

-------

## GOALS

- a simple server to manage users and authorizations based on JWT exchanges between client and server
- possibility to switch on/off some extra features as : RSA decryption/encryption, anonymous JWT, sending confirmation email

---------

## FEATURES 

Toktok includes "out-the-box" some classic features related to user authentication

### JWT (JSON Web Tokens) :

- access and refresh token for security over all the app
- RSA encryption (optionnal)
- RSA encryption : server can send to the client a RSA public key for encryption client-side
- RSA decryption : server can decode forms (login/register) encoded client-side with the RSA public key

### Users management :

- login / register user 
- anonymous login (optionnal) : sends a JWT for an anonymous use. Can be expected by server for routes with `@anonymous_required` decorator like `/login` or `/register`
- confirm email (optionnal in dev mode): confirm user by sending a confirmation link (protected) in an email 
- password forgotten by sending a link (protected) in an email with redirection to new password form 
- reset password from client interface (protected) ...

### Documentation 
	- on all API endpoints with Swagger (and some patience from the developer)

### Features TO DO  :
- user : 
	- edit user (working on)
	- edit email (protect email update)

------

## INSPIRATIONS / BENCHMARK

- not finding a simple enough open source solution resolving the following problem : having a third party service (on a distant server) able to serve reasonnably secure tokens and manage users, so to avoid to build/re-invent a custom authentication for login/register every time we work on an app... 
- more, be able to share user/credentials between multiple services 
- we looked at [Oauth2.0](https://oauth.net/2/) (but doesn't manage users per say), meteor-password (but dialog with websocket)...