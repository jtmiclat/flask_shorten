import logging
import sys
import warnings

from flask_shorten import create_app

logging.basicConfig(stream=sys.stdout)
# Ignore deprecation Warnings after app has been initialize
# to not pollute the logs when running
app = create_app()
warnings.filterwarnings("ignore", category=DeprecationWarning)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
