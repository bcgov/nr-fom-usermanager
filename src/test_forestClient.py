import pytest
import ForestClient
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")



class TestClass:

    def test_forestClientFromGitParse(self, forestClient_fixture):
        forestClient_fixture.parse()
        assert len(forestClient_fixture.forestClientData) >= 22408

    def test_getMatchingClient(self, forestClientParsed_fixture):
        values = forestClientParsed_fixture.getMatchingClient('arm')
        LOGGER.debug(f"values: {values}")

    def test_getPaddedForestClientID(self, forestClient_fixture):
        sampleData = [['33', '00000033'], ['2234', '00002234']]
        for data in sampleData:
            padded = forestClient_fixture.getPaddedForestClientID(data[0])
            assert padded == data[1]

    def test_forestClientIdExists(self, forestClientParsed_fixture):
        fc = forestClientParsed_fixture
        clientsThatExist = ['188736', '187347', '186040', '181461', '177380',
                            '62911', '23530', '2884', '1011']
        clientsThatDontExist = ['88348', '88978', '90125']
        for clExist in clientsThatExist:
            LOGGER.debug(f"fcExists: {clExist}")

            assert fc.forestClientIdExists(clExist) is True

        for clExist in clientsThatDontExist:
            fcExists = fc.forestClientIdExists(clExist)
            LOGGER.debug(f"fcExists: {clExist}  :  {fcExists}")
            assert fcExists is False


@pytest.fixture
def forestClient_fixture():
    return  ForestClient.ForestClientFromGit()

@pytest.fixture
def forestClientParsed_fixture(forestClient_fixture):
    forestClient_fixture.parse()
    return forestClient_fixture

