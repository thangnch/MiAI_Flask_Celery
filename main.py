from flask import Flask, request, jsonify
import time, math
from celery_config import celery
from transformers import pipeline
from tasks import execute_llm

app = Flask("myapp")
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery.conf.update(app.config)

@app.route("/")
def home():
    return "Home page"


@app.route("/process") # Ném vào redis
def process():
    task  = execute_llm.apply_async(args=["I love you and"])
    return jsonify({
        'task_id': task.id
    }), 200


@app.route("/getstatus/<task_id>") # Ném vào redis
def getstatus(task_id):
    task  = execute_llm.AsyncResult(task_id)
    if task.ready():
        result = task.result
    else:
        result = "Running"
    return  result




app.run(host="0.0.0.0", port=5005)
