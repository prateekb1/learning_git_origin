from user_data.models import UserTable
from user_data.tests.test_setup import TestSetUp


class Test_RegisterAPI(TestSetUp):
    """Api to store the new user details into database"""

    def test_post_cant_register(self):
        """so save the details and generating the user id"""

        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_post_can_register(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        # import pdb
        # pdb.set_trace()

        self.assertAlmostEqual(response.status_code, 201, delta=200)

    def test_user_cannot_login_with_unverified_email(self):
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertAlmostEqual(response.status_code, 400, delta=400)

    def test_user_can_login_verified_email(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        email = self.user_data['email']

        # import pdb
        # pdb.set_trace()
        user = UserTable.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertAlmostEqual(res.status_code, 201, delta=200)

    def test_sentMail_otp_toRegister_without_verifing(self):
        res = self.client.post(self.sent_mail, self.user_data, format="json")
        self.assertAlmostEqual(res.status_code, 400, delta=400)

    def test_sentMail_otp_toRegister_verifing(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        email = self.user_data['email']
        # import pdb
        # pdb.set_trace()
        user = UserTable.objects.get(email=email)
        import pdb
        pdb.set_trace()
        user.is_verified = True
        user.save()
        res = self.client.post(self.sent_mail, self.user_data, format="json")
        self.assertAlmostEqual(res.status_code, 200, delta=200)

    # def test_otp_verification(self):
    #     # response =
    #     pass
