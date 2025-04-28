from typing import Dict

from litestar import Router, get


@get("/")
async def healthcheck() -> Dict:
    return {"Success": True}

service_router = Router(
    path="/healthcheck",
    route_handlers=[healthcheck],
)
