"""
Types and methods relating to the database connection.
"""

import json

from flask_sqlalchemy import SQLAlchemy as sqlalchemy

from bookmarks import app

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookmarks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sqlalchemy(app)


class Bookmark(db.Model):
    """
    A single Bookmark element to be stored in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    desc = db.Column(db.String(80), nullable=False)
    favicon = db.Column(db.Text, unique=False, nullable=True)

    def __repr__(self):
        return "<Bookmark %r, %r>" % (self.url, self.desc)


class BookmarkEncoder(json.JSONEncoder):
    """
    Encodes a bookmark as a JSON object.
    """

    def default(self, o):
        return {'id': o.id, 'url': o.url, 'desc': o.desc, 'favicon': o.favicon}


def bookmark_decode(json_obj):
    """
    Decodes a JSON object to a Bookmark
    :param json_obj: The object to deserialize
    :return: A Bookmark
    """

    if 'id' in json_obj and 'url' in json_obj and 'desc' in json_obj:
        return Bookmark(id=json_obj['id'], url=json_obj['url'], desc=json_obj['desc'])
