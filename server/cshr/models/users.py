""" database user model """

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.office import Office
from server.cshr.models.skills import Skills


class TEAM(models.TextChoices):
    """enum class for team options"""
    # Dev-QA-Ops-Marketing-Management-Accounting

    DEV = "Development"
    QA = "Quality assurance"
    OPS = "Operations"
    MARKETING = "Marketing"
    MANAGEMENT = "Management"
    ACCOUNTING = "Accounting"


class USER_TYPE(models.TextChoices):
    """types of users"""
    # User-Admin-supervisor
    ADMIN = "Admin", "admin"
    USER = "User", "user"
    SUPERVISOR = "Supervisor", "supervisor"


class User(AbstractBaseUser, TimeStamp):
    """main user model"""
    USERNAME_FIELD = "Email"
    FirstName = models.CharField(max_length=45, null=False)
    LastName = models.CharField(max_length=45, null=False)
    Email = models.EmailField(max_length=45, null=False)
    MobileNumber = models.CharField(max_length=15, null=True, blank=True)
    TelegramLink = models.CharField(max_length=100, null=True, blank=True)
    Birthday = models.DateField(null=False)
    Team = models.CharField(
        max_length=20, null=False,
        choices=TEAM.choices
    )
    Salary = models.JSONField(default=list, null=False)
    Location_id = models.ForeignKey(
        Office,
        on_delete=models.CASCADE
    )
    Skills_ids = models.ManyToManyField(
        Skills,
        related_name="skills",
        null=False
    )
    User_type = models.CharField(
        max_length=20,
        null=False,
        choices=USER_TYPE.choices
    )
