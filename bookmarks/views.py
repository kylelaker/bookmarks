"""
Various views for the app.
"""

from datetime import datetime
import json

from flask import (
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
config = {}


@app.before_first_request
def init():
    """
    Initialize the app. This creates the database if it does not exist and
    loads in the configuration.
    """

    db.create_all()


@app.route("/")
def bookmarks():
    user = config["user"]
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

    if not validate_key(request_data):
        return json.dumps({'error': 'Invalid API key'}), 403

    app.logger.info("Starting processing")

    for bookmark in request_data['bookmarks']:
        if not bookmark_exists(bookmark):
            if 'url' not in bookmark:
                return json.dumps({'error': 'No URL given'}), 400

            if 'desc' in bookmark:
                desc = bookmark['desc']
            else:
                desc = util.get_page_title(bookmark['url'])

            if not desc:
                return json.dumps({'error': 'No description available'}), 400

            favicon = util.get_favicon_link(bookmark['url'])

            db.session.add(Bookmark(url=bookmark['url'], desc=desc, favicon=favicon))

    db.session.commit()

    app.logger.info("Processing complete")
    response = {'error': None, 'bookmarks': Bookmark.query.all()}

    return json.dumps(response, cls=BookmarkEncoder)


@app.route("/api/bookmarks/<int:id>", methods=['GET'])
def api_get_bookmark(id):
    return json.dumps(Bookmark.query.filter_by(id=id).first_or_404(), cls=BookmarkEncoder)


@app.route("/api/bookmarks/<int:id>", methods=['DELETE'])
def api_delete_bookmark(id):
    try:
        request_data = json.loads(request.data)
    except ValueError:
        return json.dumps({'error': 'Invalid JSON'}), 400

    if not validate_key(request_data):
        return json.dumps({'error': 'Invalid API key'}), 403

    bookmark = Bookmark.query.filter_by(id=id).first_or_404()
    db.session.delete(bookmark)
    db.session.commit()
    response = {'error': None, 'bookmark': bookmark}
    return json.dumps(response, cls=BookmarkEncoder)


def validate_key(data):
    return ('key' in data) and (data['key'] == config['key'])


def bookmark_exists(bookmark):
    for bmark in Bookmark.query.all():
        if bmark.url == bookmark['url']:
            return True
        if 'desc' in bookmark and bmark.url == bookmark['url']:
            return True
    return False


def main():
    global config
    with open(config_file, "r") as config_data:
        config = json.load(config_data)
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 8080)
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
