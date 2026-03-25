from contextlib import asynccontextmanager

from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse

from app.db import init_db, drop_db
from .schema import schema


@asynccontextmanager
async def lifesapn(app):
    await init_db()
    yield
    await drop_db()


graphql_app = GraphQL(schema, debug=True)


routes = [
    Route("/health", lambda r: JSONResponse({"status": "ok"})),
    Mount("/graphql", graphql_app),
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifesapn,
)
