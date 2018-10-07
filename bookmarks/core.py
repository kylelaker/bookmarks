import json

from flask import (
    Flask,
    render_template,
    request
)


app = Flask(__name__)
bookmark_file = 'bookmarks.json'
bookmarks = []

@app.before_first_request
def load_bookmarks():
    global bookmarks
    with open(bookmark_file, "r") as bookmark_data:
        bookmarks = json.load(bookmark_data)

@app.route("/")
def hello():
    return render_template("page.html", bookmarks=bookmarks)

@app.route("/api/bookmarks", methods=['GET', 'POST', 'PUT'])
def api():
    global bookmarks
    if request.method == 'GET':
        return json.dumps(bookmarks)

    print(request.data)

    if request.method == 'PUT':
        bookmarks = json.loads(request.data)
    elif request.method == 'POST':
        bookmarks += json.loads(request.data)

    with open(bookmark_file, "w+") as bookmark_out:
        json.dump(bookmarks, bookmark_out)

    return json.dumps(bookmarks)
