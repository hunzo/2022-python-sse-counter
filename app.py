from flask import Flask, request
from flask.templating import render_template
from flask.wrappers import Response
import redis
import json
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_POST", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "thisispassword")
KEEP_ALIVE = 1

MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = os.environ.get("MQTT_POST", 1883)


app = Flask(__name__)

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=1,
    password=REDIS_PASSWORD
)


def init_redis():
    r.set("count", 0)
    r.set("control", "stop")
    print("initial redis...")


init_redis()


@app.get("/app")
def index():
    key = request.args.get("key")
    if key != "test":
        return "invalid token"
 
    return render_template("index.html")


@app.get("/green")
def green():
    return render_template("green.html")


@app.get("/")
def home():
    # key = request.args.get("key")
    # if key != "test":
    # return "invalid token"
    return render_template("app.html")


@app.get("/stream")
def stream():
    def get_data():
        while True:
            # time.sleep(0.5)
            count = r.get("count")
            control = r.get("control")
            ret = {
                "count": count.decode("utf-8"),
                "control": control.decode("utf-8")
            }

            yield f'data: {json.dumps(ret)}\n\n'

    return Response(get_data(), mimetype='text/event-stream')


@app.post("/increase")
def increase():
    r.incr("count")
    return {
        "status": "increase"
    }


@app.post("/decrease")
def decrease():
    r.decr("count")
    return {
        "status": "decrease"
    }


@app.post("/reset")
def reset_counter():
    r.set("count", 0)
    return {
        "status": "reset"
    }


@app.post("/set/<num>")
def set_counter(num):
    r.set("count", num)
    return {
        "status": num,
    }
