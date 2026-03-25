from contextlib import asynccontextmanager
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.routing import Route
# from starlette.requests import Request
from starlette.responses import JSONResponse
from app.db import init_db, drop_db
from .schema import schema


@asynccontextmanager
async def lifesapn(app):
    await init_db()
    yield
    await drop_db()

routes = [
    Route("/health", lambda r: JSONResponse({"status": "ok"}))
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifesapn
)


app.mount("/graphql", GraphQL(schema, debug=True))
