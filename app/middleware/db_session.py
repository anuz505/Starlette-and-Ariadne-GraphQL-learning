from app.db.session import AsyncSessionLocal


class DBSessionMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async with AsyncSessionLocal() as session:
            scope.setdefault("state", {})["session"] = session
            try:
                await self.app(scope, receive, send)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
