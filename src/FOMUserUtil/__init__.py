import os.path
name = os.path.basename(os.path.dirname(__file__))
# version = '0.0.9' moving version to VERSION file, easier to update
import importlib.metadata
__version__ = importlib.metadata.version('FOMUserUtil')
print(__version__)