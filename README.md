# Bookmarks

My bookmark manager

## Building

`python setup.py develop` or `pip install -e .`

## Running

Create a `config.json` file in the current directory with the following items:

 - `key`: The API key as a string. Any requests that mutate state require this key
 - `user`: The name of the user

Run `bookmarks` to start the Flask server.
