from dataclasses import dataclass
import os
from os import getenv, environ
from os import getenv as getenv2, environ as environ2, system as sys2
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

import first as second

ENV_1 = os.environ["ENV_1_os"]
ENV_2 = os.environ["ENV_2_os"]
ENV_2_0 = environ["ENV_2_0"]
ENV_2_3 = environ.get("ENV_2_3")
cpu = os.cpu_count()


ENV_2_1 = os.environ.get("ENV_2_1")

ENV_2_2 = os.environ.get("ENV_2_2")

def on_ok(
    a,
    b,
    c,
    **load,
):
    load["key"] = {"form": {"auth_key": "123213"}}
    a = b + c + a
    load["a"]=a
    if load is dict:
        print("dict")
    return load


@dataclass
class Tes:
    b = 1
    pass


a = Tes()
n = a.b
c = a["da"]

ENV_3 = os.environ["ENV_3"]
ENV_4 = os.environ["ENV_4"]
ENV_5 = os.getenv(key="ENV_5", default={"k":"v"})
ENV_5_0 = os.getenv(default={"k":"v"}, key="ENV_5_0")
ENV_5_1 = os.getenv("ENV_5_1", default={"k":"v"})
ENV_6 = os.getenv("ENV_6", "value")
ENV_6_1 = os.getenv("ENV_6_1")
ENV_6_2 = os.getenv(key="ENV_6_2")
ENV_7 = getenv("ENV_7", "value")
ENV_7_1 = getenv("ENV_7_1", default="value")

class Settings1(BaseSettings):
    # default won't be validated
    foo: int = Field('test', validate_default=False)
