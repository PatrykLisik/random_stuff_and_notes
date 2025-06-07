import logging
from asyncio import sleep
import sys
from sanic import Sanic, json

app = Sanic("HTTP_Consumer", )


def configure_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.propagate = True
    return logger


configure_logger("sanic.access", logging.DEBUG)
logger = configure_logger("app", logging.INFO)


@app.route("/consume/<sleep_time:float>", methods=["POST", "GET"])
async def instant_consume(request, sleep_time: float):
    logger.info(f"access {sleep_time}")
    await sleep(sleep_time)
    return json({"status": "ok"})
