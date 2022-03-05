import logging

import keycloak_wrapper
# TODO: not happy with the way this wrapper is implemented... Should provide
#       errors when api call fails, among other things.  Connecting to api
#       end points in KC is actually pretty easy.  Move to wrapping my self.
import requests

try:
    from . import constants
    from . import ForestClient
except ImportError:
    import constants
    import ForestClient

LOGGER = logging.getLogger(__name__)


class FomKeycloak:

    def __init__(self):
        #self.connect()
        self.getAccessToken()
        self.fcUtil = ForestClient.ForestClientUtil()

    # def connect(self):
    #     self.token = keycloak_wrapper.access_token_sa(
    #         constants.KC_HOST,
    #         constants.KC_REALM,
    #         constants.KC_CLIENTID,
    #         constants.KC_SECRET)
    #     self.access_token = self.token['access_token']
    #     LOGGER.debug("success getting access token")

    def getAccessToken(self):
        uri = f"{constants.KC_HOST}/auth/realms/{constants.KC_REALM}/protocol/openid-connect/token"
        header = {'Accept': 'application/json'}
        params = {
                "client_id": constants.KC_CLIENTID,
                "client_secret": constants.KC_SECRET,
                "grant_type":"client_credentials"}
        LOGGER.debug(f'uri: {uri}')
        r = requests.post(uri, data=params, headers=header)
        r.raise_for_status()
        access_key = r.json()
        self.access_token = access_key['access_token']
        LOGGER.debug(f'response as json string {self.access_token}')

    def getMatchingUsers(self, userId):
        """ Keycloak contains a lot of information about users.  This method
        determines if a userid exists in keycloak.  The method will do its own
        search of all the users in keycloak.  (not efficient)

        Looks for either <userid>@<identity provider>, or looks for any user id
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
        # Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users" # noqa
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
            # search for username
            #if user['username'].lower().startswith(userId.lower()):
            if userId.lower() in user['username'].lower():
                email = ''
                if 'email' in user:
                    email = user['email']
                matchedUsers.append([user['username'], email])
            # search matching email
            #elif ('email' in user) and user['email'].lower().startswith(
            #        userId.lower()):
            elif ('email' in user) and userId.lower() in user['email'].lower():

                matchedUsers.append([user['username'], user['email']])
            elif (('attributes' in user) and
                  'idir_username' in user['attributes']) and \
                    userId.lower() in user['attributes']['idir_username'][0].lower():

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

    def getRoles(self, clientID):
        """returns a list of roles that exist within the provided client id"""
        roles = keycloak_wrapper.client_roles(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token,
            clientID)
        return roles

    def getFOMRoles(self, forestClientNumber: int):
        """_summary_

        :param forestClientNumber: _description_
        :type forestClientNumber: int
        :param clientID: _description_, defaults to 'fom'
        :type clientID: str, optional
        :return: _description_
        :rtype: _type_
        """
        roles = self.getRoles(constants.FOM_CLIENT_ID)
        roleName = self.fcUtil.getRoleName(forestClientNumber)

        filteredRoles = [role for role in roles if roleName == role['name']]
        return filteredRoles

    def roleExists(self, forestClientNumber: int):
        """ Checks to see if the forest client exists in keycloak

        :param forestClientNumber: [description]
        :type forestClientNumber: int
        """
        roleName = self.fcUtil.getRoleName(forestClientNumber)

        roles = self.getFOMRoles(forestClientNumber)
        roleExists = False
        if roleName in [role['name'] for role in roles]:
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

        * send payload/body where {"name":"role name to create"}
        * end point /auth/admin/realms/$REALM/clients/$CLIENTID/roles
        * method POST
        """
        # self.fcUtil.
        if not self.roleExists(forestClientId):
            roleName = self.fcUtil.getRoleName(forestClientId)
            LOGGER.debug(f'rolename: {roleName}')

            clientid = self.getFomClientId()
            Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients/{clientid}/roles"  # noqa
            data = {"name": roleName,
                    "description":  description}
            headers = {
                "Authorization": "Bearer " + self.access_token,
                'Content-type': 'application/json',
                'Accept': 'application/json'}
            response = requests.post(url=Url,
                                     headers=headers,
                                     json=data)
            response.raise_for_status()

    def removeRole(self, clientID, roleName):
        """_summary_

        :param clientID: _description_
        :type clientID: _type_
        :param roleName: _description_
        :type roleName: _type_

        https://$KC_URL/auth/admin/realms/$REALM/clients/{id}/roles/{role-name}

        """
        LOGGER.debug(f'clientID: {clientID}')
        LOGGER.debug(f'roleName: {roleName}')
        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients/{clientID}/roles/{roleName}"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}
        LOGGER.debug(f"deleting the role: {roleName}")
        response = requests.delete(url=Url,
                                   headers=headers
                                   )
        response.raise_for_status()
        LOGGER.debug(f"response: {response.status_code}")

    def getClients(self):
        '''
        GET /{realm}/clients
        '''
        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}
        response = requests.get(url=Url,
                                headers=headers
                                )
        response.raise_for_status()
        LOGGER.debug(f"response: {response.status_code}")

        data = response.json()
        return data

    def getClient(self, clientID):
        """gets a list of all the clients in the realm and returns only the
        client that matches the clientID provided
        """
        clients = self.getClients()
        client = None
        for client in clients:
            if client['clientId'].lower() == clientID.lower():
                break
        return client

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

        roles = self.getFOMRoles(forestClientId)
        LOGGER.debug(f"roles length {len(roles)}")
        LOGGER.debug(f"role length {roles}")

        clientid = self.getFomClientId()

        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users/{matchUsers[0]['id']}/role-mappings/clients/{clientid}"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}

        response = requests.post(url=Url,
                                 headers=headers,
                                 json=roles)
        response.raise_for_status()
