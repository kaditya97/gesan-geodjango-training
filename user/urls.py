from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from user.views import (
    UserSignIn,
    UserLogoOut,
    change_password,
    UserViewset,
)

router = routers.DefaultRouter()
router.register(r"user", UserViewset, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("sign-in/", UserSignIn.as_view()),
    path("logout/", UserLogoOut.as_view()),
    path("change-password/", change_password, name="change_password"),
]