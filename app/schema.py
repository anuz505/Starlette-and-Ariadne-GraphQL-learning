from pathlib import Path
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from ariadne import ObjectType, load_schema_from_path, make_executable_schema
from app.resolvers import query, mutation


user_type = ObjectType("User")
project_type = ObjectType("Project")

type_defs = load_schema_from_path(
    str(Path(__file__).resolve().parent.parent / "graphql" / "schema.graphql")
)
schema = make_executable_schema(type_defs, query, user_type, mutation, project_type)
