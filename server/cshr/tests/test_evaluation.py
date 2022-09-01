from rest_framework.test import APITestCase
from django.urls import reverse
from ..models.evaluations import Evaluations
from ..models.users import User
from ..models.office import Office
from rest_framework import status


def createTmp():
    """function to create tmp record"""

    Evaluations.objects.create(user=User.objects.get(id=1), link="testCase")


class EvaluationTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")

        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user1@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="Admin",
        )

        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user2@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="User",
        )

        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user3@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="Supervisor",
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "user1@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "user2@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "user3@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    """test post method"""

    def test_create_evaluation_by_admin(self):
        """test ability of creating a new evaluation by admin"""
        url = reverse("evaluation")
        data = {"link": "testCase", "user": 1}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Evaluations.objects.last().link, "testCase")

    def test_create_evaluation_by_supervisor(self):
        """test unauthorized  evaluation creation by supervisor"""
        url = reverse("evaluation")
        data = {"link": "testCase", "user": 1}
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_evaluation_by_user(self):
        """test unauthorized  evaluation creation by user"""
        url = reverse("evaluation")
        data = {"link": "testCase", "user": 1}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_evaluation_by_unauthenticated_user(self):
        """test unauthorized  evaluation creation by unauthenticated user"""
        url = reverse("evaluation")
        data = {"link": "testCase", "user": 1}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """test get method"""

    def test_get_all_evaluation_by_admin(self):
        """test list evaluations by admin"""
        createTmp()
        """create a new record"""
        url = reverse("evaluation")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "evaluations found")

    def test_get_all_evaluation_by_supervisor(self):
        """test list evaluations by supervisor"""

        createTmp()
        """create a new record"""
        url = reverse("evaluation")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "evaluations found")

    def test_get_all_evaluation_by_user(self):
        """test list evaluations by user"""

        createTmp()
        """create a new record"""
        url = reverse("evaluation")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "evaluations found")

    def test_get_all_evaluation_by_unauthenticated_user(self):
        """test list evaluations by unauthenticated user"""

        createTmp()
        """create a new record"""
        url = reverse("evaluation")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_evaluation_empty_list(self):
        """test ability to return empty list if database is empty"""
        url = reverse("evaluation")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_evaluation_by_id(self):
        """test get by id with admin credentials"""

        createTmp()
        """create a new record"""
        self.assertEqual(Evaluations.objects.count(), 1)

        url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_get_evaluation_by_id(self):
        """test get by id with supervisor credentials"""

        createTmp()
        """create a new record"""
        url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_evaluation_by_id(self):
        """test get by id with user credentials"""

        createTmp()
        """create a new record"""
        url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_get_evaluation_by_id(self):
        """test get by id with no credentials"""

        createTmp()
        """create a new record"""
        url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """test patch methods"""

    def test_admin_update_evaluation(self):
        """test ability to update record with admin credentials"""

        createTmp()
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.patch(
            update_url, {"user": "2", "link": "updatedByAdmin"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Evaluations.objects.last().user.id, 2)
        self.assertEqual(Evaluations.objects.last().link, "updatedByAdmin")

    def test_supervisor_update_evaluation(self):
        """test ability to update record with supervisor credentials"""

        createTmp()
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.patch(
            update_url,
            {"user": "2", "link": "updatedBySupervisor"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Evaluations.objects.last().user.id, 2)
        self.assertEqual(Evaluations.objects.last().link, "updatedBySupervisor")

    def test_user_update_evaluation(self):
        """test unauthorized  update record with user credentials"""

        createTmp()
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.patch(
            update_url, {"user": "2", "link": "updatedBySupervisor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update_evaluation(self):
        """test unauthorized  update record with no credentials"""

        createTmp()
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        response = self.client.patch(
            update_url,
            {"user": "2", "link": "updatedBySupervisor"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_update_evaluation_partially(self):
        """test ability to update record with admin credentials"""

        createTmp()
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.patch(
            update_url, {"link": "updatedByAdminPartially"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Evaluations.objects.last().user.id, 1)
        self.assertEqual(Evaluations.objects.last().link, "updatedByAdminPartially")

    def test_admin_update_not_exists_evaluation(self):
        """test update request error: not found -- with admin credentials"""

        createTmp()
        """create a new record"""

        update_url = f"/api/evaluation/{65}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.patch(
            update_url, {"user": "2", "link": "updatedBySupervisor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_supervisor_update_not_exists_evaluation(self):
        """test update request error: not found -- with supervisor credentials"""

        createTmp()
        """create a new record"""

        update_url = f"/api/evaluation/{65}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.patch(
            update_url, {"user": "2", "link": "updatedBySupervisor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update_not_exists_evaluation(self):
        """test user update request error: unauthorized -- with user credentials"""

        createTmp()
        """create a new record"""

        update_url = f"/api/evaluation/{65}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.patch(
            update_url, {"user": "2", "link": "updatedBySupervisor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update_not_exists_evaluation(self):
        """test user update request error: forbidden -- with no credentials"""

        createTmp()
        """create a new record"""

        update_url = f"/api/evaluation/{65}/"
        response = self.client.patch(
            update_url, {"user": "2", "link": "updatedBySupervisor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_update_evaluation_bad_request(self):
        """test update request with empty body"""

        createTmp()
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.get().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.patch(update_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_evaluation(self):
        # '''test delete record by id with admin credentials'''

        createTmp()
        """create a new record"""
        count = Evaluations.objects.count()
        delete_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Evaluations.objects.count(), count - 1)

    def test_supervisor_delete_evaluation(self):
        """test unauthorized delete record by id with supervisor credentials"""

        createTmp()
        """create a new record"""
        count = Evaluations.objects.count()
        delete_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Evaluations.objects.count(), count)

    def test_user_delete_evaluation(self):
        """test unauthorized delete record by id with supervisor credentials"""

        createTmp()
        """create a new record"""
        count = Evaluations.objects.count()
        delete_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Evaluations.objects.count(), count)

    def test_unauthenticated_delete_evaluation(self):
        """test delete record by id with no credentials"""

        createTmp()
        """create a new record"""
        count = Evaluations.objects.count()
        delete_url = f"/api/evaluation/{Evaluations.objects.last().id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Evaluations.objects.count(), count)
