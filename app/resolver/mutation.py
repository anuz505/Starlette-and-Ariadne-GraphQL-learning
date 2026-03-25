from ariadne import MutationType
# from sqlalchemy import select
from app.models import User
from app.utils import get_hashed_password

mutation = MutationType()


@mutation.field("createUser")
async def resolve_user_create(_, info, input):
    session = info.context["session"]
    hashed_password = get_hashed_password(input["password"])
    user = User(username=input["username"], email=input["email"], password=hashed_password, role=input["role"])
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
