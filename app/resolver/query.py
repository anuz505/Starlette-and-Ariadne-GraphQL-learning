from ariadne import QueryType
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import User, Project
from app.core import LoggerSetup
from app.db import AsyncSessionLocal
from app.models.task_model import Task

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


@query.field("tasks")
async def resolve_tasks(_, info, status=None, priority=None, search=None, limit=20, offset=0,  project_id=None, assignee_id=None):
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    stmt = (
        select(Task).options(
            selectinload(Task.project),
            selectinload(Task.assignee)
        )
        .order_by(Task.created_at.desc())
    )

    if status is not None:
        stmt = stmt.where(Task.status == status)

    if priority is not None:
        stmt = stmt.where(Task.priority == priority)

    if project_id is not None:
        stmt = stmt.where(Task.project_id == project_id)

    if assignee_id is not None:
        stmt = stmt.where(Task.assignee_id == assignee_id)

    if search:
        stmt = stmt.where(Task.description.ilike(f"%{search}%"))

    stmt = stmt.limit(limit).offset(offset)
    async with AsyncSessionLocal() as session:
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        logger.info(
            "Fetched %d tasks (status=%s, priority=%s, project_id=%s, assignee_id=%s, search=%s, limit=%d, offset=%d)",
            len(tasks),
            status,
            priority,
            project_id,
            assignee_id,
            search,
            limit,
            offset,
        )
        return tasks


@query.field("task")
async def resolve_task(_, info, id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Task).options(
                selectinload(Task.project),
                selectinload(Task.assignee),
            ).where(Task.id == id)
        )
        return result.scalar_one_or_none()
