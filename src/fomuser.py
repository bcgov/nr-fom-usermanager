"""command line based tool that attempts to make it easy to add new users
to the fom application
"""

import keycloak_wrapper
import logging
import constants
import requests
import ForestClient

#
LOGGER = logging.getLogger()

class FomAddUser:

    def __init__(self):
        self.kc = FomKeycloak()
        self.fc = ForestClient.ForestClient()

    def addUser(self, fomClientId: int, userId):
        roleExists = self.kc.roleExists(fomClientId)
        if not roleExists:
            self.kc.createRole(fomClientId)


class FomKeycloak:

    def __init__(self):
        self.connect()
        self.fcUtil = ForestClient.ForestClientUtil()
        self.rolePrefix = 'fom_forest_client_'
        # self.fc = ForestClient.ForestClient()

    def connect(self):
        self.token = keycloak_wrapper.access_token_sa(
            constants.KC_HOST,
            constants.KC_REALM,
            constants.KC_CLIENTID,
            constants.KC_SECRET)
        #print(f'self.token {self.token}')
        self.access_token = self.token['access_token']

    def createRole(self, forestClientNumber: int):
        pass

    def userIDExists(self, userId):
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

        users = keycloak_wrapper.realm_users(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token)

        # if userid.lower() in [ role['name'] for user in users]:

        LOGGER.debug(f"users: {users}")
        return users


    def roleExists(self, forestClientNumber: int):
        """ Checks to see if the forest client exists in keycloak

        :param forestClientNumber: [description]
        :type forestClientNumber: int
        """
        fcPadded = self.fcUtil.getPaddedForestClientID(forestClientNumber)
        roleName = f'{self.rolePrefix}{fcPadded}'
        LOGGER.debug(f"self.access_token: {self.access_token}")
        roles = keycloak_wrapper.client_roles(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token,
            'fom')
        roleExists = False
        if roleName in [ role['name'] for role in roles]:
            roleExists = True
        return roleExists





if __name__ == '__main__':
    FomKeycloak()
