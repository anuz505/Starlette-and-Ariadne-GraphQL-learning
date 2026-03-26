from ariadne import MutationType
from sqlalchemy import select
from sqlalchemy.orm import selectinload
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


@mutation.field("updateTask")
async def resolve_task_update(_, info, id, input):
    async with AsyncSessionLocal() as session:
        # Fetch the task
        task = await session.get(Task, id)
        if not task:
            raise Exception("Task not found")

        # Optional: fetch new assignee if provided
        if "assignee_id" in input:
            assignee = await session.get(User, input["assignee_id"])
            if not assignee:
                raise Exception("Assignee not found")
            task.assignee_id = assignee.id

        # Optional: fetch new project if provided
        if "project_id" in input:
            project = await session.get(Project, input["project_id"])
            if not project:
                raise Exception("Project not found")
            task.project_id = project.id

        # Update other fields
        for field in ["description", "priority", "status"]:
            if field in input:
                setattr(task, field, input[field])

        # Commit changes
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Eager-load related project and assignee before returning
        task = (
            (await session.execute(
                select(Task)
                .options(selectinload(Task.project), selectinload(Task.assignee))
                .where(Task.id == task.id)
            ))
        ).scalar_one_or_none()

        return task


@mutation.field("deleteTask")
async def resolve_task_delete(_, info, id):
    async with AsyncSessionLocal() as session:
        task = await session.execute(select(Task).where(Task.id == id))
        task = task.scalars().first()
        if not task:
            raise Exception("The task does not exist")
        await session.delete(task)
        await session.commit()
        return True


@mutation.field("deleteProject")
async def resolve_project_delete(_, info, id):
    async with AsyncSessionLocal() as session:
        project = await session.execute(select(Project).where(Project.id == id))
        project = project.scalar_one_or_none()
        if not project:
            raise Exception("The Project does not exist")
        await session.delete(project)
        await session.commit()
        return True
