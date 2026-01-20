import time
import os

import redis
from flask import Flask, request, redirect, url_for, send_from_directory

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379, decode_responses=True)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_FILENAME = "w3-jobs-done.gif"
GIF_THRESHOLD = 10


def incr_key(key: str) -> int:
    retries = 5
    while True:
        try:
            return int(cache.incr(key))
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def get_int(key: str) -> int:
    retries = 5
    while True:
        try:
            val = cache.get(key)
            return int(val) if val is not None else 0
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/")
def hello():
    page_views = incr_key("hits")
    worker_ticks = get_int("worker_ticks")

    gif_html = ""
    if worker_ticks >= GIF_THRESHOLD:
        gif_html = f"""
        <h2>Job's Done.</h2>
        <img src="/w3-gif" alt="Jobs done" />
        """

    return f"""
    <html>
        <body>
            <h1>Hello World!</h1>

            <p><strong>Page views:</strong> {page_views}</p>
            <p><strong>Worker ticks:</strong> {worker_ticks}</p>

            {gif_html}

            <form action="/reset" method="post">
                <button type="submit">Reset counters</button>
            </form>
        </body>
    </html>
    """


@app.route("/w3-gif")
def w3_gif():
    return send_from_directory(APP_DIR, GIF_FILENAME)


@app.route("/reset", methods=["POST"])
def reset():
    cache.set("hits", 0)
    cache.set("worker_ticks", 0)
    return redirect(url_for("hello"))