# Objective

Simple command line tool that makes it easy to add new users to the FOM
application.  Planned syntax:

## list forest client ids that match

`fomuser --getfc <characters>`

Returns a list of forest clients that match the provided characters.  Match
is case insensitive

## list keycloak users

`fomuser --getusers_email <email>`

returns a list of keycloak users that match the query

## Add fom user

`fomuser --add <user KC id> <fom client #>`

example:
```
fomuser --add kjnether@idir 1011
```


# Plan

* Glue together forest client functionality into CLI to allow user to query for
  forest client ids.

* Glue together keycloak functionality to allow CLI to query for users in kc


# Undetermined

## best way to setup so shareable

* how will auth work.  At moment app pulls in service account from



