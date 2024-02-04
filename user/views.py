from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import parser_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from user.serializers import (
    UserSerializer,
    UserPostSerializer,
    UserPatchSerializer,
)
from user.swagger_params import *


# *****************Pagination******************
class UserlistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# *****************Pagination******************


class UserViewset(ModelViewSet):
    """
    A viewset that provides CRUD operations for the User model.
    """

    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = (FormParser, MultiPartParser)
    default_serializer_class = UserSerializer
    pagination_class = UserlistPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ["username", "email"]
    ordering_fields = ["username", "email", "created_at", "updated_at"]
    queryset = User.objects.all()
    serializer_classes = {
        "create": UserPostSerializer,
        "partial_update": UserPatchSerializer,
    }

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            return [AllowAny()]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        """
        Get the appropriate serializer class based on the request action.
        Returns the serializer class for the given request action.
        """
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @swagger_auto_schema(
        operation_summary="Get a single user's information", tags=["user"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Get a single user's information.

        Parameters:
            request, *args, **kwargs

        Returns:
            Response: The HTTP response object with user information.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get a list of user's information",
        tags=["user"],
        manual_parameters=userlist_parameters,
    )
    def list(self, request, *args, **kwargs):
        """
        Get a list of user information.

        search_fields includes "first_name", "last_name", "username", "email"
        ordering_fields includes "id", "username", "email", "role_type"

        Parameters:
            request, *args, **kwargs

        Returns:
            Response: The HTTP response object with a list of users.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a user's information",
        tags=["user"],
        manual_parameters=userpatch_parameters,
    )
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        user_instance = self.get_object()

        if response.status_code != status.HTTP_200_OK:
            return response  # Return early if the update failed

        user_instance.save()
        response.data = {
            "message": "The information has been updated.",
            "details": {
                "id": user_instance.id,
                "username": user_instance.username,
                "email": user_instance.email,
            },
        }

        return response

    @swagger_auto_schema(
        operation_summary="Delete a user",
        tags=["user"],
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a user
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a user",
        tags=["user"],
    )
    def create(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")

            user = User.objects.filter(email=email).first()
            if not user:
                serializer = self.get_serializer_class()(data=request.data)
                if serializer.is_valid():
                    user = serializer.save(is_active=True)
                    return Response(
                        {
                            "message": "User successfully registered",
                            "details": {
                                "id": user.id,
                                "username": user.username,
                                "email": user.email,
                            },
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response({"message": str(serializer.errors)}, status=400)

            else:
                return Response({"message": "Email is already registered"}, status=400)

        except Exception as error:
            return Response({"message": str(error)}, status=400)


class UserSignIn(APIView):
    """
    API view to sign in a user.
    This view handles user sign-in functionality and returns a token if the provided credentials are valid.

    Parameters:
        - username, password

    Returns:
        - 200 OK: If sign-in is successful, returns a JSON response with the following keys:
            - token (str): Authentication token for the user.
            - user_id (int): The primary key of the authenticated user.
            - email (str): The email address of the authenticated user.
            - username (str): The username of the authenticated user.
        - 400 Bad Request: If the provided username or email does not exist in the system.
        - 403 Forbidden: If the provided password is incorrect.
        - 400 Bad Request: If the user is inactive and cannot be authenticated.

    """

    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Sign in a user",
        tags=["user"],
        manual_parameters=signin_parameters,
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user sign-in using provided credentials.

        Args:
            request, *args, **kwargs

        Returns:
        - Response:If successful, returns a Response containing the user's authentication token and relevant user information.
                   If the user is inactive, returns a Response with status code 400 and a message indicating the user's status.
                   If the provided password is incorrect, returns a Response with status code 403 and a message indicating an invalid password.
                   If the user does not exist, returns a Response with status code 400 and a message indicating that the user does not exist.

        """
        username = request.data.get("username")
        password = request.data.get("password")
        if User.objects.filter(Q(username=username)).exists():
            user = User.objects.filter(Q(username=username))[0]
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "token": token.key,
                        "user_id": user.pk,
                        "email": user.email,
                        "username": user.username,
                    }
                )
            return Response({"message": "Invalid password"}, status=403)
        return Response({"message": "User does not exist."}, status=400)


class UserLogoOut(APIView):
    """
    A view for user sign out.

    Permission Classes:
    - IsAuthenticated: Only authenticated users can access this view.

    Methods:
    post(self, request, *args, **kwargs) -- Logout the authenticated user.

    """

    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Sign out a user",
        tags=["user"],
    )
    def post(self, request, *args, **kwargs):
        """
        Logout the authenticated user.

        Parameters:
            request, *args, **kwargs

        Returns:
        - Response: If the user is successfully , returns a Response with status code 200 and a success message.
                   If an error occurs during logout, returns a Response with status code 400 and an error message.

        """
        try:
            logout(request)
            return Response(
                {"message": "User logged out successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {"message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )


@swagger_auto_schema(
    method="post",
    operation_summary="Change user password",
    tags=["user"],
    manual_parameters=changepassword_parameters,
)
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@parser_classes((FormParser, MultiPartParser))
def change_password(request):
    """
    Change user password.

    This endpoint allows an authenticated user to change their password by providing the old password,
    the new password, and confirming the new password.

    Parameters:
    - request (HttpRequest): The HTTP request object containing user data.

    Returns:
    - Response: If the password change is successful, returns a Response with status code 201 and a success message.
               If the new password and confirm password do not match, returns a Response with status code 400 and an error message.
               If the old password provided is incorrect, returns a Response with status code 400 and an error message.

    """
    old_password = request.data.get("old_password", None)
    new_password = request.data.get("new_password", None)
    confirm_password = request.data.get("confirm_password", None)
    user = authenticate(username=request.user.username, password=old_password)

    if user is not None:
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": "Password Successfuly Updated."},
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "New and Confirm passwords do not match."},
            )

    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"message": "Incorrect old password"},
        )
    