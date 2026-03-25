from ariadne import QueryType
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import User, Project
from app.core import LoggerSetup
from app.db import AsyncSessionLocal

logger = LoggerSetup.setup_logger(__name__)

query = QueryType()


@query.field("hello_world")
def resolve_hello_world(_, info):
    return "Hello World"


@query.field("users")
async def resolve_users(_, info):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).order_by(User.created_at.desc()))
        return result.scalars().all()


@query.field("user")
async def resolve_user(_, info, id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()


@query.field("projects")
async def resolve_projects(_, info):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Project).options(selectinload(Project.owner)).order_by(Project.created_at.desc())
        )
        projects = result.scalars().all()
        logger.info("Fetched %d projects", len(projects))
        return projects


@query.field("project")
async def resolve_project(_, info, id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Project).where(Project.id == id))
        return result.scalar_one_or_none()
