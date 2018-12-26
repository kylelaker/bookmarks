"""
Drops all data from the bookmark database. This should be used to remove all
the bookmarks and related data for testing purposes.
"""

from bookmarks.db import db
db.drop_all()
