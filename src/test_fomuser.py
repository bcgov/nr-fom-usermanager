import pytest
import ForestClient
import logging
import fomuser

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")



class TestClass:

    def test_getFOMRoles(self, fomKeyCloak_fixture):
        fomKeyCloak_fixture.roleExists('234234')
        #assert len(forestClient_fixture.forestClientData) >= 22408

@pytest.fixture
def fomKeyCloak_fixture():
    return  fomuser.FomKeycloak()

