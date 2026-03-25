from graphql import GraphQLError


def get_session(info):
    session = info.context.get("session")
    if session is None:
        raise GraphQLError("DB session missing from GraphQL context")
    return session
