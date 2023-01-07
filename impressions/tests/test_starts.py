from django.test import TestCase
from django.contrib.auth.models import User
from start.models import Profile


class TestsLogin(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("Test", "example@mail.ru", "1234",
                                 first_name="Ivan", last_name="Ivanov")

    def test_should_stay_in_login_for_not_auth_users(self):
        client = self.client
        ans = client.get("")
        templates_names_for_not_auth = ["start/index.html", "base.html"]
        self.assertListEqual(
            list(map(lambda t: t.name, ans.templates)),
            templates_names_for_not_auth
        )
        client.login(username="Test", password="1234")
        ans = client.get("")
        self.assertEqual("/remember/", ans.url)

    def test_should_profile_get_right_dict(self):
        user = User.objects.get_by_natural_key("Test")
        example_avatar = "http://pictures.com/1.png"
        profile = Profile.objects.create(user=user, avatar=example_avatar)
        self.assertDictEqual(
            {"name": "Ivan Ivanov", "avatar": example_avatar},
            profile.get_name_and_avatar()
        )

    def test_should_profile_get_right_str(self):
        user = User.objects.get_by_natural_key("Test")
        example_avatar = "http://pictures.com/1.png"
        profile = Profile.objects.create(user=user, avatar=example_avatar)
        self.assertEqual(f"User: {user.username}", str(profile))
