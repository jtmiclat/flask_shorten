import logging
import sys
import warnings

from flask_shorten import create_app

# Ignore deprecation Warnings after app has been initialize
# to not pollute the logs when running
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.basicConfig(stream=sys.stdout)
app = create_app()
