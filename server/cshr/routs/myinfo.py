from django.urls import path

from ..views.users import SelfUserAPIView


urlpatterns = [path("", SelfUserAPIView.as_view({"get": "get_one", "put": "put"}))]