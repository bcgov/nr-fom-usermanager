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

# Setup



# Running Script

## Search forest clients

Before a new user can be added we need to know what forest client id to attach
them to.  This is accomplished with a forest client search.

`python fomuser.py -qfc <search string>`

Example:

```
kirk@NCC1701:$ python fomuser.py -qfc kli
forest clients matching: kli
--------------------------------------------------------------------------------
KLINGON CONTRACTING LTD.                           -    18514
KLINGON SAND & GRAVEL LTD.                         -    31775
KLINGON & BORG CONSULTING                          -    53996
KLI FOREST PRODUCTS INC.                           -    68697
KLI ENG. & LAND SURVEYING INC                      -    97448
KLI INVESTMENTS LTD.                               -   103766
KLIMA RESOURCES LTD.                               -   110974
KLISTERS PELLET INC                                -   126239
KLIK & CLOCK CONSULTING LTD.                       -   126967

```

## Search Keycloak users
Having determined what the forest client id is, use the following command to
search for the users in keycloak:

`fomuser.py -qu <search string>`

Example:

```
kirk@NCC1701:$ python fomuser.py -qu sp
matching users for search: kj
--------------------------------------------------------------------------------
spock@enterprisedir                    - spock.mock@gov.bc.ca
speed.warp@Prometheusdir               - speedwarp@gmail.com
sp.warf@bce-klingon-id                 - warf@birdofprey.ca
```

## Adding the user - <not complete>

Having determined the user id, and the forest client the new user can now be
added:

`fomuser --add <userid> <forest client id>`


Projected syntax:
```
fom-user <forest client id> <user email>
```

# Building the package manually

```
pip install -r requirements-build.txt
python -m build --sdist
```

# Related links / Information

https://github.com/bcgov/ocp-sso/issues/118
