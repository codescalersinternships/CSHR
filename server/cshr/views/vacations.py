from server.cshr.serializers.vacations import (
    VacationsCommentsSerializer,
    VacationsSerializer,
)
from typing import List
from server.cshr.serializers.vacations import (
    VacationsUpdateSerializer,
    UserVacationBalanceSerializer,
    UserBalanceUpdateSerializer,
)
from server.cshr.api.permission import IsSupervisor, UserIsAuthenticated, IsAdmin
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.models.users import User
from server.cshr.utils.vacation_balance_helper import StanderdVacationBalance
from server.cshr.services.users import get_user_by_id
from server.cshr.services.vacations import (
    get_vacation_by_id,
    get_all_vacations,
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.api.response import CustomResponse
from datetime import datetime
from server.cshr.utils.update_change_log import (
    update_vacation_change_log,
    update_vacation_comment_log,
)
from server.cshr.utils.email_messages_templates import (
    get_vacation_request_email_template,
    get_vacation_reply_email_template,
)
from server.cshr.celery.send_email import send_email_for_request
from server.cshr.celery.send_email import send_email_for_reply
from server.cshr.models.vacations import Vacation
from server.cshr.services.vacations import get_vacations_by_user
from server.cshr.utils.redis_functions import (
    set_notification_request_redis,
    set_notification_reply_redis,
)


class VacationBalanceApiView(GenericAPIView):
    """Class VacationBalance to update or post vacation balance by only admin."""

    serializer_class = VacationsSerializer
    permission_classes = [IsAdmin]

    def post(self, request: Request) -> Response:
        pass


class BaseVacationsApiView(ListAPIView, GenericAPIView):
    """Class Vacations_APIView to create a new vacation into database or get all"""

    serializer_class = VacationsSerializer
    permission_classes = [UserIsAuthenticated]

    def post(self, request: Request) -> Response:
        """Method to create a new vacation request"""
        serializer = self.get_serializer(data=request.data)
        v = StanderdVacationBalance()
        if (
            type(request.data["end_date"]) == str
            and type(request.data["end_date"]) == str
        ):
            from_date: List[str] = request.data.get("from_date").split(
                "-"
            )  # Year, month, day
            end_date: List[str] = request.data.get("end_date").split(
                "-"
            )  # Year, month, day
            converted_from_date: datetime = datetime(
                year=int(from_date[0]), month=int(from_date[1]), day=int(from_date[2])
            ).date()
            converted_end_date: datetime = datetime(
                year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2])
            ).date()
            request.data["from_date"] = converted_from_date
            request.data["end_date"] = converted_end_date

        if serializer.is_valid():
            balance = v.check_balance(
                user=request.user,
                reason=serializer.validated_data.get("reason"),
                start_date=serializer.validated_data.get("from_date"),
                end_date=serializer.validated_data.get("end_date"),
            )
            if balance is not True:
                return CustomResponse.bad_request(message=balance)
            serializer.save(
                type=TYPE_CHOICES.VACATIONS,
                status=STATUS_CHOICES.PENDING,
                applying_user=request.user,
            )
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            msg = get_vacation_request_email_template(
                request.user, serializer.data, url
            )
            set_notification_request_redis(serializer.data, url)
            send_email_for_request(request.user.id, msg, "Vacation request")
            return CustomResponse.success(
                status_code=201, message="Successfully updated balance"
            )
        return CustomResponse.bad_request(error=serializer.errors)

    def get_queryset(self) -> Response:
        """method to get all vacations"""
        query_set: List[Vacation] = get_all_vacations()
        return query_set


class VacationsHelpersApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsSerializer
    permission_classes = [UserIsAuthenticated]
    """Class Vacations_APIView to delete  vacation from database or get certain vacation"""

    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single vacation by id"""
        print(id)
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(
                message="vacation is not found", status_code=404
            )

        serializer = VacationsSerializer(vacation)
        return CustomResponse.success(
            data=serializer.data, message="vacation request found", status_code=200
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a vacation request by id"""
        vacation = get_vacation_by_id(id=id)
        if vacation is not None:
            vacation.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found", status_code=404)


class VacationUserApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsUpdateSerializer
    permission_classes = [UserIsAuthenticated]

    def get(self, request: Request) -> Response:
        """method to get all vacations for certain user"""
        current_user: User = get_user_by_id(request.user.id)
        if current_user is None:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
        vacations = get_vacations_by_user(current_user.id)
        serializer = VacationsSerializer(vacations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="vacation requests found", status_code=200
        )


class VacationsUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsUpdateSerializer
    permission_classes = [IsSupervisor]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")
        serializer = self.get_serializer(vacation, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)

        if serializer.is_valid():

            serializer.save(approval_user=current_user)
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            msg = get_vacation_reply_email_template(current_user, vacation, url)

            bool = send_email_for_reply.delay(
                current_user.id, vacation.applying_user.id, msg, "Vacation reply"
            )
            if bool:
                return CustomResponse.success(
                    data=serializer.data,
                    message="vacation request updated",
                    status_code=202,
                )
            else:
                return CustomResponse.not_found(
                    message="user is not found", status_code=404
                )

        return CustomResponse.bad_request(
            data=serializer.errors, message="vacation failed to update"
        )


class VacationsAcceptApiView(ListAPIView, GenericAPIView):
    permission_classes = [IsSupervisor]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")
        current_user: User = get_user_by_id(request.user.id)
        vacation.approval_user = current_user
        vacation.status = STATUS_CHOICES.APPROVED
        vacation.save()
        url = request.build_absolute_uri()
        bool1 = set_notification_reply_redis(vacation, "accepted", url)
        msg = get_vacation_reply_email_template(current_user, vacation, url)
        bool2 = send_email_for_reply.delay(
            current_user.id, vacation.applying_user.id, msg, "Vacation reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="vacation request accepted", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class VacationsRejectApiView(ListAPIView, GenericAPIView):
    permission_classes = [IsSupervisor]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")
        current_user: User = get_user_by_id(request.user.id)
        vacation.approval_user = current_user
        vacation.status = STATUS_CHOICES.REJECTED
        vacation.save()
        url = request.build_absolute_uri()
        bool1 = set_notification_reply_redis(vacation, "rejected", url)
        msg = get_vacation_reply_email_template(current_user, vacation, url)
        bool2 = send_email_for_reply.delay(
            current_user.id, vacation.applying_user.id, msg, "Vacation reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="vacation request rejected", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class VacationApprovalAPIView(GenericAPIView):
    """Use this class endpoint to change approved user value."""

    serializer_class = VacationsSerializer
    permission_classes = [IsAdmin | IsSupervisor]

    def put(self, request: Request, id: str) -> Request:
        """Use this endpoint to approve request."""
        vacation = get_vacation_by_id(id=id)
        vacation.approval_user = request.user
        vacation.status = request.data["status"]
        comment = request.data.get("comment")
        comment_ = {"user": request.user.id, "comment": comment}
        update_vacation_change_log(vacation, str(datetime.today()), comment_)
        return CustomResponse.success(
            data=VacationsSerializer(vacation).data,
            status_code=202,
            message="vacation change log and status updated",
        )


class VacationCommentsAPIView(GenericAPIView):
    """Use this endpoint to add a comment as a user."""

    permission_classes = [UserIsAuthenticated]
    serializer_class = VacationsCommentsSerializer

    def put(self, request: Request, id: str) -> Request:
        """Use this endpoint to approve request."""
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.bad_request(status_code=404)
        comment = request.data.get("comment")
        comment_ = {"user": request.user.id, "comment": comment}
        update_vacation_comment_log(vacation, comment_)
        return CustomResponse.success(
            data=comment_, status_code=202, message="vacation comment added"
        )


class UserVacationBalanceUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = UserVacationBalanceSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request):
        yourdata = request.data
        serializer = UserVacationBalanceSerializer(data=yourdata)
        if serializer.is_valid():
            v = StanderdVacationBalance()
            v.bulk_write(dict(serializer.data))
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="base balance updated"
            )
        return CustomResponse.bad_request(
            data=serializer.error, message="failed to update base balance"
        )


class UserBalanceUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = UserBalanceUpdateSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request):
        yourdata = request.data
        serializer = UserBalanceUpdateSerializer(data=yourdata)
        if serializer.is_valid():
            vh = StanderdVacationBalance()
            ids = serializer.data["ids"]
            type = serializer.data["type"]
            new_value = serializer.data["new_value"]
            for id in ids:
                try:
                    u = get_user_by_id(id=int(id))
                except User.DoesNotExist:
                    return CustomResponse.bad_request(
                        data=serializer.error, message="failed to update balance"
                    )
                vh.check(u)
                v = u.vacationbalance
                vh.update_balance(type, v, new_value)
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="Users' balance updated"
            )
        return CustomResponse.bad_request(
            data=serializer.error, message="failed to update balance"
        )


class UserVacationBalanceApiView(GenericAPIView):
    serializer_class = UserVacationBalanceSerializer
    permission_classes = [
        UserIsAuthenticated,
    ]

    def get(self, request: Request) -> Response:
        """Get method to get all user balance"""
        user: User = get_user_by_id(request.user.id)
        v: StanderdVacationBalance = StanderdVacationBalance()
        balance = v.check(user)
        return CustomResponse.success(
            message="Baance founded.", data=self.get_serializer(balance).data
        )
