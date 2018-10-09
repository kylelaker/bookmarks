import json

from flask import (
    Flask,
    render_template,
    request
)

from bookmarks import (
    app,
    util,
)
from bookmarks.db import (
    db,
    Bookmark,
    BookmarkEncoder,
)


config_file = "config.json"
key = ""
user = ""


@app.before_first_request
def init():
    db.create_all()
    global key
    global user
    with open(config_file, "r") as config_data:
        config = json.load(config_data)
        key = config['key']
        user = config['user']


@app.route("/")
def hello():
    return render_template("page.html", user=user, bookmarks=Bookmark.query.all())


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
            if not 'url' in bookmark:
                return json.dumps({'error': 'No URL given'}), 400

            if 'desc' in bookmark:
                desc = bookmark['desc']
            else:
                desc = util.get_page_title(bookmark['url'])

            if not desc:
                return json.dumps({'error': 'No description available'}), 400

            db.session.add(Bookmark(url=bookmark['url'], desc=desc))

    db.session.commit()

    response = {'error': None, 'bookmarks': Bookmark.query.all()}

    return json.dumps(response, cls=BookmarkEncoder)


@app.route("/api/bookmarks/<int:id>", methods=['GET'])
def api_get_bookmark(id):
    return json.dumps(Bookmark.query.filter_by(id=id).first_or_404(), cls=BookmarkEncoder)

@app.route("/api/bookmarks/<int:id>", methods=['DELETE'])
def api_delete_bookmark(id):
    bookmark = Bookmark.query.filter_by(id=id).first_or_404()
    db.session.delete(bookmark)
    db.session.commit()
    response = {'error': None, 'bookmark': bookmark}
    return json.dumps(response, cls=BookmarkEncoder)


def bookmark_exists(bookmark):
    for bmark in Bookmark.query.all():
        if bmark.url == bookmark['url']:
            return True
        if 'desc' in bookmark and bmark.url == bookmark['url']:
            return True
    return False


def main():
    app.run()
