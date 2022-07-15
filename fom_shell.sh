#!/bin/bash
set -eu

# Vars
export KC_SECRET=$KC_SECRET
export KC_HOST=https://oidc.gov.bc.ca
export KC_CLIENTID=fom-admin
export KC_REALM=ichqx89w
export KC_FOM_CLIENTID=fom
export KC_ENV=prod

# Env
if [ ! -d venvfom ]
then
    python3 -m venv venvfom
    . ./venvfom/bin/activate
    python -m pip install --upgrade pip
    pip install FOMUserUtil
else
    source ./venvfom/bin/activate
fi

# Instructions
echo -e "\n"
echo -e "\nQuery for users and note their ID (left column).  A login attempt must have already been made."
echo -e "  E.g. fomuser -qu <name>"
echo -e "\nFind their forest client ID (right column)."
echo -e "  E.g. fomuser -qfc <company>"
echo -e "\nAdd a user to a forest client ID."
echo -e "  E.g. fomuser -a <UserID> <ClientID>"
echo -e "\n"

# Bash prompt with vars
PS1="fomuser on ${KC_ENV}> " /bin/bash
