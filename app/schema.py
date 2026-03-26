from pathlib import Path
# from sqlalchemy.orm import selectinload
# from sqlalchemy import select
from ariadne import ObjectType, load_schema_from_path, ScalarType, make_executable_schema
from app.resolver import query, mutation
from datetime import date, datetime

datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


user_type = ObjectType("User")
project_type = ObjectType("Project")

type_defs = load_schema_from_path(
    str(Path(__file__).resolve().parent.parent / "graphql" / "schema.graphql")
)
schema = make_executable_schema(type_defs, query, user_type, mutation, project_type, datetime_scalar)
