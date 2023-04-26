import pathlib
import os
import logging
from dotenv import load_dotenv
from logging.config import dictConfig
load_dotenv()

DISCORD_API_SECRET = os.getenv('DISCORD_TOKEN')

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_Loggers": False,
    "formatters":{
        "verbose":{
            "format": "%(Levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard":{
            "format": "%(Levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers":{
        "console": {
            'level': "DEBUG",
            'class':"logging.StreamHandler",
            'formatter': "standard"
        },
        "console2": {
            'level': "WARNING",
            'class':"logging.StreamHandler",
            'formatter': "standard"
        },
    "file": {
            'level': "INFO",
            'class':"logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w",
            'formatter': "verbose"
        },
    },
    "Loggers":{
        "bot": {
            'handlers': ['console'],
            "Level": "INFO",
            "propagate": False
        },
        "discord" : {
            'handlers': ['console2', "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)