import logging
import sys
import warnings

from flask_shorten import create_app

# Ignore deprecation Warnings after app has been initialize
# to not pollute the logs when running
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.basicConfig(stream=sys.stdout)
app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
