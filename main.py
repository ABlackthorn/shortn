from fastapi import FastAPI
import logging
from container import Container
from routers.link_router import link_router

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

container = Container()
container.wire(packages=['routers'])

app = FastAPI()

app.include_router(link_router)
