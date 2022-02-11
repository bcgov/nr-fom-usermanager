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

class FomKeycloak:

    def __init__(self):
        self.connect()
        self.fc = ForestClient.ForestClient()

    def connect(self):
        self.token = keycloak_wrapper.access_token_sa(
            constants.KC_HOST,
            constants.KC_REALM,
            constants.KC_CLIENTID,
            constants.KC_SECRET)
        print(f'self.token {self.token}')
        self.access_token = self.token['access_token']

    def roleExists(self, forestClientNumber: int):
        """ Checks to see if the forest client exists in keycloak

        :param forestClientNumber: [description]
        :type forestClientNumber: int
        """
        roles = keycloak_wrapper.client_roles(constants.KC_HOST,
            constants.KC_REALM,
            self.access_token,
            constants.KC_CLIENTID)
        LOGGER.debug('roles: {roles}')











if __name__ == '__main__':
    FomKeycloak()
