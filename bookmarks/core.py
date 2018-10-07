import json

from flask import (
    Flask,
    render_template,
    request
)


app = Flask(__name__)
bookmark_file = 'bookmarks.json'
key_file = "key.json"
bookmarks = []
key = ""
err_response = {'error': 'Invalid key'}

@app.before_first_request
def load_bookmarks():
    global bookmarks
    global key
    with open(bookmark_file, "r") as bookmark_data:
        bookmarks = json.load(bookmark_data)

    with open(key_file, "r") as key_data:
        key = json.load(key_data)['key']


@app.route("/")
def hello():
    return render_template("page.html", bookmarks=bookmarks)


@app.route("/api/bookmarks", methods=['GET', 'POST', 'PUT'])
def api():
    global bookmarks
    if request.method == 'GET':
        return json.dumps(bookmarks)

    request_data = json.loads(request.data)
    if (request_data['key'] != key):
        return json.dumps(err_response);

    if request.method == 'PUT':
        bookmarks = request_data['bookmarks']
    elif request.method == 'POST':
        for bookmark in request_data['bookmarks']:
            if bookmark not in bookmarks:
                bookmarks.append(bookmark)

    # Write out the bookmark data so it will be there when the app launches
    # next
    with open(bookmark_file, "w+") as bookmark_out:
        json.dump(bookmarks, bookmark_out)

    response = {'error': None, 'bookmarks': bookmarks}

    return json.dumps(response)
