import httpx
import requests
from httpx import Limits
from sanic import Sanic, json

URL = "http://http_consumer_server:8080/instant_consume/0.5"

app = Sanic("HTTP_Consumer")


client = httpx.AsyncClient(limits=Limits(max_connections=200))


@app.post("/make_request_httpx_async")
async def make_request_httpx_async(request):
    response = await client.post(URL)
    return json(response.json())


@app.post("/make_request_httpx_sync")
async def make_request_httpx_sync(request):
    response = httpx.post(URL)
    return json(response.json())


@app.post("/make_request_requests")
async def make_request_requests(request):
    response = requests.post(URL)
    return json(response.json())
