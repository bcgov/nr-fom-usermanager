import pytest
import ForestClient
import logging
import fomuser

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")


class TestClass:

    def test_getFOMRoles(self, fomKeyCloak_fixture):
        clientRoleExists = fomKeyCloak_fixture.roleExists('234234')
        assert not clientRoleExists

        clientRoleExists = fomKeyCloak_fixture.roleExists('1011')
        assert clientRoleExists

    def test_userIDExists(self, fomKeyCloak_fixture):
        userData = fomKeyCloak_fixture.userIDExists('kjnether@idir')
        LOGGER.debug(f"userData: {userData}")


@pytest.fixture
def fomKeyCloak_fixture():
    return  fomuser.FomKeycloak()
