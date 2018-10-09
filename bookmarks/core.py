import json

from flask import (
    Flask,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy as sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookmarks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sqlalchemy(app)

key_file = "key.json"
key = ""


@app.before_first_request
def init():
    db.create_all()
    global key
    with open(key_file, "r") as key_data:
        key = json.load(key_data)['key']


@app.route("/")
def hello():
    return render_template("page.html", bookmarks=Bookmark.query.all())

@app.route("/api/bookmarks", methods=['GET'])
def api_get():
    return json.dumps(Bookmark.query.all(), cls=BookmarkEncoder)

@app.route("/api/bookmarks", methods=['POST'])
def api_post():
    if request.method == 'GET':
        return json.dumps(Bookmark.query.all(), cls=BookmarkEncoder)

    try:
        request_data = json.loads(request.data)
    except ValueError:
        return json.dumps({'error': 'Invalid JSON'}), 400

    if 'key' not in request_data:
        return json.dumps({'error': 'No API key provided'}), 403
    elif (request_data['key'] != key):
        return json.dumps({'error': 'Invalid key'}), 401

    for bookmark in request_data['bookmarks']:
        if not bookmark_exists(bookmark):
            db.session.add(Bookmark(url=bookmark['url'], desc=bookmark['desc']))

    db.session.commit()

    response = {'error': None, 'bookmarks': Bookmark.query.all()}

    return json.dumps(response, cls=BookmarkEncoder)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    desc = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return ("<Bookmark %r, %r>" % (self.url, self.desc))


class BookmarkEncoder(json.JSONEncoder):
    def default(self, o):
        return {'id': o.id, 'url': o.url, 'desc': o.desc}


def bookmark_decode(json_obj):
    if 'id' in json_obj and 'url' in json_obj and 'desc' in json_obj:
        return Bookmark(id=id, url=url, desc=desc)


def bookmark_exists(bookmark):
    for bmark in Bookmark.query.all():
        if bmark.url == bookmark['url'] or bmark.desc == bookmark['desc']:
            return True
    return False

def main():
    pass
