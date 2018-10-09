import json

from flask import (
    Flask,
    render_template,
    request
)

from bookmarks import app

from bookmarks.db import (
    db,
    Bookmark,
    BookmarkEncoder,
)


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


def bookmark_exists(bookmark):
    for bmark in Bookmark.query.all():
        if bmark.url == bookmark['url'] or bmark.desc == bookmark['desc']:
            return True
    return False


def main():
    app.run()
