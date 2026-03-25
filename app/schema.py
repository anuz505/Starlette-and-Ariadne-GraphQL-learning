from pathlib import Path

from ariadne import load_schema_from_path, make_executable_schema

from app.resolvers.query import query


type_defs = load_schema_from_path(
    str(Path(__file__).resolve().parent.parent / "graphql" / "schema.graphql")
)
schema = make_executable_schema(type_defs, query)
