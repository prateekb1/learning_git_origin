from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.sent_mail = reverse("sentmail")
        self.fake = Faker()

        self.user_data = {
            "email": self.fake.email(),
            "password": self.fake.password(),
            "firstName": self.fake.name(),
            "lastName": self.fake.name(),
            "player_name": self.fake.name(),
            "team_name": self.fake.name(),
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
