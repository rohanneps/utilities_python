import logging
from utils.global_variables import LOGFILE, MICROSERVICELOGFILE


logger = logging.getLogger('RESTLOGGER')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(LOGFILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(logging.StreamHandler())
logger.addHandler(handler)



microServiceLogger = logging.getLogger('MICROSERVICELOGGER')
microServiceLogger.setLevel(logging.INFO)

microServicehandler = logging.FileHandler(MICROSERVICELOGFILE)
microServicehandler.setLevel(logging.INFO)
microServiceFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
microServicehandler.setFormatter(microServiceFormatter)

microServiceLogger.addHandler(logging.StreamHandler())
microServiceLogger.addHandler(microServicehandler)