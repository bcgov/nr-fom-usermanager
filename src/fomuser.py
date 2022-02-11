"""command line based tool that attempts to make it easy to add new users
to the fom application
"""

import keycloak_wrapper
import logging
import constants
import requests
import ForestClient
import argparse
import pprint

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

        users = keycloak_wrapper.realm_users(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token)

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

class CLI:

    def __init__(self):
        self.defineParser()

    def defineParser(self):
        parser = argparse.ArgumentParser(description='Add / Query Fom user data.')
        parser.add_argument('-qfc', '--query-forest-client', type=str,                             help='Define the starting characters for forest clients you want to view / retrieve forest client ids for')
        parser.add_argument('-qu', '--query-users',
                             help='Query for keycloak users that match the string')
        # parser.add_argument('--add-user', nargs=2,
        #                     help='sum the integers (default: find the max)')

        #parser.print_help()
        print(f'parser: {parser}')

        args = parser.parse_args()
        print(f'args: {args}')

        if args.query_forest_client:
            # do search
            print(f'search chars: {args.query_forest_client}')
            self.queryForestClient(args.query_forest_client)

        elif args.query_users:
            print(f'search chars: {args.query_users}')
            self.queryUsers(args.query_users)

    def queryForestClient(self, queryString):
        fc = ForestClient.ForestClient()
        matches = fc.getMatchingClient(queryString)
        print(f"forest clients matching: {queryString}")
        print("-"*80)
        formattedList = [f"{match[0]:50} - {int(match[1]):8d}" for match in matches]
        print('\n'.join(formattedList))

    def queryUsers(self, queryString):
        kc = FomKeycloak()
        users = kc.getMatchingUsers(queryString)
        formattedList = [f"{match[0]:30} - {match[1]:20}" for match in users]
        print(f"matching users for search: {queryString}")
        print("-"*80)
        print('\n'.join(formattedList))




if __name__ == '__main__':
    # FomKeycloak()
    cli = CLI()
