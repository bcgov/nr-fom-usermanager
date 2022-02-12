import constants
import ForestClient
import keycloak_wrapper
import logging
import requests
import json

LOGGER = logging.getLogger(__name__)

class FomKeycloak:

    def __init__(self):
        self.connect()
        self.fcUtil = ForestClient.ForestClientUtil()

    def connect(self):
        self.token = keycloak_wrapper.access_token_sa(
            constants.KC_HOST,
            constants.KC_REALM,
            constants.KC_CLIENTID,
            constants.KC_SECRET)
        #print(f'self.token {self.token}')
        self.access_token = self.token['access_token']

    def getMatchingUsers(self, userId):
        """ Keycloak contains a lot of information about users.  This method
        determines if a userid exists in keycloak.  The method will do its own
        search of all the users in keycloak.  (not efficient)

        Looks for either <userid>@<identitiy provider>, or looks for any user id
        that matches the identity provider.

        If more than one user is found then a warning message will be logged.

            user@dir
            user@bceid
            <email address>

        Will get a list of the users in the realm and search for

        :param userId: [description]
        :type userId: [type]
        :return: [description]
        :rtype: [type]
        """
        # /{realm}/users
        # params = {"realm-name": constants.KC_REALM}
        # headers = {"Authorization": "Bearer " + self.access_token}
        # Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users"
        # LOGGER.debug(f"URL: {Url}")
        # response = requests.get(url=Url,
        #                         headers=headers)

        # LOGGER.debug(f"response: {response}")
        # LOGGER.debug(f"status: {response.status_code}")
        # LOGGER.debug(f"status: {response.json()}")

        users = self.getAllUsers()

        # if userid.lower() in [ role['name'] for user in users]:

        # search in username email attributes.idir_username
        # return username / email
        matchedUsers = []
        for user in users:

            if user['username'].lower().startswith(userId.lower()):
                matchedUsers.append([user['username'], user['email']])
            elif  ('email' in user ) and   user['email'].lower().startswith(userId.lower()):
                matchedUsers.append([user['username'], user['email']])
            elif (( 'attributes' in user ) and 'idir_username' in user['attributes']) and \
                    user['attributes']['idir_username'][0].lower().startswith(userId.lower()):
                matchedUsers.append([user['username'], user['email']])

        LOGGER.debug(f"users: {users}")
        return matchedUsers

    def getAllUsers(self):
        users = keycloak_wrapper.realm_users(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token)
        return users

    def isValidUser(self, userid):
        """validates that the user provided exists in keycloak, and that the
        id is unique

        :param userid: input user id to be validated
        :type userid: str
        """
        isValid = False
        users = self.getAllUsers()
        LOGGER.debug(f"users: {users}")
        matches = []
        for user in users:
            if user['username'] == userid:
                matches.append(user)
        if len(matches) == 1:
            isValid = True
        return isValid

    def getRoles(self, forestClientNumber: int):
        roleName = self.fcUtil.getRoleName(forestClientNumber)

        LOGGER.debug(f"self.access_token: {self.access_token}")
        roles = keycloak_wrapper.client_roles(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token,
            'fom')
        LOGGER.debug(f"{roles}")
        roles = [ role for role in roles  if roleName == role['name'] ]
        return roles

    def roleExists(self, forestClientNumber: int):
        """ Checks to see if the forest client exists in keycloak

        :param forestClientNumber: [description]
        :type forestClientNumber: int
        """
        roleName = self.fcUtil.getRoleName(forestClientNumber)

        roles = self.getRoles(forestClientNumber)
        roleExists = False
        if roleName in [  role['name'] for role in roles]:
            roleExists = True
        return roleExists

    def getFomClientId(self):
        """Looks up the FOM client 'id' using the 'clientid'

        the client 'id' is usually what is required to create / modify objects
        in / for / on behalf of the client
        """
        clients = keycloak_wrapper.realm_clients(
            f"{constants.KC_HOST}/auth/", constants.KC_REALM,
             self.access_token)
        fomClient = None
        for client in clients:
            if client['clientId'] == constants.KC_FOM_CLIENTID:
                fomClient = client['id']
        return fomClient

    def createRole(self, forestClientId, description):
        """Creates the role for the forest client id if it doesn't already
        exist.

        * send payload/body where {"name":"rolenametocreate"}
        * end point /auth/admin/realms/$REALM/clients/$CLIENTID/roles
        * method POST
        """
        #self.fcUtil.
        if not self.roleExists(forestClientId):
            roleName = self.fcUtil.getRoleName(forestClientId)
            LOGGER.debug(f'rolename: {roleName}')

            clientid = self.getFomClientId()
            Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients/{clientid}/roles"
            data = { "name" : roleName,
                     "description":  description}
            headers = {
                "Authorization": "Bearer " + self.access_token,
                'Content-type':'application/json',
                'Accept':'application/json'}
            response = requests.post(url=Url,
                                     headers=headers,
                                     json=data)
            LOGGER.debug(f"response: {response.status_code}")

    def addRoleToUser(self, userid, forestClientId):
        """This is the role mapping exercise...


        /auth/admin/realms/$REALM/users/$USERID/role-mappings/clients/$CLIENTID
        USERID - comes from user['id']

        assumes that the forestclientid and the userid have been
        validated then does the role mapping

        https://$KC_URL/auth/admin/realms/$REALM/users/$userid/role-mappings/clients/$fom_client_id

        1. get user id
        1. get client id
        1. get role
        """
        users = self.getAllUsers()
        matchUsers = []
        for user in users:
            if user['username'] == userid:
                matchUsers.append(user)

        # TODO: make sure only one user
        LOGGER.debug(f"users length {len(matchUsers)}")


        roles = self.getRoles(forestClientId)
        LOGGER.debug(f"roles length {len(roles)}")
        LOGGER.debug(f"role length {roles}")

        clientid = self.getFomClientId()

        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users/{matchUsers[0]['id']}/role-mappings/clients/{clientid}"
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type':'application/json',
            'Accept':'application/json'}

        response = requests.post(url=Url,
                                    headers=headers,
                                    json=roles)




