from ariadne import MutationType
from sqlalchemy import select
from sqlalchemy.orm import selectinload
# from sqlalchemy import select
from app.db import AsyncSessionLocal
from app.models import User, Project, Task
from app.utils import get_hashed_password

mutation = MutationType()


@mutation.field("createUser")
async def resolve_user_create(_, info, input):
    hashed_password = get_hashed_password(input["password"])
    user = User(username=input["username"], email=input["email"], password=hashed_password, role=input["role"])
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@mutation.field("createProject")
async def resolve_project_create(_, info, input):
    async with AsyncSessionLocal() as session:
        project = Project(title=input["title"], owner_id=input["owner_id"])
        session.add(project)
        await session.commit()
        await session.refresh(project)

        # Eager-load owner before returning
        project = (
            (await session.execute(
                select(Project)
                .options(selectinload(Project.owner))
                .where(Project.id == project.id)
            ))
        ).scalar_one_or_none()
        return project


@mutation.field("createTask")
async def resolve_task_create(_, info, input):
    async with AsyncSessionLocal() as session:
        project = await session.get(Project, input["project_id"])
        if not project:
            raise Exception("Project not found")

        assignee = await session.get(User, input["assignee_id"])
        if not assignee:
            raise Exception("Assignee not found")

        task = Task(description=input["description"], priority=input["priority"], status=input["status"], project_id=project.id, assignee_id=assignee.id)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        task = (
            (await session.execute(
                select(Task).options(selectinload(Task.project), selectinload(Task.assignee)).where(Task.id == task.id)
            ))
        ).scalar_one_or_none()
        return task
