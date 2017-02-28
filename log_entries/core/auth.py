import functools

from log_entries.core.exceptions import UnauthorizedAccess


def requires_auth(view_func):
    """Wraps a view and checks that the request is authorized,
    raises an Unauthorized exception if user is not logged."""
    @functools.wraps(view_func)
    def wrapper(request, **kwargs):
        if not request.user.pk:
            raise UnauthorizedAccess()

        return view_func(request, **kwargs)

    return wrapper