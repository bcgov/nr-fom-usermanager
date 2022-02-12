import os
import dotenv
import sys
import logging

LOGGER = logging.getLogger(__name__)

# populate the env vars from an .env file if it exists
envPath = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(envPath):
    LOGGER.debug("loading dot env...")
    dotenv.load_dotenv()

# env vars that should be populated for script to run
ENV_VARS = ['KC_HOST', 'KC_CLIENTID', 'KC_REALM', 'KC_SECRET',
            'FOREST_CLIENT_IN_GIT', 'KC_FOM_CLIENTID']
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

