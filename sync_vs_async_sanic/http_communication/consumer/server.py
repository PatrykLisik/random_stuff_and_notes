import logging
from asyncio import sleep

from sanic import Sanic, json

app = Sanic("HTTP_Consumer")


def configure_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.propagate = True
    return logger


configure_logger("sanic.access", logging.INFO)


@app.route("/consume/<sleep_time:float>")
async def instant_consume(request, sleep_time: float):
    print("access")
    await sleep(sleep_time)
    return json({"status": "ok"})
