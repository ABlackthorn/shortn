from fastapi import HTTPException
from fastapi import APIRouter, Depends
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from dependency_injector.wiring import Provide, inject
from repositories.link_repository import LinkRepository
from container import Container
from routers import logger
import base64
from datetime import datetime

link_router = APIRouter(
        prefix="/link",
        tags=["links"]
)

@link_router.post("/shorten")
@inject
def shorten_link(link: str, link_repository: LinkRepository = Depends(Provide[Container.link_repository])):
    try:
        #base64 encode the link to avoid SQL injection
        #encode link to utf8
        encoded_link = link.encode('utf-8')
        #b64encode result
        b64link = base64.b64encode(encoded_link)
        #decode to get byte string value
        b64linkdata = b64link.decode()
        #generate formatted creation date
        today = datetime.now()
        date = f"{today.year}/{today.month:02d}/{today.day:02d}"

        print(f"Adding to db : {b64linkdata} created at {date}")
        shortened = link_repository.add_link(b64linkdata, date)
        return shortened
    except Exception as e:
        logger.error(f"Error shortening link : {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)

@link_router.get("/expand/{shortened}")
@inject
async def expand_link(shortened: str, link_repository: LinkRepository = Depends(Provide[Container.link_repository])):
    try:
        #format auto incremented index to integer
        shortened_index = int(shortened)
        b64linkdata = link_repository.get_link_by_shortened_link(shortened_index)
        b64link = b64linkdata.encode()
        #decode b64link
        encoded_link = base64.b64decode(b64link)
        full_link = encoded_link.decode('utf-8')
        return full_link
    except Exception as e:
        logger.error(f"Error expanding link {shortened} : {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
