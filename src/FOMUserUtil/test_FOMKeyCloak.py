import logging

import pytest

from . import FOMKeyCloak

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")


class Test_FOMKeyCloak:

    def test_getFOMRoles(self, fomKeyCloak_fixture):
        clientRoleExists = fomKeyCloak_fixture.roleExists('234234')
        assert not clientRoleExists

        clientRoleExists = fomKeyCloak_fixture.roleExists('1011')
        assert clientRoleExists

    def test_getRoles(self, fomKeyCloak_fixture):
        roles = fomKeyCloak_fixture.getRoles('99999999')
        # should error but doesn't
        LOGGER.debug(f"roles: {roles}")

    def test_userIDExists(self, fomKeyCloak_fixture):
        userData = fomKeyCloak_fixture.isValidUser('kjnether@idir')
        LOGGER.debug(f"userData: {userData}")
        assert userData is True

    def test_addRoleToUser(self, fomKeyCloak_fixture):
        fomKeyCloak_fixture.addRoleToUser('kjnether@idir', '99999999')

    def test_createRole(self, fomKeyCloak_fixture):
        testfcid = '99999999'
        description = "test dummy role"
        fomKeyCloak_fixture.createRole(testfcid, description)

    def test_getFomClientId(self, fomKeyCloak_fixture):
        client = fomKeyCloak_fixture.getFomClientId()
        LOGGER.debug(f"clientid: {client}")
        assert client is not None

    def test_isValidUser(self, fomKeyCloak_fixture):
        users = fomKeyCloak_fixture.getAllUsers()
        valid = fomKeyCloak_fixture.isValidUser(users[0]['username'])
        LOGGER.debug(f"isvalid: {valid}")


@pytest.fixture
def fomKeyCloak_fixture():
    return FOMKeyCloak.FomKeycloak()
