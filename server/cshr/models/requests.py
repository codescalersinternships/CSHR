from django.db import models

from server.cshr.models.abstracts import TimeStamp


from server.cshr.models.users import User


class TYPE_CHOICES(models.TextChoices):
    """
    it is a list of choices for the request type
    """

    HR_LETTERS = "hr_letters", "HR Letters"
    COMPENSATION = "compensations", "Compensations"
    VACATIONS = "vacations", "Vacations"
    OFFICIAL_DOCUMENT = "official-document", "Official document"


class STATUS_CHOICES(models.TextChoices):
    """
    it is a list of choices for the request status
    """

    REJECTED = "rejected", "Rejected"
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"


class Requests(TimeStamp):
    """Class Requests model for adding a new
    Request automatically  to the database"""

    # to use it User.user_requests.all()

    applying_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="apply_user"
    )
    approval_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="approve_user", null=True
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES.choices)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices)

    def __str__(self) -> str:
        return self.type

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"
