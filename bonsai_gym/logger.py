import logging
import os

logFormatter = "[%(asctime)s][%(module)s][%(levelname)s] %(message)s"
logging.basicConfig(format=logFormatter, datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger(__name__)

if os.getenv("BONSAI_GYM_DEBUG"):
    log.setLevel(level=logging.DEBUG)
    log.debug("Debug log enabled.")
else:
    log.setLevel(level=logging.INFO)
