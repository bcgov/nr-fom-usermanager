# Overview

The [Forest Operations Map](https://github.com/bcgov/nr-fom-api) application
supports the ability for licensees to authenticate / login to the application.
Authentication is handled using OIDC.  The application in its current site
requires that someone in government be able to manage access.

Adding new users / roles to the application through the keycloak UI would be
inefficient as it would require  looking up:
* forest client number
* determining if it exists as a role in keycloak
* create if roles does not exist
* add user to the role

This repository contains the code for a simple command line based tool. That
will make it easy to add new users to the FOM application.

Projected syntax:
```
fom-user <forest client id> <user email>
```
