from litestar import Litestar
from app.core.routers.user_router import user_router
from app.core.routers.service_router import service_router


app = Litestar(
    route_handlers=[
        user_router,
        service_router,
    ],
)
