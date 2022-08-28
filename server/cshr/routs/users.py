from django.urls import path

from server.cshr.views.users import (
    AdminUserAPIView,
    GeneralUserAPIView,
    SupervisorUserAPIView,
)


urlpatterns = [
    path("superView/<str:id>/", SupervisorUserAPIView.as_view({"get": "get_one"})),
    path("superView/", SupervisorUserAPIView.as_view({"get": "get_all"})),
    path(
        "adminView/<str:id>/",
        AdminUserAPIView.as_view({"put": "put", "get": "get_one", "delete": "delete"}),
    ),
    path("adminView/", AdminUserAPIView.as_view({"get": "get_all"})),
    path("", GeneralUserAPIView.as_view({"get": "get_all"})),
    path("<str:id>/", GeneralUserAPIView.as_view({"get": "get_one"})),
]