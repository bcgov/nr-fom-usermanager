
misc code in trying to understand how to duplicate the keycloak oid
authorization flow

curl -v \
  -d "client_id=$KC_CLIENTID" \
  -d "username=$KC_USERNAME" \
  -d "password=$KC_PASSWORD" \
  -d "grant_type=password" \
  "$KC_HOST/realms/master/protocol/openid-connect/token"

# get the config
curl \
"$KC_HOST/auth/realms/$KC_REALM/.well-known/openid-configuration"
http://keycloakhost:keycloakport/auth/realms/{realm}/.well-known/openid-configuration
https://oidc.gov.bc.ca/auth/realms/ichqx89w/.well-known/openid-configuration

# WORKS! gets access token (JWT?)
# and decodes it to json
curl  \
  -H "Accept: application/json" \
  -d "client_id=$KC_CLIENTID" \
  -d "client_secret=$KC_SECRET" \
  -d "grant_type=client_credentials" \
  "$KC_HOST/auth/realms/$KC_REALM/protocol/openid-connect/token" | \
  jq ".access_token" | tr -d '"' | jq -R 'split(".") | .[0],.[1] | @base64d | fromjson'



curl \
  -H "Authorization: bearer $KC_ACCESS_TOKEN" \
  "$KC_HOST/auth/admin/realms/$KC_REALM"


# What did?
# ------------------------------------------------------------------------------

a) created service account - similar to other service accounts in the realms

b) Modified service account roles
    * had to go to "service account roles" some different roles

c) Tried a few different python keycloak api wrappers.  Ended up liking this one
   the most: https://pypi.org/project/keycloak-wrapper/

d) Figured out the auth process

e) Modified the install to allow the rest call to update the description for the
   role.  Long term should just extend the class in my own class, or submit a
   patch to original author.

# Useful Links
# ------------------------------------------------------------------------------

keycloak-wrapper : https://pypi.org/project/keycloak-wrapper/
                   https://github.com/kapsali29/keycloak_wrapper
                   https://github.com/bcgov/ocp-sso/tree/master/scripts

keycloak api: https://www.keycloak.org/docs-api/5.0/rest-api/index.html

Where roles were extracted from the app: https://raw.githubusercontent.com/bcgov/nr-fom-api/master/apps/api/src/migrations/main/1616015261635-forestClient.js


# Adding roles to keycloak service account

stolen from: https://stackoverflow.com/questions/66452108/keycloak-get-users-returns-403-forbidden

1. select client
1. make sure service account is enabled
1. go to service account roles
1. in client roles: select realm management
1. find the permission required
