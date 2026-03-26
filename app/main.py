from contextlib import asynccontextmanager
from app.utils import custom_error_formatter
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from app.middleware import DBSessionMiddleware
from app.db import init_db, drop_db
from .schema import schema


@asynccontextmanager
async def lifesapn(app):
    await init_db()
    yield
    await drop_db()


async def get_context_value(request: Request, _data):
    return {
        "request": request,
        "session": request.state.session,
    }


graphql_app = GraphQL(
                      schema,
                      debug=True,
                      error_formatter=custom_error_formatter,
                      context_value=get_context_value
                    )

routes = [
    Route("/health", lambda r: JSONResponse({"status": "ok"})),
    Mount("/graphql", graphql_app),
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifesapn,
)

app.add_middleware(DBSessionMiddleware)
