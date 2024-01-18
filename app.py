"""
Counter Application
"""

import json
import os
from datetime import datetime

from flask import Flask, request
from flask.templating import render_template
from flask.wrappers import Response

import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_POST", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "thisispassword")
APIKEY = os.environ.get("APIKEY", "thisisapikey")
KEEP_ALIVE = 1


MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = os.environ.get("MQTT_POST", 1883)


app = Flask(__name__)

r = redis.Redis(host=REDIS_HOST, port=int(
    REDIS_PORT), db=1, password=REDIS_PASSWORD)


def init_redis():
    """
    initial function fo redis
    """
    r.set("count", 0)
    r.set("kpm", 0)
    r.set("control", "stop", )
    print("initial redis...")


def update_kpm():
    """
    Update key press per minutes
    """
    now = datetime.now()
    print(now)


init_redis()


@app.get("/")
def home():
    """
    home page
    """
    return render_template("display.html")


@app.get("/green")
def green():
    """
    green display
    """
    return render_template("green.html")


@app.get("/g2")
def green_2():
    """
    green display
    """
    return render_template("green-2.html")


@app.get("/app")
def index():
    """
    Application Page
    """
    key = request.args.get("key")
    if key != APIKEY:
        return "invalid token"

    return render_template("app.html")


@app.post("/keypress")
def kpm():
    """
    on key press api
    """
    request_data = request.get_json()
    assert request_data is not None

    r.set("kpm", request_data["kpm"])

    print(request_data)

    return {
        "success": "set_key_per_minutes",
    }


@app.get("/resetkpm")
def reset_kpm():
    """
    reset key per minutes
    """

    r.set("kpm", 0)

    print("reset kpm")

    return {
        "message": "reset key per minutes"
    }


@app.get("/stream")
def stream():
    """
    stream server data to pages
    """
    def get_data():
        while True:
            # time.sleep(0.5)
            count = r.get("count")
            control = r.get("control")
            key_per_minutes = r.get("kpm")

            assert count is not None
            assert control is not None
            assert key_per_minutes is not None

            ret = {
                "count": count.decode("utf-8"),
                "control": control.decode("utf-8"),
                "kpm": key_per_minutes.decode("utf-8"),
            }

            yield f"data: {json.dumps(ret)}\n\n"

    return Response(get_data(), mimetype="text/event-stream")


@app.post("/increase")
def increase():
    """
    increment counter api
    """
    r.incr("count")
    update_kpm()
    return {"status": "increase"}


@app.post("/decrease")
def decrease():
    """
    decrement counter api
    """
    r.decr("count")
    return {"status": "decrease"}


@app.post("/reset")
def reset_counter():
    """
    reset counter
    """
    r.set("count", 0)
    return {"status": "reset counter"}


@app.post("/set/<num>")
def set_counter(num):
    """
    force set counter
    """
    r.set("count", num)
    update_kpm()
    return {
        "status": num,
    }
