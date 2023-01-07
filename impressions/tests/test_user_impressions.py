from django.test import TestCase
from django.urls.exceptions import NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from user_impressions.models import *


class TestMyPlaceRemember(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_name = "User"
        cls.user_password = "0000"
        cls.avatar = "https://picture.com/1.png"
        cls.user = User.objects.create_user(cls.user_name, "example@mail.ru",
                                            cls.user_password)
        Profile.objects.create(user=cls.user, avatar=cls.avatar)

    def test_should_redirect_to_login_for_not_auth_user(self):
        client = self.client
        url = "/remember/"
        self.assertRaises(NoReverseMatch, client.get, url)
        client.login(username=self.user_name, password=self.user_password)
        ans = client.get(url)
        good_templates = ["user_impressions/index.html", "base_with_user.html",
                          "base.html"]
        self.assertListEqual(
            list(map(lambda t: t.name, ans.templates)),
            good_templates
        )

    def test_should_to_slug_from_title_work_right(self):
        title_1 = "Лорем ипсум долор"
        title_2 = "!@#Лорем !@ипсум (долор)$%^&*"
        title_3 = "Lorem ipsum dolor"
        title = 'Lorem-ipsum-dolor'
        self.assertEqual(f"{self.user_name}-{title}",
                         to_slug_from_title(title_1, self.user_name))
        self.assertEqual(f"{self.user_name}-{title}",
                         to_slug_from_title(title_2, self.user_name))
        self.assertEqual(f"{self.user_name}-{title}",
                         to_slug_from_title(title_3, self.user_name))


    def test_should_create_remember_right(self):
        profile = Profile.objects.get(user=self.user)
        title = "Россия"
        remember = RememberModel.objects.create(
            title=title, body="Big text", profile=profile,
            location="Россия, Москва")
        self.assertEqual(f"{profile.user.username}-Rossija",
                         remember.slug)
        self.assertEqual(title, str(remember))

    def test_should_get_urls_work_right(self):
        profile = Profile.objects.get(user=self.user)
        title = "Отдых"
        remember = RememberModel.objects.create(
            title=title, body="Big text", profile=profile,
            location="Россия, Москва")
        right_slug = f"{profile.user.username}-Otdyh"
        self.assertEqual(f"/remember/{right_slug}/",
                         remember.get_absolute_url())
        self.assertEqual(f"/remember/{right_slug}/del/",
                         remember.get_absolute_delete_url())

    def test_should_create_remember_if_form_valid(self):
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        title = "Отдых"
        ans = client.post("/remember/create/", {
            "title": title,
            "location": 'Россия, Москва',
            "body": "Some big text"
        })
        self.assertEqual("/remember/", ans.url)
        self.assertIsNotNone(RememberModel.objects.get(title=title))
        self.assertEqual("/remember/", ans.url)
        ans = client.post("/remember/create/")
        template_create_remember = "user_impressions/form.html"
        self.assertIn(template_create_remember,
                      list(map(lambda t: t.name, ans.templates)))


    def test_should_remove_remember(self):
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        profile = Profile.objects.get(user=self.user)
        title = "TestTitle"
        remember = RememberModel.objects.create(title=title, location="Россия, Москва",
                                                body="Some body", profile=profile)
        ans = client.get(f"/remember/{remember.slug}/del/")
        self.assertRaises(ObjectDoesNotExist, RememberModel.objects.get, title=title)
        self.assertEqual("/remember/", ans.url)

    def test_should_return_right_temples_when_open_remember_detail(self):
        right_templates = ["user_impressions/details.html", "base_with_user.html", "base.html",
                           'home_button.html']
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        profile = Profile.objects.get(user=self.user)
        remember = RememberModel.objects.create(title="Test", location="Россия, Москва",
                                                body="Some body", profile=profile)
        ans = client.get(f"/remember/{remember.slug}/")
        self.assertListEqual(
            list(map(lambda t: t.name, ans.templates)),
            right_templates)
