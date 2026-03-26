
def custom_error_formatter(error, debug):
    # error is a GraphQLError
    return {
        "message": str(error),        # Always include message
        "code": getattr(error.original_error, "code", "UNKNOWN"),
        "locations": error.locations,
        "path": error.path
    }
