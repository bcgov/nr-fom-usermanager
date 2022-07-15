#!/bin/bash
set -eu


# Protecter var - can be accepted as a param or environment variable
if [ ! -z "${1:-}" ]; then
    export KC_SECRET=${1}
elif [ ! -z "${KC_SECRET:-}" ]; then
    export KC_SECRET=${KC_SECRET}
else
    echo -e "\nPlease provide KC_SECRET as a param or environment variable"
    echo -e "  ./script <key>"
    echo -e "  KC_SECRET=<key> ./script\n"
    exit
fi


# Vars
export KC_HOST=https://oidc.gov.bc.ca
export KC_CLIENTID=fom-admin
export KC_REALM=ichqx89w
export KC_FOM_CLIENTID=fom
export KC_ENV=prod


# Env
if [ ! -d venvfom ]
then
    python -m venv venvfom
    . ./venvfom/bin/activate
    which pip || python -m pip install --upgrade pip
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
