"""This file contains everything related to the request functionalty."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.api.permission import IsSupervisor, IsUser
from server.cshr.api.response import CustomResponse
from server.cshr.services.requests import requests_format_response
from typing import Dict


class RequestApiView(GenericAPIView):
    permission_classes = [IsSupervisor | IsUser]

    def get(self, request: Request) -> Response:
        res: Dict = requests_format_response(request.user)
        return CustomResponse.success(data=res)
