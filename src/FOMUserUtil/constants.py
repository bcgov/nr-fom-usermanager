import os
import dotenv
import sys
import logging

LOGGER = logging.getLogger(__name__)

envFile = '.env-dev'

# populate the env vars from an .env file if it exists
envPath = os.path.join(os.path.dirname(__file__), '..', '..', envFile)
LOGGER.debug(f"envPath: {envPath}")
if os.path.exists(envPath):
    LOGGER.debug("loading dot env...")
    dotenv.load_dotenv(envPath)

# env vars that should be populated for script to run
ENV_VARS = ['KC_HOST', 'KC_CLIENTID', 'KC_REALM', 'KC_SECRET',
            'KC_FOM_CLIENTID', 'KC_SA_CLIENTID']

module = sys.modules[__name__]

envsNotSet = []
for env in ENV_VARS:
    if env not in os.environ:
        envsNotSet.append(env)
    else:
        # transfer env vars to module properties
        setattr(module, env, os.environ[env])

if envsNotSet:
    msg = 'The script expects the following environment variables to ' + \
          f'be set {envsNotSet}'
    raise EnvironmentError(msg)

# default values for the references to the forest clients in the fom repo
FOREST_CLIENT_IN_GIT = \
    'https://raw.githubusercontent.com/bcgov/nr-fom-api/master/apps/api/src/migrations/main/1616015261635-forestClient.js' + '||' + \
    'https://github.com/bcgov/nr-fom-api/blob/master/apps/api/src/migrations/main/1639180924469-forestClientTypesNonCNonI.js' # noqa

FOM_CLIENT_ID = 'fom'