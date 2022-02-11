""" interface to provision of forest client data.  For now its going to
parse / the data in the fom github repo...

Eventually will interface with the forest client api to get this information
"""

import constants
import requests
import re
import logging

LOGGER = logging.getLogger(__name__)

class ForestClient:

    def __init__(self):
        self.fc_git = ForestClientFromGit()

    def getMatchingClient(self, searchCharacters):
        return self.fc_git.getMatchingClient(searchCharacters)

    def forestClientIdExists(self, clientId):
        return self.fc_git.forestClientIdExists(clientId)




class ForestClientFromGit:

    def __init__(self):
        self.fcTable = constants.FOREST_CLIENT_IN_GIT
        self.forestClientData = None
        #self.parse()

    def parse(self):
        # pulling the data down from the git repo
        forestClientDict = {}
        response = requests.get(constants.FOREST_CLIENT_IN_GIT)
        response.raise_for_status()
        jsFCFile = response.text
        # the insert line marks the start of the data.  This regex detects
        # the insert line
        insertLine_regex = re.compile('^\s+INSERT\s+INTO\s+app_fom\.forest_client.*$')
        # sample line that shows the pattern that the next line does.
        #  ('189974', 'LUXOR-SPUR DEVELOPMENTS LTD.', CURRENT_USER),
        dataLine_regex = re.compile("^\s+\('[0-9]{4,8}'\,\s+'.+'\,\s+CURRENT_USER\)\,\s*$")

        LOGGER.debug(f"jsFCFile {type(jsFCFile)}")
        for line in jsFCFile.split('\n'):
            if dataLine_regex.match(line):
                line = line.replace( ', CURRENT_USER),', '')
                line = line.replace('(', '').replace(')', '').strip()
                line = line.replace(', ', ',').replace("'", '')
                lineList = line.split(',')
                forestClientId = self.getPaddedForestClientID(lineList[0])
                forestClientDict[lineList[1]] = forestClientId
        self.forestClientData = forestClientDict
        LOGGER.debug(f"number forest clients = {len(self.forestClientData)}")

    def getMatchingClient(self, characters):
        values = []
        for fc in self.forestClientData:
            if fc.lower().startswith(characters.lower()):
                values.append(fc)
        return values

    def forestClientIdExists(self, clientId):
        # remove any padding characters
        clientIdPadded = self.getPaddedForestClientID(clientId)
        clientExists = False
        if clientIdPadded in self.forestClientData.values():
            clientExists = True
        return clientExists

    def getPaddedForestClientID(self, clientId):
        """Forest clients are an 8 digit field that is stored as a string.
        This method will pad the forestclient id with leading 0's to meet
        the expected 8 character length

        :param clientId: input forest client
        :type clientId: str, int
        """
        clientId_str = str(clientId)
        numChars = len(clientId_str)
        #LOGGER.debug(f"clientId_str length: {numChars}")

        if numChars < 8:
            padding = 8 - numChars
            clientId_str = ('0' * padding) + clientId_str
            #LOGGER.debug(f"clientId_str: {clientId_str}")
        return clientId_str




if __name__ == '__main__':
    fc = ForestClientFromGit()
    fc.parse()