"""command line based tool that attempts to make it easy to add new users
to the fom application
"""

import keycloak_wrapper
import logging
import constants
import requests
import ForestClient
import PyInquirer
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

class CLIArgparse:

    def __init__()

class CLIInquirer:
    """https://medium.com/geekculture/build-interactive-cli-tools-in-python-47303c50d75

    looks promising, but taking to long... circle back to easier way.
    Leaving code here for future
    """
    def __init__(self):
        self.getQuestionDefs()
        #self.defineStyles()

    def defineStyles(self):
        styleDict1 = {
            "separator": '#6C6C6C',
            "questionmark": '#FF9D00 bold',
            "selected": '#5F819D',
            "pointer": '#FF9D00 bold',
            "instruction": '',  # default
            "answer": '#5F819D bold',
            "question": '',        }
        self.style1 = PyInquirer.style_from_dict(styleDict1)

    def getQuestionDefs(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'queryType',
                'message': 'Query Type?',
                'choices': [
                    'forest client query',
                    'key cloak user query'
                ]
            },
            {
                'type': "input",
                "name": "forestClientSearch",
                "message": "Enter the characters to search forest clients"
            },
            {
                'type': 'list',
                'name': 'queryType',
                'message': 'Query Type?',
                'choices':

            },

            ]

    def cliInit(self):
        queryType = PyInquirer.prompt(self.questions)
        print(f"queryType: {queryType}")
        if queryType['queryType'] == 'forest client query':
            fcSearch = queryType.get('forestClientSearch')


            print(f'fcSearch: {fcSearch}')

        LOGGER.debug("answers")
        pprint(answers)




if __name__ == '__main__':
    # FomKeycloak()
    cli = CLI()
    cli.cliInit()
