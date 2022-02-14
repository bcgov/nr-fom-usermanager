#!/usr/bin/python

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
import FOMKeyCloak

LOGGER = logging.getLogger()

# class FomAddUser:

#     def __init__(self):
#         self.kc = FomKeycloak()
#         self.fc = ForestClient.ForestClient()

#     def addUser(self, fomClientId: int, userId):
#         roleExists = self.kc.roleExists(fomClientId)
#         if not roleExists:
#             self.kc.createRole(fomClientId)



class CLI:

    def __init__(self):
        self.defineParser()
        self.fc = ForestClient.ForestClient()


    def defineParser(self):
        parser = argparse.ArgumentParser(description='Add / Query Fom user data.')
        parser.add_argument('-qfc', '--query-forest-client', type=str,                             help='Define the starting characters for forest clients you want to view / retrieve forest client ids for')
        parser.add_argument('-qu', '--query-users',
                             help='Query for keycloak users that match the string')
        parser.add_argument('-a' '--add-user', nargs=2,
                             help='Add User ')

        # TODO: Add a subparser here to better describe the two args for add-user


        args = parser.parse_args()

        if not args.query_forest_client and \
            not args.query_users and \
                not args.query_users:
                    parser.print_help()

        LOGGER.debug(f'parser: {parser}')

        LOGGER.debug(f'args: {args}')

        if args.query_forest_client:
            # do search
            LOGGER.debug(f'search chars: {args.query_forest_client}')
            self.queryForestClient(args.query_forest_client)

        elif args.query_users:
            LOGGER.debug(f'search chars: {args.query_users}')
            self.queryUsers(args.query_users)

    def queryForestClient(self, queryString):
        fc = ForestClient.ForestClient()
        matches = fc.getMatchingClient(queryString)
        print(f"forest clients matching: {queryString}")
        print("-"*80)
        formattedList = [f"{match[0]:50} - {int(match[1]):8d}" for match in matches]
        print('\n'.join(formattedList))

    def queryUsers(self, queryString):
        kc = FOMKeyCloak.FomKeycloak()
        users = kc.getMatchingUsers(queryString)
        formattedList = [f"{match[0]:30} - {match[1]:20}" for match in users]
        print(f"matching users for search: {queryString}")
        print("-"*80)
        print('\n'.join(formattedList))

    def addUser(self, userid, forestclient):
        """receives a key cloak user id, verifies that it exists and that it
        is unique.

        Does a search to make sure the forest client id exists.

        If both of the above criteria are met, checks to see if a role associated
        with the user already exists.  If not one is created.  Then adds the
        user to the role.

        :param userid: name of input user
        :type userid: str
        :param forestclient: name of forest client
        :type forestclient: str, int
        """
        # validation: verify forest client
        fc = ForestClient.ForestClient()
        if not fc.forestClientIdExists(forestclient):
            msg = f"The forest client: {forestclient} does not exist"
            raise ValueError(msg)

        # validation: verify the user
        kc = FOMKeyCloak.FomKeycloak()
        if not kc.isValidUser(userid):
            msg = f'The key cloak user: {userid} is invalid'
            raise ValueError(msg)

        # adding the user
        if not kc.roleExists(forestclient):
            description = self.fc.getForestClientDescription(forestclient)
            # creating the role if it doesn't exist
            kc.createRole(forestclient, description)
        # mapping role to user
        kc.addRoleToUser(userid, forestclient)








if __name__ == '__main__':
    # FomKeycloak()
    cli = CLI()
