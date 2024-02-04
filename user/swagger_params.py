from drf_yasg import openapi

groups = ["Admin", "Viewer", "Editor"]

signin_parameters = [
    openapi.Parameter(
        name="username",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        name="password",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]

changepassword_parameters = [
    openapi.Parameter(
        name="old_password",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=True,
        description="The old password of the user.",
    ),
    openapi.Parameter(
        name="new_password",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=True,
        description="The new password of the user.",
    ),
    openapi.Parameter(
        name="confirm_password",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=True,
        description="The new password of the user.",
    ),
]

userlist_parameters = [
    openapi.Parameter(
        name="search",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description="Search query string for filtering user data",
        required=False,
    ),
    openapi.Parameter(
        name="ordering",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description="Query string for ordering the user data",
        required=False,
    ),
]

userpatch_parameters = [
    openapi.Parameter(
        name="username",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=False,
        description="username of the user",
    ),
]
