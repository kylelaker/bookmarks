import json

from flask_sqlalchemy import SQLAlchemy as sqlalchemy

import bookmarks.util
from bookmarks import app

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookmarks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sqlalchemy(app)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    desc = db.Column(db.String(80), nullable=False)
    favicon = db.Column(db.Text, unique=False, nullable=True)

    def __repr__(self):
        return ("<Bookmark %r, %r>" % (self.url, self.desc))


class BookmarkEncoder(json.JSONEncoder):
    def default(self, o):
        return {'id': o.id, 'url': o.url, 'desc': o.desc}


def bookmark_decode(json_obj):
    if 'id' in json_obj and 'url' in json_obj and 'desc' in json_obj:
        return Bookmark(id=id, url=url, desc=desc)
