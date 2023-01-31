"""
John Doe's Flask API.
"""

from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)
import configparser

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])

@app.route("/<url>")
def hello(url):
    valid = os.path.exists("pages/" + url)

    if valid:
        return send_from_directory("pages/", url)
    elif ".." in url or "~" in url:
        abort(403)
    else:
        abort(404)

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def notFound(e):
    return send_from_directory('pages/', '404.html'), 404

if __name__ == "__main__":
    app.run(debug=config["SERVER"]["DEBUG"], host='0.0.0.0', port=config["SERVER"]["PORT"])
