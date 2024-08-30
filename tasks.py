from celery import Celery
from transformers import pipeline

celery = Celery(
    "myapp",
    broker="redis://localhost:6379/0",
    backend= "redis://localhost:6379/0"
)

pipe = pipeline("text-generation", model="openai-community/gpt2")


@celery.task()
def execute_llm(message):
    return pipe(message)