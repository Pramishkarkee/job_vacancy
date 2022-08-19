from functools import wraps
from django.shortcuts import redirect


def check_permission(profiletype):
    def main_decorator(viewfunc):
        @wraps(viewfunc)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.profile_type == profiletype:
                    return viewfunc(request, *args, **kwargs)
                return redirect("about", profile_type=profiletype)
            return redirect("login")

        return wrapper

    return main_decorator
