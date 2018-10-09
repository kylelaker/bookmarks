from flask import Flask
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'root': {
        'level': 'DEBUG'
    }
})

app = Flask(__name__)


import bookmarks.views
