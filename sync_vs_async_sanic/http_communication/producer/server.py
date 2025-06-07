import httpx
import requests
from httpx import Limits
from sanic import Sanic, json
import logging
import sys

URL = "http://http_consumer_server:8080/instant_consume/0.5"

app = Sanic("HTTP_Consumer")

def configure_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.propagate = True
    return logger


configure_logger("sanic.access", logging.INFO)
logger = configure_logger("app", logging.INFO)


client = httpx.AsyncClient(limits=Limits(max_connections=200))


@app.post("/make_request_httpx_async")
async def make_request_httpx_async(request):
    response = await client.post(URL)
    logging.info(response)
    return json({"status": "ok"})


@app.post("/make_request_httpx_sync")
async def make_request_httpx_sync(request):
    response = httpx.post(URL)
    return json(response.json())


@app.post("/make_request_requests")
async def make_request_requests(request):
    response = requests.post(URL)
    return json(response.json())
