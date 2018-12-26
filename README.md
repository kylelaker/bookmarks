# Bookmarks

My bookmark manager

## Building

`python setup.py develop` or `pip install -e .`

## Running

Create a `config.json` file in the current directory with the following items:

 - `key`: The API key as a string. Any requests that mutate state require this key
 - `user`: The name of the user

The following config items are optional:
 - `host`: The host to use. Default: `0.0.0.0`.
 - `port`: The port to use. Default: `8080`.

Run `bookmarks` to start the Flask server.
